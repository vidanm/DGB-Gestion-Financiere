import pandas as pd
import sys
import time
from flask import Flask,send_file,request,flash,redirect,url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
from app.dataprocess.plan_comptable import *
from app.dataprocess.synthese import *
from app.pdf_generation.tabletopdf import *
from app.dataprocess.postesparent import *
from app.dataprocess.postes_chantier import *
from app.dataprocess.postes_structure import *
from app.dataprocess.read_file import read_budget
from app.dataprocess.dataframe_to_html import *

'''
postes = Postes(plan)
postes.calcul_chantier(charges.get_raw_chantier("19-GP-ROSN"),6,2020)
'''

UPLOAD_FOLDER= 'var'
DOWNLOAD_FOLDER = 'bibl'
ALLOWED_EXTENSIONS = ['xls']

app = Flask("DGB Gesfin")
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

codes_missing = open("missing_numbers.txt","w")
expected_files = ['plan','charges','budget']

postes = None #Stockage des donnees sous pdf
mois = "" #Mois du pdf genere
code = "" #Code chantier STRUCT ou GLOB du pdf
date = "" #Date complete du pdf genere

def check_file_here():
    '''
        Verifie la presence des fichiers prerequis qui sont : 
        - Le Plan Comptable
        - Les Charges
        - Le Budget
    '''
    plan = None;
    charges = None;
    for filename in os.listdir('var'):
        print(filename)
        if 'plan.xls' == filename:
            plan = PlanComptable('var/plan.xls')
        if 'charges.xls' == filename and plan != None:
                charges = Charges('var/charges.xls',plan,codes_missing)
        if 'budget.xls' == filename:
            budget = read_budget('var/budget.xls')
    
    return (plan,charges,budget)


