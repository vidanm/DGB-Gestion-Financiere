import sys
import os
import time
from flask import Flask,send_file,request,flash,redirect,url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
from app.dataprocess.plan_comptable import *
from app.dataprocess.poste import *
from app.dataprocess.synthese import *
from app.pdf_generation.tabletopdf import *

'''
postes = Postes(plan)
postes.calcul_chantier(charges.get_raw_chantier("19-GP-ROSN"),6,2020)
'''

UPLOAD_FOLDER= 'var'
DOWNLOAD_FOLDER = 'bibl'
ALLOWED_EXTENSIONS = ['xlsx']

app = Flask("DGB Gesfin")

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

codes_missing = open("missing_numbers.txt","w")
expected_files = ['plan','charges']


def check_file_here():
    plan = None;
    charges = None;
    for filename in os.listdir('var'):
        if filename == 'plan':
            plan = PlanComptable('var/plan.xlsx')
        if filename == 'charges':
            charges = Charges('var/charges.xlsx',plan,codes_missing)
    
    return (plan,charges)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    charges_modif = time.ctime(os.path.getmtime('var/charges.xlsx'))
    plan_modif = time.ctime(os.path.getmtime('var/plan.xlsx'))

    return render_template("index.html") + '<p>' + 'Dernière mise à jour du fichier de charges : '+ str(charges_modif) + '</p><p>' + 'Dernière mise à jour du plan comptable : '+str(plan_modif) + '</p>'



@app.route('/rad')
def rad():
    return render_template("rad.html")



@app.route('/table')
def table():
    table = postes.dicPostes["MO"]
    return table.to_html()



@app.route('/synthese_globale',methods=['POST','GET'])
def syntpdf():
    plan,charges = check_file_here()
    if (plan == None or charges == None):
        return "Missing file"

    syn = Synthese(charges)
    pdf = PDF("bibl/Synthese.pdf")
    syn.calcul_synthese_annee(6,2020)

    pdf.new_page("Synthese","Juin 2020")
    pdf.add_table(syn.synthese_annee,x='center',y='center')
    pdf.create_bar_graph()
    pdf.save_page()
    pdf.save_pdf()
    return send_file("bibl/Synthese.pdf",as_attachment=True)



@app.route('/synthese_chantier',methods=['POST','GET'])
def chantpdf():
    
    if request.method == 'POST':
        date = request.form['date']
        print(date)
        code = request.form['code']

        plan,charges = check_file_here();
        if (plan == None or charges == None):
            return "Missing file"

        filename = "bibl/"+code+"_"+request.form['date']+".pdf"
        postes = Postes(plan,code)
        postes.calcul_chantier(charges.get_raw_chantier(code),6,2020)
        postes.calcul_structure(charges.get_struct(),6,2020)
        postes.calcul_pfdc_budget()
        postes.round_2dec_df()
        pdf = PDF(filename)
        
        for nom in postes.nomPostes:
            pdf.new_page(nom,code)
            pdf.add_table(postes.dicPostes[nom])
            pdf.save_page()

        pdf.save_pdf()
        return send_file(filename,as_attachment=True)
    return "A"



@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        files = []
        # check if the post request has the file part
        print(request.files)
        for fileit in expected_files :
            if fileit not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files[fileit]
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = fileit
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename+".xlsx"))
        return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template("upload.html")
 

@app.route('/loading')
def loading_page():
    return render_template("loader.html")


@app.route('/bibliotheque')
def bibliotheque() :
    out = "<!DOCTYPE HTML><html><body>"
    for filename in os.listdir('bibl'):
        out += '<a href="/download/'+filename+'">'+filename+'</a><br>'
    return out + "</body></html>"

@app.route('/download/<path:filename>', methods=['GET','POST'])
def download(filename):
    bibl = os.path.join(app.root_path,app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(directory=bibl,filename=filename)

