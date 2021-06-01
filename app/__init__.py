"""FLASK APPLICATION."""

from flask import Flask, send_file, request, flash, redirect,\
        render_template, session
from app.dataprocess.accounting_plan import AccountingPlan
# from app.dataprocess.synthese import Synthese
from app.dataprocess.overview import Overview
from app.pdf_generation.tabletopdf import PDF
from app.dataprocess.worksite import Worksite
from app.dataprocess.office import Office
from app.dataprocess.dataframe_to_html \
        import convert_single_dataframe_to_html_table
from app.dataprocess.imports import \
        split_expenses_file_as_worksite_csv, get_accounting_file,\
        get_budget_file, split_salary_file_as_salary_csv
from app.dataprocess.date import get_month_name
from app.dataprocess.errors_to_html import errors_to_html
from app.dataprocess.forward_planning import ForwardPlanning
from app.pdf_generation.colors import bleuciel
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
app.secret_key = os.environ.get('SECRET_KEY', 'NULL')

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dgbgesfin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SESSION_TYPE = 'redis'
# Session(app)

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

if not (os.path.exists("var")):
    os.makedirs("var/csv/")

if not (os.path.exists("var/csv/")):
    os.makedirs("var/csv/")

if not (os.path.exists('bibl/')):
    os.makedirs("bibl/")


def allowed_file(filename):
    """Verifie le bon format des fichiers prerequis
    fournis par l'utilisateur."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel(username=os.environ.get('USERNAME', 'Anonymous'))
    user.set_password(os.environ.get('PASSWORD', 'Password'))
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

    if (os.path.exists("log.txt")):
        os.remove("log.txt")

    return render_template("index.html")


@app.route('/synthese_globale', methods=['POST'])
@login_required
def syntpdf():
    """
    Generation de la synthese. Sauvegarde en pdf.
    """
    date = request.form['date']
    year = date[0:4]
    month = date[5:7]
    budget = None

    filename = "bibl/Synthese.pdf"
    try:
        accounting_plan = AccountingPlan(
            get_accounting_file("var/PlanComptable.xls"))
    except Exception as e:
        return "Erreur de lecture du plan comptable " + str(e)

    try:
        budget = get_budget_file("var/Budget.xls")
    except Exception:
        print("Pas de fichier budget")
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

    pdf.add_table(formatted_overview,
                  y=A4[0] - inch * 3.2,
                  tableHeight=inch * 3,
                  indexName="CHANTIER",
                  letters='')
    pdf.create_bar_syntgraph(600, 250, overview.data)
    pdf.save_page()
    pdf.save_pdf()
    return send_file(filename, as_attachment=True)


@app.route('/synthese_divers', methods=['POST'])
@login_required
def diverspdf():
    """Generation de la synthese divers"""

    date = request.form['date']
    year = date[0:4]
    month = date[5:7]
    worksite_name = request.form['code']

    filename = "bibl/" + date + "/" + worksite_name + "_DIV.pdf"
    if not (os.path.exists('bibl/' + date)):
        os.makedirs("bibl/" + date)

    try:
        accounting_plan = AccountingPlan(
            get_accounting_file("var/PlanComptable.xls"))
    except Exception as error:
        return "Erreur de lecture du plan comptable :" + str(error)

    worksite = Worksite(accounting_plan, worksite_name)
    worksite.calculate_worksite(int(month), int(year))
    divers_result_tab = worksite.calcul_divers_result(year)
    pdf = PDF(filename)
    for nom in worksite.categories.keys():

        if (nom == "DIVERS"):
            pdf.new_page(nom, worksite_name)
            pdf.add_table(worksite.get_formatted_data(nom),
                          y=(A4[0] / 2) - inch / 2,
                          tableHeight=inch * 5)
            pdf.add_table(divers_result_tab,
                          y=inch,
                          tableHeight=inch * 2,
                          indexName="")
            pdf.add_sidetitle(get_month_name(int(month)) + ' ' + year)
            pdf.save_page()
            break

    pdf.save_pdf()
    return send_file(filename, as_attachment=True)


@app.route('/synthese_chantier', methods=['POST'])
@login_required
def chantpdf():
    """Generation de la synthese du chantier.

    Affichage en HTML pour permettre a l'utilisateur
    l'entree du Reste A Depenser."""

    date = request.form['date']
    year = date[0:4]
    month = date[5:7]
    worksite_name = request.form['code']
    budget = None

    try:
        accounting_plan = AccountingPlan(
            get_accounting_file("var/PlanComptable.xls"))
    except Exception as error:
        return "Erreur de lecture de plan comptable :" + str(error)

    # try:
    worksite = Worksite(accounting_plan, worksite_name)
    # except Exception as error:
    #    return "Erreur de lecture de fichier chantier : " + str(error)

    try:
        budget = get_budget_file("var/Budget.xls")
    except Exception:
        print("No Budget")

    worksite.calculate_worksite(int(month), int(year), budget)
    worksite.round_2dec_df()  # Verifier l'utilité
    convert_single_dataframe_to_html_table(worksite.categories, int(month),
                                           year, worksite_name)

    session['worksite_name'] = worksite_name
    session['date'] = date

    if (os.path.exists("log.txt")
            and len(open("log.txt", "r").readlines()) != 0):
        errors_to_html()
        return render_template("errors.html")
    else:
        return render_template("rad.html")


