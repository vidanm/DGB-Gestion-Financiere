"""Ce fichier permet la transformation en html dans le style du site\
        des données de synthese chantier dans le but de laisser\
        a l'utilisateur la possibilité de rentrer les restes a dépenser."""

from .date import get_month_name

HTML_HEAD = "<head><meta charset='UTF-8'>\
        <title>Bois Béton Acier</title>\
        <link rel='stylesheet' type='text/css' href=" +\
        '"{{ url_for("static",filename="rad.css") }}' + '"></head><body>'

HTML_TITLE_HEAD = "<body><div id='image'>\
        <img src=\
        'https://dgb.construction/wp-content/uploads/2019/06/dgb.png'>\
        </div><h1>"

HTML_TITLE_BOT = "</h1>"

HTML_TABLE_HEAD = "<table class='table-fill'><thead><tr>"

HTML_TABLE_TITLE_HEAD = "<th class='text-left'>"
HTML_TABLE_TITLE_BOT = "</th>"

HTML_TABLE_BODY_HEAD = "</thead><tbody class='table-hover'>"
HTML_TABLE_ROW_HEAD = "<td class='text-left'>"
HTML_TABLE_ROW_BOT = "</td>"
HTML_TABLE_BODY_BOT = "</tbody></table>"
HTML_BOT = "<input type='submit' id='confirm' value='Confirmer'\
        form='rad'></input></form></body>"


def bab_input(accounting_plan):
    
    file = open("templates/bab.html", "w")
    file.write(HTML_HEAD)
    file.write("<h1>Bois Acier Beton</h1>")
    
    aciers = accounting_plan.loc[accounting_plan["POSTE"] == "ACIERS"]["SOUS POSTE"]
    bois = accounting_plan.loc[accounting_plan["POSTE"] == "BOIS"]["SOUS POSTE"]
    beton = accounting_plan.loc[accounting_plan["POSTE"] == "BETON"]["SOUS POSTE"]

    print(aciers)
    print(bois)
    print(beton)

    file.write("<form action='/bab' method=post id='bab'>")
    file.write(HTML_TABLE_HEAD)
    file.write("<th class='text-left'>Bois</th>\
                <th class='text-left'>M² du mois</th>\
                <th class='text-left'>M² cumulés</th></tr></thead>")

    file.write("<tbody class='table-hover'>")
    for sp in bois:
        file.write("<tr><td class='text-left'>"+sp+"</td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Bois$"+sp+"'></input></td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Bois$"+sp+"'></input></td></tr>")

    file.write("<tr><th class='text-left'>Aciers</th>\
                <th class='text-left'>Dépenses du mois (kg)</th>\
                <th class='text-left'>Dépenses cumulées (kg)</th>\
                <th class='text-left'>Quantité restante (kg)</th>\
                </tr>")

    for sp in aciers:
        file.write("<tr><td class='text-left'>"+sp+"</td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Aciers$"+sp+"'></input></td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Aciers$"+sp+"'></input></td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Aciers$"+sp+"'></input></td></tr>")

    file.write("<tr><th class='text-left'>Béton</th>\
                <th class='text-left'>Quantité du mois (m³)</th>\
                <th class='text-left'>Quantité cumulé (m³)</th>\
                <th class='text-left'>Quantité restante (m³)</th>\
                </tr>")

    for sp in beton:
        file.write("<tr><td class='text-left'>"+sp+"</td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Beton$"+sp+"'></input></td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Beton$"+sp+"'></input></td>")
        file.write("<td class='text-left'><input type='text' form='rad' name='Beton$"+sp+"'></input></td></tr>")

    file.write( "</tbody></table><input type='submit' id='confirm' value='Confirmer' form='bab'></input></form>")
    file.close()
