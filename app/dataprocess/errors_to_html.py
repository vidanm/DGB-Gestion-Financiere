HTML_HEAD = "\
<!DOCTYPE HTML>\
    <html>\
        <head>\
            <meta charset='UTF-8'>\
            <title>Erreurs</title>\
            <link rel='stylesheet' \
            type='text/css' \
            href="+'"{{ url_for("static",filename="index.css")}}">'+\
        "</head>\
        <body>\
            <h1> Erreurs </h1>\
            <div id='buttons'>"

HTML_FOOT = "\
                <form id='continuer' method=get action='/rad'>\
                    <input type='submit' value='Continuer quand même'></input>\
                </form><br>\
                <form id='menu' method=get action='/'>\
                    <input type='submit' value='Retour au menu'></input>\
                </form>\
            </div>\
        </body>\
    </html>"

def errors_to_html():
    output = open("templates/errors.html","w")
    input_file = open("log.txt","r")
    output.write(HTML_HEAD)
    for line in input_file.readlines():
        output.write("<p>"+line+"</p>")
    output.write(HTML_FOOT)