@app.route('/rad', methods=['GET', 'POST'])
@login_required
def rad():
    """Suite de chantpdf().

    Recupere les Reste A Depenser entree precedemment
    par l'utilisateur.
    Calcul les donnees manquantes, la gestion previsionnelle.
    Sauvegarde le tout en PDF."""
    if request.method == "GET":
        return render_template("rad.html")

    budget = None
    worksite_name = session.get('worksite_name',
                                'not set')  # Défini dans chantpdf()
    accounting_plan = AccountingPlan(
        get_accounting_file("var/PlanComptable.xls"))

    worksite = Worksite(accounting_plan, worksite_name)
    try:
        budget = get_budget_file("var/Budget.xls")
    except Exception:
        print("Pas de budget")

    date = session.get('date', 'not set')  # Défini dans chantpdf()
    year = date[0:4]
    month = date[5:7]
    filename = "bibl/" + date + "/" + worksite_name + ".pdf"

    if not (os.path.exists('bibl/' + date)):
        os.makedirs("bibl/" + date)

    worksite.calculate_worksite(int(month), int(year), budget)
    worksite.round_2dec_df()  # Verifier l'utilité

    for value in request.form:
        category, subcategory = value.split('$')
        worksite.add_rad(category, subcategory, request.form[value])

    worksite.compose_pfdc_budget()
    worksite.add_worksite_total()
    planning = ForwardPlanning(worksite)
    planning_margin = planning.calculate_margins(int(month),
                                                 int(year),
                                                 with_cumul=False,
                                                 with_year=True)

    planning_margin_cumul = planning.calculate_margins(int(month),
                                                       int(year),
                                                       with_cumul=True,
                                                       with_year=False)

    planning_pfdc = planning.calculate_pfdc_tab(budget)

    worksite.calcul_ges_prev()
    worksite.remove_category("PRODUITS")
    # worksite.remove_category("PRORATA")

    with open("bibl/" + date + "/" + worksite_name + "_tt.txt", "w") as file:
        file.write(str(worksite.categories["GESPREV"].iloc[-1]["PFDC"]))

    worksite.round_2dec_df()
    pdf = PDF(filename)

    for nom in worksite.categories.keys():

        if (nom == "GESPREV"):
            pdf.new_page("Gestion prévisionnelle 1/2", worksite_name)
            # pdf.add_table(worksite.get_formatted_data(nom),
            #              y=A4[0] - inch * 3.2,x=inch*4,tableHeight=inch*3)
            # pdf.create_bar_gesprevgraph(600, 250, worksite)
            # pdf.add_table(planning_margin,y=A4[0]-inch*3.2,x=inch*9.6,tableHeight=inch*2,indexName="Temps")
            # pdf.add_table(planning_pfdc,y=inch*2,x=A4[1]-inch*1.5,tableHeight=inch*2,indexName="Marges")
            pdf.add_table(worksite.get_formatted_data(nom),
                          y=A4[0] - inch * 3.2,
                          tableHeight=inch * 3,
                          coloring=True)

            pdf.add_table(planning_margin,
                          y=inch * 2,
                          x=inch * 4.5,
                          tableHeight=inch * 2,
                          indexName="Période",
                          title="Marge à l'avancement",
                          coloring=True,
                          total=False,
                          letters='marge_a_avancement')

            pdf.add_table(planning_pfdc,
                          y=inch * 2,
                          x=A4[1] - inch * 3,
                          tableHeight=inch * 2,
                          indexName="Marges",
                          title="Marge à fin de chantier",
                          noIndexLine=True,
                          coloring=True,
                          total=False,
                          letters='marge_fdc')

            pdf.add_legend("PFDC = Prévision fin de chantier",
                           x=0.1 * inch,
                           y=0.2 * inch)
            pdf.add_legend("RAD = Restes à dépenser",
                           x=inch * 0.1,
                           y=0.4 * inch)
            pdf.add_legend("CA = Chiffre d'affaires",
                           x=inch * 0.1,
                           y=0.6 * inch)
            pdf.add_sidetitle(get_month_name(int(month)) + ' ' + year)
            pdf.save_page()

            pdf.new_page("Gestion prévisionnelle 2/2", worksite_name)
            pdf.add_table(planning_margin_cumul,
                          tableHeight=inch * 2,
                          indexName="Période",
                          title="Marge à l'avancement",
                          coloring=True,
                          total=False,
                          letters='marge_a_avancement')

        elif (nom == "DIVERS"):
            continue
        else:
            pdf.new_page(nom, worksite_name)
            pdf.add_table(worksite.get_formatted_data(nom),
                          y=(A4[0] / 2) - inch / 2,
                          tableHeight=inch * 5)

        pdf.add_sidetitle(get_month_name(int(month)) + ' ' + year)
        pdf.save_page()

    pdf.save_pdf()
    return send_file(filename, as_attachment=True)


