from .postes_chantier import *
from pandas import Index

HTML_HEAD = "<head><meta charset='UTF-8'><title>Rentrer Reste à dépenser</title><link rel='stylesheet' type='text/css' href="+'"{{ url_for("static",filename="rad.css") }}'+'"></head>'
HTML_TITLE_HEAD = "<body><div class='title'><h1>"
HTML_TITLE_BOT = "</h1></div>"
HTML_TABLE_HEAD = "<table class='table-fill'><thead><tr>"

HTML_TABLE_TITLE_HEAD = "<th class='text-left'>"
HTML_TABLE_TITLE_BOT = "</th>"

HTML_TABLE_BODY_HEAD = "</thead><tbody class='table-hover'>"
HTML_TABLE_ROW_HEAD = "<td class='text-left'>"
HTML_TABLE_ROW_BOT = "</td>"
HTML_TABLE_BODY_BOT = "</tbody></table>"
HTML_BOT = "<button type='submit' id='confirm'>Confirmer</button></body>"



def convert_single_dataframe_to_html_table(dataframe,nomPoste,mois,annee,chantier):
    index_rad = 0
    file = open("templates/rad.html","w")
    
    file.write(HTML_HEAD)
    file.write(HTML_TABLE_HEAD)
    file.write(HTML_TITLE_HEAD)
    file.write("Bilan "+nomPoste+" | "+str(chantier)+" | "+str(mois)+" "+str(annee))
    file.write(HTML_TITLE_BOT)

    for col in dataframe.columns:
        if (col == 'RAD'):
            input_col = dataframe.columns.get_loc(col)

        file.write(HTML_TABLE_TITLE_HEAD)
        file.write(str(col))
        file.write(HTML_TABLE_TITLE_BOT)
    
    file.write(HTML_TABLE_BODY_HEAD)

    for index,row in dataframe.iterrows():
        file.write("<tr>")
        for cell in row:
            index_rad += 1
            file.write(HTML_TABLE_ROW_HEAD)
            if (index_rad == input_col+1):
                file.write("<input type='text'></input>")
            else:
                file.write(str(cell))
            file.write(HTML_TABLE_ROW_BOT)
        index_rad = 0
        file.write("</tr>")

    file.write(HTML_TABLE_BODY_BOT)
    file.write(HTML_BOT)
