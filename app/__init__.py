import sys
import os
from flask import Flask,send_file,request,flash,redirect,url_for,render_template
from werkzeug.utils import secure_filename
from app.dataprocess.plan_comptable import *
from app.dataprocess.poste import *
from app.pdf_generation.tabletopdf import *

plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
codes_missing = open("missing_numbers.txt","w")
charges = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",plan,codes_missing)
postes = Postes(plan)
postes.calcul_chantier(charges.get_raw_chantier("19-GP-ROSN"),6,2020)

app = Flask("DGB Gesfin")
UPLOAD_FOLDER= '~/DGBGesfinFlask/var/'
ALLOWED_EXTENSIONS = ['pdf','txt','xlsx']
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table')
def table():
    table = postes.dicPostes["MO"]
    return table.to_html()

@app.route('/pdf')
def pdf():
    pdf = TablePDF("DGB.pdf")
    pdf.new_page("Page test","sous test",postes.dicPostes["MO"])
    pdf.save_pdf()
    return send_file("DGB.pdf",as_attachment=True)

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template("upload.html")
    
