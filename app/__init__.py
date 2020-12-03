import sys
import os
from flask import Flask,send_file,request,flash,redirect,url_for,render_template
from werkzeug.utils import secure_filename
from app.dataprocess.plan_comptable import *
from app.dataprocess.poste import *
from app.pdf_generation.tabletopdf import *

'''
postes = Postes(plan)
postes.calcul_chantier(charges.get_raw_chantier("19-GP-ROSN"),6,2020)
'''

UPLOAD_FOLDER= 'var'
ALLOWED_EXTENSIONS = ['xlsx']

app = Flask("DGB Gesfin")

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    return render_template("index.html")

@app.route('/table')
def table():
    table = postes.dicPostes["MO"]
    return table.to_html()

@app.route('/pdf')
def pdf():
    
    plan,charges = check_file_here();
    if (plan == None or charges == None):
        return "Missing file"

    postes = Postes(plan)
    postes.calcul_chantier(charges.get_raw_chantier("19-GP-ROSN"),6,2020)
    pdf = TablePDF("DGB.pdf")
    pdf.new_page("MATERIELS","19-GP-ROSN | Juin 2020",postes.dicPostes["MATERIELS"])
    pdf.save_pdf()
    return send_file("DGB.pdf",as_attachment=True)

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
 
@app.route('/bibliotheque')
def bibliotheque() :
    out = ""
    for filename in os.listdir('bibl'):
        out += '<a href="~/DGBGesfinFlask/bibl/'+filename +'>'+ filename  + '</a><br>'
    return out
