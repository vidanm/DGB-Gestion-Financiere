from flask import Flask,send_file,request,flash,redirect,url_for,render_template
from app.dataprocess.plan_comptable import PlanComptable
from app.dataprocess.synthese import Synthese
from app.pdf_generation.tabletopdf import PDF
from app.dataprocess.postes_chantier import ChantierPoste
from app.dataprocess.charges import Charges
from app.dataprocess.chiffreaffaire import ChiffreAffaire
from app.dataprocess.postes_structure import StructPoste
from app.dataprocess.dataframe_to_html import convert_single_dataframe_to_html_table
from app.dataprocess.read_file import CustomFileReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os

UPLOAD_FOLDER= 'var'
DOWNLOAD_FOLDER = 'bibl'
ALLOWED_EXTENSIONS = ['xls']

app = Flask("DGB Gesfin")
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

codes_missing = open("missing_numbers.txt","w")
expected_files = ['plan','charges','budget']
annee_disponibles = []

postes = None #Stockage des donnees sous pdf
mois = "" #Mois du pdf genere
code = "" #Code chantier STRUCT ou GLOB du pdf
date = "" #Date complete du pdf genere


def get_files(path,year):

    try:
        files = CustomFileReader("var/",year)
    except Exception as error:
        files = None
        raise error
    return files


def allowed_file(filename):
    """Verifie le bon format des fichiers prerequis fournis par l'utilisateur."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Page d'accueil."""
    #charges_modif = time.ctime(os.path.getmtime('var/charges.xls'))
    #plan_modif = time.ctime(os.path.getmtime('var/plan.xls'))

    return render_template("index.html") #+ '<p>' + 'Dernière mise à jour du fichier de charges : '+ str(charges_modif) + '</p><p>' + 'Dernière mise à jour du plan comptable : '+str(plan_modif) + '</p>'



@app.route('/synthese_globale',methods=['POST'])
def syntpdf():
    """Generation de la synthese. Sauvegarde en pdf."""
    global date
    date = request.form['date']
    year = date[0:4]
    month = date[5:7]

    try:
        files = get_files("var/",year)
    except Exception as error:
        return "Erreur de lecture de fichiers : "+ str(error)  

    plan = PlanComptable(files.get_plan())
    charges = Charges(files.get_charges(),plan,codes_missing)
    budget = files.get_budget()
    CA = ChiffreAffaire(charges.get_raw_charges())
    
    camois = CA.calcul_ca_mois(int(month),int(year))
    cacumul = CA.calcul_ca_annee(int(year))

    syn = Synthese(charges)
    pdf = PDF("bibl/Synthese.pdf")
    syn.calcul_synthese_annee(int(month),int(year),budget)
    syn.calcul_tableau_ca(camois,cacumul)

    pdf.new_page("Synthese",date)
    pdf.add_table(syn.synthese_annee,y=A4[0]-inch*4.5)
    pdf.add_table(syn.total_ca_marge,y=inch*3,x=A4[1]-inch*5)
    pdf.create_bar_syntgraph(600,250,syn.synthese_annee)
    pdf.save_page()
    pdf.save_pdf()
    return send_file("bibl/Synthese.pdf",as_attachment=True)


@app.route('/synthese_chantier',methods=['POST'])
def chantpdf():
    """Generation de la synthese du chantier. Affichage en HTML pour permettre a l'utilisateur l'entree du Reste A Depenser."""
    global code
    global date
    global postes

    date = request.form['date']
    year = date[0:4]
    month = date[5:7]
    print(month)
    print(year)
    code = request.form['code']

    try:
        files = get_files("var/",year)
    except Exception as error:
        return "Erreur de lecture de fichiers : "+ str(error)


    plan = PlanComptable(files.get_plan())
    charges = Charges(files.get_charges(),plan,codes_missing)
    budget = files.get_budget()
    
    #filename = "bibl/"+code+"_"+request.form['date']+".pdf"
    postes = ChantierPoste(plan,charges,code)
    try :
        postes.calcul_chantier(int(month),int(year),budget)
    except Exception as e :
        print(e)
        return str(e)
    
    postes.round_2dec_df()
    convert_single_dataframe_to_html_table(postes.dicPostes,month,year,code)

    return render_template("rad.html")
    

@app.route('/rad',methods=['POST'])
def rad():
    """Suite de chantpdf(). Recupere les Reste A Depenser entree precedemment par l'utilisateur. Calcul les donnees manquantes, la gestion previsionnelle. Sauvegarde le tout en PDF."""
    global postes #Défini dans chantpdf()
    global code #Défini dans chantpdf()
    global date #Défini dans chantpdf()
    filename = "bibl/"+date+"/"+code+".pdf"
    
    if not (os.path.exists("bibl/"+date)):
        os.makedirs("bibl/"+date)

    for value in request.form:
        poste,sousposte = value.split('$')
        print(request.form[value])
        postes.ajoute_rad(poste,sousposte,request.form[value])
    
    postes.calcul_pfdc_budget()
    postes.calcul_total_chantier()
    postes.calcul_ges_prev()
    postes.remove_poste("PRODUITS")
    with open("bibl/"+date+"/"+code+"_tt.txt","w") as file:
        file.write(str(postes.dicPostes["GESPREV"].iloc[-1]["PFDC"]))

    #postes.dicPostes["GESPREV"].iloc[-1] = pd.read_csv("bibl/"+date+"/"+code+"_tt.csv")
    #print(postes.dicPostes["GESPREV"].iloc[-1])
    postes.round_2dec_df()
    pdf = PDF(filename)

    for nom in postes.dicPostes.keys():
        pdf.new_page(nom,code)
        pdf.add_sidetitle(str(date))
        if (nom == "GESPREV"):
            pdf.add_table(postes.dicPostes[nom],y=A4[0]-inch*4)
            pdf.create_bar_gesprevgraph(600,250,postes)
        else :
            pdf.add_table(postes.dicPostes[nom])

        pdf.save_page()
    
    pdf.save_pdf()
    return send_file(filename,as_attachment=True)


@app.route('/synthese_structure',methods=['POST','GET'])
def structpdf():
    """Generation du bilan de la structure."""
    if request.method == 'POST':
        date = request.form['date']
        year = date[0:4]
        month = date[5:7]
        code = "STRUCT"

        try:
            files = get_files("var/",year)
        except Exception as error:
            return "Erreur de lecture de fichiers : "+ str(error)

        plan = PlanComptable(files.get_plan())
        charges = Charges(files.get_charges(),plan,codes_missing)
        #budget = files.get_budget()
      
        filename = "bibl/"+date+"/"+code+".pdf"
        if not (os.path.exists("bibl/"+date)):
            os.makedirs("bibl/"+date)        

        postes = StructPoste(plan,charges)
        postes.calcul_structure(month,year)
        pdf = PDF(filename)
        pdf.new_page("STRUCT","")
        pdf.add_sidetitle(str(date))
        pdf.add_struct_table(postes.format_for_pdf(),postes.row_noms,size=0.6)
        pdf.save_page()
        pdf.save_pdf()

        return send_file(filename,as_attachment=True)
    return "B"


@app.route('/upload',methods=['GET','POST'])
def upload_file():
    """Page permettant a l'utilisateur le telechargement sur le serveur, des fichiers prerequis pour le calcul des bilans."""
    if request.method == 'POST':
        #files = []
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
 
