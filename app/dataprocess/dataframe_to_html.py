from .postes_chantier import *
from pandas import Index

HTML_HEAD = "<head><meta charset='UTF-8'><title>Rentrer Reste à dépenser</title><link rel='stylesheet' type='text/css' href="+'"{{ url_for("static",filename="rad.css") }}'+'"></head>'
HTML_TITLE_HEAD = "<body><div id='image'><img src='https://dgb.construction/wp-content/uploads/2019/06/dgb.png'></div><h1>"
HTML_TITLE_BOT = "</h1>"
HTML_TABLE_HEAD = "<table class='table-fill'><thead><tr>"

HTML_TABLE_TITLE_HEAD = "<th class='text-left'>"
HTML_TABLE_TITLE_BOT = "</th>"

HTML_TABLE_BODY_HEAD = "</thead><tbody class='table-hover'>"
HTML_TABLE_ROW_HEAD = "<td class='text-left'>"
HTML_TABLE_ROW_BOT = "</td>"
HTML_TABLE_BODY_BOT = "</tbody></table>"
HTML_BOT = "<input type='submit' id='confirm' form='rad'></input></form></body>"



def convert_single_dataframe_to_html_table(dicPostes,mois,annee,chantier):
    index_rad = 0
    file = open("templates/rad.html","w")

    
    file.write(HTML_HEAD)
    file.write(HTML_TITLE_HEAD)
    file.write("Bilan "+str(chantier)+" | "+str(mois)+" "+str(annee))
    file.write(HTML_TITLE_BOT)

    file.write("<form action='/rad' method=post id='rad'>")
    file.write(HTML_TABLE_HEAD)
    first_df = True
    skip_column = []

    for key in dicPostes:
        dataframe = dicPostes[key]
        
        if (first_df):
            file.write(HTML_TABLE_TITLE_HEAD)
            file.write(key)
            file.write(HTML_TABLE_TITLE_BOT)
            for col in dataframe.columns:
                if ("PFDC" in col.upper()):
                    skip_column.append(dataframe.columns.get_loc(col)+1)
                else:
                    if (col == 'RAD'):
                        input_col = dataframe.columns.get_loc(col)
                    file.write(HTML_TABLE_TITLE_HEAD)
                    file.write(str(col))
                    file.write(HTML_TABLE_TITLE_BOT)
            
            file.write(HTML_TABLE_BODY_HEAD)
            first_df = False
        else :
            file.write(HTML_TABLE_TITLE_HEAD)
            file.write(key)
            file.write(HTML_TABLE_TITLE_BOT)

        for index,row in dataframe.iterrows():
            index_cell = 0
            file.write("<tr>")
            file.write(HTML_TABLE_ROW_HEAD)
            file.write(index)
            file.write(HTML_TABLE_ROW_BOT)
            
            for cell in row:
                index_cell += 1
                if (index_cell not in skip_column):
                    file.write(HTML_TABLE_ROW_HEAD)
                    if (index_cell == input_col+1):
                        id = key+"$"+index
                        file.write("<input type='text' form='rad'")
                        file.write('name="'+id+'">')
                        file.write("</input>")
                    else:
                        file.write(str(cell))
                    file.write(HTML_TABLE_ROW_BOT)
            index_cell = 0
            file.write("</tr>")
        file.write("</br>")

    file.write(HTML_TABLE_BODY_BOT)
    file.write(HTML_BOT)