def allowed_file(filename):
    
    '''
        Verifie le bon format des fichiers prerequis fournis par l'utilisateur
    '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    
    '''
        Page d'accueil
    '''

    charges_modif = time.ctime(os.path.getmtime('var/charges.xls'))
    plan_modif = time.ctime(os.path.getmtime('var/plan.xls'))

    return render_template("index.html") + '<p>' + 'Dernière mise à jour du fichier de charges : '+ str(charges_modif) + '</p><p>' + 'Dernière mise à jour du plan comptable : '+str(plan_modif) + '</p>'



@app.route('/synthese_globale',methods=['POST','GET'])
def syntpdf():

    '''
        Generation de la synthese
        Sauvegarde en pdf
    '''
    global date
    date = request.form['date']
    plan,charges,budget = check_file_here()
    if (plan == None or charges == None):
        return "Missing file"

    syn = Synthese(charges)
    pdf = PDF("bibl/Synthese.pdf")
    syn.calcul_synthese_annee(6,2020)

    pdf.new_page("Synthese",date)
    pdf.add_table(syn.synthese_annee,x='center',y='center')
    pdf.create_bar_graph()
    pdf.save_page()
    pdf.save_pdf()
    return send_file("bibl/Synthese.pdf",as_attachment=True)


@app.route('/synthese_chantier',methods=['POST','GET'])
def chantpdf():

    '''
        Generation de la synthese du chantier
        Affichage en HTML pour permettre a l'utilisateur
        l'entree du Reste A Depenser
    '''
    
    global code
    global date
    global postes

    if request.method == 'POST':
        date = request.form['date']
        year = date[0:4]
        month = date[5:7]
        print(month)
        print(year)
        code = request.form['code']

        plan,charges,budget = check_file_here();
        if (plan == None or charges == None):
            return "Missing file"

        filename = "bibl/"+code+"_"+request.form['date']+".pdf"
        postes = ChantierPoste(plan,charges,code)
        postes.calcul_chantier(int(month),int(year),budget)
        postes.round_2dec_df()
        convert_single_dataframe_to_html_table(postes.dicPostes,month,year,code)

        return render_template("rad.html")
        
        ''''''
    return "A"

@app.route('/rad',methods=['POST'])
def rad():
    '''
        Suite de chantpdf()
        Recupere les Reste A Depenser entree precedemment par
        l'utilisateur
        Calcul les donnees manquantes, la gestion previsionnelle
        Sauvegarde le tout en PDF
    '''
    global postes #Défini dans chantpdf()
    global code #Défini dans chantpdf()
    global date #Défini dans chantpdf()
    filename = "bibl/"+date+"/"+code+".pdf"
    
    if not (os.path.exists("bibl/"+date)):
        os.makedirs("bibl/"+date)

    for value in request.form:
        poste,sousposte = value.split('$')
        postes.ajoute_rad(poste,sousposte,request.form[value])
    postes.calcul_pfdc_budget()
    postes.calcul_total_chantier()
    postes.calcul_ges_prev()
    postes.remove_poste("FACTURATION CLIENT")
    postes.dicPostes["GESPREV"].iloc[-1].to_csv("bibl/"+date+"/"+code+"_tt.csv")
    #postes.dicPostes["GESPREV"].iloc[-1] = pd.read_csv("bibl/"+date+"/"+code+"_tt.csv")
    #print(postes.dicPostes["GESPREV"].iloc[-1])
    postes.round_2dec_df()
    pdf = PDF(filename)

    for nom in postes.dicPostes.keys():
        pdf.new_page(nom,code)
        pdf.add_sidetitle(str(date))
        if (nom == "GESPREV"):
            pdf.add_table(postes.dicPostes[nom],y=A4[0]-inch*4)
            pdf.create_bar_graph(600,250,postes)
        else :
            pdf.add_table(postes.dicPostes[nom])

        pdf.save_page()
    
    pdf.save_pdf()
    return send_file(filename,as_attachment=True)


@app.route('/synthese_structure',methods=['POST','GET'])
def structpdf():
    '''
        Generation du bilan de la structure
    '''
    if request.method == 'POST':
        date = request.form['date']
        code = "STRUCT"
        plan,charges,budget = check_file_here();
        if (plan == None or charges == None):
            return "Missing file"

        
        filename = "bibl/"+date+"/"+code+".pdf"
        if not (os.path.exists("bibl/"+date)):
            os.makedirs("bibl/"+date)        

        postes = StructPoste(plan,charges)
        postes.calcul_structure(6,2020)
        pdf = PDF(filename)
        pdf.new_page("STRUCT",code)
        pdf.add_sidetitle(str(date))
        pdf.add_struct_table(postes.format_for_pdf(),postes.row_noms)
        pdf.save_page()
        pdf.save_pdf()

        return send_file(filename,as_attachment=True)
    return "B"


@app.route('/upload',methods=['GET','POST'])
def upload_file():
    '''
        Page permettant a l'utilisateur 
        le telechargement sur le serveur, 
        des fichiers prerequis pour le calcul des bilans
    '''
    if request.method == 'POST':
        files = []
        # check if the post request has the file part
        print(request.files)
        for fileit in expected_files :
            if fileit not in request.files:
                print('No file part')
                continue
            file = request.files[fileit]
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                continue
            if file and allowed_file(file.filename):
                filename = fileit
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename+".xls"))
        return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template("upload.html")
 

@app.route('/loading')
def loading_page():
    '''
        Pas utilise
    '''
    return render_template("loader.html")


@app.route('/bibliotheque')
def bibliotheque() :
    
    '''
        Obsolete ( Pas forcement d'interet )
    '''
    
    out = "<!DOCTYPE HTML><html><body>"
    for filename in os.listdir('bibl'):
        out += '<a href="/download/'+filename+'">'+filename+'</a><br>'
    return out + "</body></html>"

@app.route('/download/<path:filename>', methods=['GET','POST'])
def download(filename):
    
    '''
        Obsolete ( Telechargement depuis la bibliotheque )
    '''

    bibl = os.path.join(app.root_path,app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(directory=bibl,filename=filename)


@app.route('/table')
def table():\

    '''
        Obsolete ?
    '''

    table = postes.dicPostes["MO"]
    return table.to_html()


