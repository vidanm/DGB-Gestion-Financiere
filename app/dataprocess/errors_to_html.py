HTML_HEAD = "\
<!DOCTYPE HTML>\
    <html>\
        <head>\
            <meta charset='UTF-8'>\
            <title>Erreurs</title>\
            <link rel='stylesheet' \
            type='text/css' \
            href=" + '"{{ url_for("static",filename="index.css")}}">' +\
        "</head>\
        <body>\
            <h1> Erreurs </h1>\
            <div id='errors'>"

HTML_FOOT = "</div><div id='passer'>\
                <form id='continuer' method=get action='/rad'>\
                    <input type='submit' value='Continuer quand même'></input>\
                </form><br>"

NON_CRITIC = "<form id='menu' method=get action='/'>\
                    <input type='submit' value='Retour au menu'></input>\
                    </form>"

FOOTER = "</div></body></html>"


def errors_to_html(critic=False):
    output = open("templates/errors.html", "w")
    input_file = open("log.txt", "r")
    output.write(HTML_HEAD)
    for line in input_file.readlines():
        output.write("<p>"+line+"</p>")
    output.write(HTML_FOOT)
    if not critic:
        output.write(NON_CRITIC)
    output.write(FOOTER)
