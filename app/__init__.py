"""FLASK APPLICATION."""

from flask import Flask, send_file, request, flash, redirect, render_template
from app.dataprocess.accounting_plan import AccountingPlan
# from app.dataprocess.synthese import Synthese
from app.dataprocess.overview import Overview
from app.pdf_generation.tabletopdf import PDF
from app.dataprocess.worksite import Worksite
from app.dataprocess.expenses import Expenses
from app.dataprocess.office import Office

from app.dataprocess.dataframe_to_html \
        import convert_single_dataframe_to_html_table

from app.dataprocess.imports import get_expenses_file,\
        split_expenses_file_as_worksite_csv, get_accounting_file,\
        get_budget_file, split_salary_file_as_salary_csv

from app.dataprocess.date import get_month_name
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .models import db, login, UserModel
from flask_login import current_user, login_user, login_required, logout_user
import os
import time

UPLOAD_FOLDER = 'var'
DOWNLOAD_FOLDER = 'bibl'
ALLOWED_EXTENSIONS = ['xls']

app = Flask("DGB Gesfin")
app.secret_key = os.environ.get('SECRET_KEY','NULL')

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dgbgesfin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login.init_app(app)
login.login_view = 'login'

worksite = None  # Stockage des donnees sous pdf
month = ""  # Mois du pdf genere
worksite_name = ""  # Code chantier STRUCT ou GLOB du pdf
date = ""  # Date complete du pdf genere
filename = ""

def allowed_file(filename):
    """Verifie le bon format des fichiers prerequis
    fournis par l'utilisateur."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel(username = os.environ.get('USERNAME','Anonymous'))
    user.set_password(os.environ.get('PASSWORD','Password'))
    db.session.add(user)
    db.session.commit()


@app.route('/login', methods=['POST', 'GET'])
def user_login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        user = UserModel.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/upload')

    return render_template('login.html')


@app.route('/logout')
def logout():
    clear()
    logout_user()
    return redirect('/login')


@app.route('/errors')
def error_page():
    return render_template("error.html")


@app.route('/')
def index():
    """Page d'accueil."""
    if not current_user.is_authenticated:
        return redirect('/login')

    if not (os.path.exists("var/csv/")):
        os.makedirs("var/csv/")

    if not (os.path.exists('bibl/')):
        os.makedirs("bibl/")

    return render_template(
        "index.html"
    )


@app.route('/synthese_globale', methods=['POST'])
@login_required
def syntpdf():
    """
    Generation de la synthese. Sauvegarde en pdf.
    """
    tic = time.perf_counter()
    global date
    global filename
    date = request.form['date']
    year = date[0:4]
    month = date[5:7]

    filename = "bibl/Synthese.pdf"
    accounting_plan = AccountingPlan(
        get_accounting_file("var/PlanComptable.xls"))
    budget = get_budget_file("var/Budget.xls")
    # revenues = Revenues(charges.get_raw_charges())
    # camois = CA.calcul_ca_mois(int(month),int(year))
    # cacumul = CA.calcul_ca_annee(int(year))

    overview = Overview(accounting_plan, int(month), int(year))
    pdf = PDF(filename)

    overview.calculate_data(int(month), int(year), budget)
    overview.add_total()
    # overview.calcul_tableau_ca(camois,cacumul)
    formatted_overview = overview.get_formatted_data()

    pdf.new_page("Synthese", get_month_name(int(date[5:7])) + ' ' + year)
    pdf.add_table(formatted_overview, y=A4[0] - inch * 3.2, tableHeight=inch*3)
    pdf.create_bar_syntgraph(600, 250, overview.data)
    pdf.save_page()
    pdf.save_pdf()
    toc = time.perf_counter()
    print(f"SYN : {toc-tic:4f} seconds")
    return send_file(filename, as_attachment=True)


@app.route('/synthese_chantier', methods=['POST'])
@login_required
def chantpdf():
    """Generation de la synthese du chantier.

    Affichage en HTML pour permettre a l'utilisateur
    l'entree du Reste A Depenser."""
    tic = time.perf_counter()
    global worksite_name
    global date
    global worksite

    date = request.form['date']
    year = date[0:4]
    month = date[5:7]
    worksite_name = request.form['code']

    try:
        accounting_plan = AccountingPlan(
            get_accounting_file("var/PlanComptable.xls"))
    except Exception as error:
        return "Erreur de lecture de fichiers :" + str(error)

    try:
        worksite = Worksite(accounting_plan, worksite_name)
    except Exception as error:
        return "Erreur de lecture de fichiers : " + str(error)

    try:
        budget = get_budget_file("var/Budget.xls")
    except Exception as error:
        return "Erreur de lecture de fichiers :" + str(error)

    worksite.calculate_worksite(int(month), int(year), budget)
    worksite.round_2dec_df()
    convert_single_dataframe_to_html_table(worksite.categories, month, year,
                                           worksite_name)
    toc = time.perf_counter()
    print(f"CHA : {toc-tic:4f} seconds")
    return render_template("rad.html")


