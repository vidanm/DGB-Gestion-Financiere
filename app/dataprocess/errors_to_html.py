HTML_HEAD = "\
<!DOCTYPE HTML>\
    <html>\
        <head>\
            <meta charset='UTF-8'>\
            <title>Erreurs</title>\
            <link rel='stylesheet' \
            type='text/css' \
            href="                   + '"{{ url_for("static",filename="index.css")}}">' +\
        "</head>\
        <body>\
            <h1> Erreurs </h1>\
            <div id='errors'>"

HTML_BODY = "</div><div id='passer'>"\

HTML_ACTION_START = "<form id='continuer' method=get action='"

HTML_ACTION_END = "'>"

HTML_FOOT = "<input type='submit' value='Continuer quand même'></input>\
        </form><br>"

NON_CRITIC = "<form id='menu' method=get action='/'>\
                    <input type='submit' value='Retour au menu'></input>\
                    </form>"

FOOTER = "</div></body></html>"


def errors_to_html(action="/", critic=False):
    output = open("templates/errors.html", "w")
    input_file = open("log.txt", "r")
    output.write(HTML_HEAD)
    for line in input_file.readlines():
        output.write("<p>" + line + "</p>")
    output.write(HTML_BODY)
    output.write(HTML_ACTION_START)
    output.write(action)
    output.write(HTML_ACTION_END)
    output.write(HTML_FOOT)
    if not critic:
        output.write(NON_CRITIC)
    output.write(FOOTER)