@app.route('/synthese_structure', methods=['POST', 'GET'])
@login_required
def structpdf():
    """Generation du bilan de la structure."""
    if request.method == 'POST':
        date = request.form['date']
        year = date[0:4]
        month = date[5:7]

        filename = "bibl/Structure" + year + "-" + month + ".pdf"
        try:
            accounting_plan = AccountingPlan(
                get_accounting_file("var/PlanComptable.xls"))
        except Exception as e:
            return "Erreur de lecture du plan comptable : " + str(e)

        # try:
        office = Office(accounting_plan, int(month), int(year))
        # except Exception as e:
        #    return "Erreur de lecture des charges de la structure : "+str(e)

        if not (os.path.exists("bibl/" + date)):
            os.makedirs("bibl/" + date)

        office.calculate_office()

        pdf = PDF(filename)
        pdf.new_page("Structure", get_month_name(int(month)) + ' ' + year)

        num_poste = 0  # nombre de postes sur la page courante
        df = None
        style = []
        current_nb_of_rows = 1

        for i in range(len(office.category_names)):
            print(office.category_names)
            if num_poste >= 2 or i >= len(office.category_names) - 1:
                style.append(('SPAN', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows)))
                # Titre de section
                style.append(('BACKGROUND', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows),bleuciel))

                df = df.append(
                    office.get_formatted_data(office.category_names[i]))
                pdf.new_page("Structure", " ")
                pdf.add_table(df, custom_style=style,
                        total=(i >= len(office.category_names)-1))
                pdf.add_sidetitle(get_month_name(int(month)) + ' ' + year)
                df = None
                num_poste = 0
                current_nb_of_rows = 1
                style = []
                pdf.save_page()
            elif df is None:
                num_poste += 1
                style.append(('SPAN', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows)))
                style.append(('BACKGROUND', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows),bleuciel))

                # Titre de section

                df = office.get_formatted_data(office.category_names[i])
                current_nb_of_rows = len(df.index) + 1
            else:
                num_poste += 1
                print("\nHELO from " + office.category_names[i] + "\n")
                style.append(('SPAN', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows)))
                style.append(('BACKGROUND', (0, current_nb_of_rows),
                              (-1, current_nb_of_rows),bleuciel))

                # Titre de section

                df = df.append(
                    office.get_formatted_data(office.category_names[i]))
                current_nb_of_rows = len(df.index) + 1

        for i in style:
            print("\n" + str(i) + "\n")
        pdf.save_pdf()

        return send_file(filename, as_attachment=True)
    return "B"


@app.route('/download_last_file', methods=['GET', 'POST'])
@login_required
def download_last_file():
    filename = session.get('filename', 'not set')
    return send_file(filename, as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Page permettant a l'utilisateur le telechargement sur le serveur,
    des fichiers prerequis pour le calcul des bilans."""
    tic = time.perf_counter()
    if not current_user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':

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
    if (os.path.exists("var/csv/")):
        for filename in os.listdir("var/csv"):
            os.remove("var/csv/" + filename)
    if (os.path.exists("log.txt")):
        os.remove("log.txt")
    if (os.path.exists("var/PlanComptable.xls")):
        os.remove("var/PlanComptable.xls")
    if (os.path.exists("var/Charges.xls")):
        os.remove("var/Charges.xls")
    if (os.path.exists("var/Budget.xls")):
        os.remove("var/Budget.xls")


def check_save_uploaded_file(tag):

    if tag not in request.files:
        print("tag not in request")
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
                split_salary_file_as_salary_csv(filepath=os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    tag + '.' + filename.split('.')[1]),
                                                outputpath="var/csv/")