@app.route('/rad', methods=['POST'])
@login_required
def rad():
    """Suite de chantpdf(). 

    Recupere les Reste A Depenser entree precedemment
    par l'utilisateur.
    Calcul les donnees manquantes, la gestion previsionnelle.
    Sauvegarde le tout en PDF."""
    global filename
    global worksite  # Défini dans chantpdf()
    global worksite_name  # Défini dans chantpdf()
    global date  # Défini dans chantpdf()
    filename = "bibl/" + date + "/" + worksite_name + ".pdf"

    year = date[0:4]
    month = date[5:7]
    if not (os.path.exists("bibl/" + date)):
        os.makedirs("bibl/" + date)

    for value in request.form:
        category, subcategory = value.split('$')
        worksite.add_rad(category, subcategory, request.form[value])

    worksite.compose_pfdc_budget()
    worksite.add_worksite_total()
    worksite.calcul_ges_prev()
    worksite.remove_category("PRODUITS")
    with open("bibl/" + date + "/" + worksite_name + "_tt.txt", "w") as file:
        file.write(str(worksite.categories["GESPREV"].iloc[-1]["PFDC"]))

    worksite.round_2dec_df()
    pdf = PDF(filename)

    for nom in worksite.categories.keys():

        if (nom == "GESPREV"):
            pdf.new_page("Gestion prévisionnelle", worksite_name)
            pdf.add_table(worksite.get_formatted_data(nom),
                          y=A4[0] - inch * 3.2, tableHeight=inch*3)
            pdf.create_bar_gesprevgraph(600, 250, worksite)
        else:
            pdf.new_page(nom, worksite_name)
            pdf.add_table(worksite.get_formatted_data(nom),
                          y=(A4[0]/2)-inch/2, tableHeight=inch*5)
        
        pdf.add_sidetitle(get_month_name(int(month)) + ' ' + year)
        pdf.save_page()

    pdf.save_pdf()
    return send_file(filename, as_attachment=True)


@app.route('/synthese_structure', methods=['POST', 'GET'])
@login_required
def structpdf():
    """Generation du bilan de la structure."""
    global filename
    tic = time.perf_counter()
    if request.method == 'POST':
        date = request.form['date']
        year = date[0:4]
        month = date[5:7]

        filename = "bibl/Structure" + year + "-" + month + ".pdf"
        accounting_plan = AccountingPlan(
            get_accounting_file("var/PlanComptable.xls"))
        year_expenses = Expenses(get_expenses_file("var/Charges.xls"),
                                 accounting_plan)
        office = Office(accounting_plan, year_expenses, 2020)

        if not (os.path.exists("bibl/" + date)):
            os.makedirs("bibl/" + date)

        office.calculate_office(month)

        pdf = PDF(filename)
        pdf.new_page("Structure", get_month_name(int(month)) + ' ' + year)
        pdf.add_struct_table(office.format_for_pdf(),
                             office.row_names,
                             size=0.6)
        pdf.save_page()
        pdf.save_pdf()

        toc = time.perf_counter()
        print(f"STRU : {toc-tic:4f} seconds")
        return send_file(filename, as_attachment=True)
    return "B"

@app.route('/download_last_file', methods=['GET','POST'])
@login_required
def download_last_file():
    global filename
    print(filename)
    return send_file(filename, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Page permettant a l'utilisateur le telechargement sur le serveur,
    des fichiers prerequis pour le calcul des bilans."""
    tic = time.perf_counter()
    if not current_user.is_authenticated:
        return redirect('/login')

    if not (os.path.exists("var/csv/")):
        os.makedirs("var/csv/")

    if not (os.path.exists('bibl/')):
        os.makedirs("bibl/")


    if request.method == 'POST':
        if not (os.path.exists("var/")):
            os.makedirs("var/")

        if not (os.path.exists("var/csv/")):
            os.makedirs("var/csv/")

        # files = []
        #  check if the post request has the file part
        check_save_uploaded_file("PlanComptable")
        check_save_uploaded_file("Charges")
        check_save_uploaded_file("Budget")
        check_save_uploaded_file("MasseSalariale")
        toc = time.perf_counter()
        print(f"IMP : {toc-tic:4f} seconds")

        return redirect('/')
        # return redirect(url_for('upload_file',filename=filename))
    return render_template("upload.html")


def clear():
    for filename in os.listdir("var/csv"):
        os.remove("var/csv/"+filename)


def check_save_uploaded_file(tag):

    if tag not in request.files:
        print("tag non")
    else:
        file = request.files[tag]
        if file.filename == '':
            flash("No selected files")
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(
                os.path.join(app.config["UPLOAD_FOLDER"],
                             tag + '.' + filename.split('.')[1]))

            if tag == "Charges":
                split_expenses_file_as_worksite_csv(filepath=os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    tag + '.' + filename.split('.')[1]),
                                                    outputpath="var/csv/")
            elif tag == "MasseSalariale":
                split_salary_file_as_salary_csv(
                        filepath=os.path.join(
                            app.config['UPLOAD_FOLDER'],
                            tag + '.' + filename.split('.')[1]),
                        outputpath="var/csv/")
