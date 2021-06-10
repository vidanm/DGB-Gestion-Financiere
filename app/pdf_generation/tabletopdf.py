import locale
from .colors import black, lightwhite, bleu, bleuciel, yellow
from rlextra.graphics.quickchart import QuickChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from .style import Style
from .index_letters import index_default_table, index_marge_fdc,\
        index_marge_a_avancement, index_synthese,\
        index_marge_a_avancement_cumul, index_synthese_annee
import os.path

locale.setlocale(locale.LC_ALL, 'en_US.utf8')
script_dir = os.path.dirname(os.path.abspath(__file__))


class PDF():
    def __init__(self, nom):
        """Permets la generation des différents pdf
        ( synthese / structure etc )."""
        self.nom = nom
        self.c = canvas.Canvas(nom, pagesize=(A4[1], A4[0]))
        self.logo = os.path.join('images/DGB.jpeg')
        self.__background()

    def __background(self):
        self.c.setFillColorRGB(1, 1, 1)
        self.c.rect(0, 0, A4[1], A4[0], fill=1)
        self.c.setFillColorRGB(0, 0, 0)

    def struct_style(self, row_nom):
        style = [('FACE', (0, 0), (-1, -1), "Helvetica-Bold"),
                 ('GRID', (0, 0), (-1, -1), 0.1, "BLACK"),
                 ('FONTSIZE', (0, 0), (-1, -1), 6),
                 ('ALIGN', (0, 0), (-1, -1), "CENTER"),
                 ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                 ('BACKGROUND', (0, 0), (-1, 0), bleuciel),
                 ('TEXTCOLOR', (0, 0), (-1, 0), "BLACK"),
                 ('BACKGROUND', (1, 1), (-1, -1), "WHITE"),
                 ('BACKGROUND', (0, -1), (-1, -1), yellow),
                 ('TOPPADDING', (0, 0), (-1, -1), 6)]

        for i in row_nom:
            style.append(('BACKGROUND', (0, i), (-1, i), bleu))
            style.append(('TEXTCOLOR', (0, i), (-1, i), bleu))
            style.append(('TEXTCOLOR', (0, i), (0, i), lightwhite))

        return TableStyle(style)

    def draw_header(self):
        self.c.setFillColor(bleu)
        self.c.rect(inch, A4[0] - inch * 1.5, A4[1] - 2 * inch, inch, fill=1)
        self.c.setFillColorRGB(0, 0, 0)

    def ajoute_total(self, numTable):
        # Vérifier utilité
        total = [[0] * 7]
        for i in range(1, len(numTable)):
            for j in range(1, len(numTable[0])):
                total[0][j] += numTable[i][j]

        total[0][0] = 'Total'
        numTable.append(total[0])

    def create_bar_syntgraph(self, width, height, synt):
        pfdc = synt["PFDC"].tolist()
        budget = synt["BUDGET"].tolist()
        dep = synt["DEP CUMULEES"].tolist()

        d = Drawing(width, height)
        d.add(QuickChart(), name='chart')
        d.chart.height = height
        d.chart.width = width
        d.chart.seriesNames = 'PFDC', 'Budget', 'Dépenses cumulées'
        d.chart.seriesRelation = 'sidebyside'
        d.chart.dataLabelsFontSize = 10
        d.chart.legendFontSize = 10
        d.chart.chartColors = [bleu, bleuciel, yellow]
        d.chart.data = [pfdc, budget, dep]
        d.chart.chartType = 'column'
        d.chart.titleText = ''
        d.chart.xTitleText = ''
        d.chart.xAxisFontSize = 10
        d.chart.xAxisLabelAngle = 30
        d.chart.yAxisFontSize = 10
        # d.chart.yAxisLabelAngle = 30
        d.chart.categoryNames = synt.index.tolist()
        d.chart.dataLabelsAlignment = 'bottom'
        # d.chart.pointerLabelMode = 'leftAndRight'
        d.chart.bgColor = None
        d.chart.plotColor = None
        d.chart.titleFontColor = black
        # d.rotate(90)
        d.drawOn(self.c, inch, inch * 0.1)

    """
    A deplacer dans graphe.py

    def create_bar_gesprevgraph(self, width, height, postes):
        pfdc = []
        budget = []
        dep = []

        for key in postes.categories.keys():
            if key != "GESPREV" and key != "FACTURATION CLIENT":
                if key == "DIVERS":
                    pfdc.append(0)
                    budget.append(0)
                else:
                    pfdc.append(postes.categories[key].iloc[-1]["PFDC"])
                    budget.append(postes.categories[key].iloc[-1]["Budget"])
                dep.append(
                        postes.categories[key].iloc[-1]["Dépenses cumulées"]
                        )

        d = Drawing(width, height)
        d.add(QuickChart(), name='chart')
        d.chart.height = height
        d.chart.width = width
        d.chart.seriesNames = 'PFDC', 'Budget', 'Dépenses cumulées'
        d.chart.seriesRelation = 'sidebyside'
        d.chart.dataLabelsFontSize = 10
        d.chart.legendFontSize = 10
        d.chart.chartColors = [bleu, bleuciel, yellow]
        d.chart.data = [pfdc, budget, dep]
        d.chart.chartType = 'column'
        d.chart.titleText = ''
        d.chart.xTitleText = ''
        d.chart.xAxisFontSize = 10
        d.chart.xAxisLabelAngle = 30
        d.chart.yAxisFontSize = 10
        # d.chart.yAxisLabelAngle = 30
        d.chart.categoryNames = list(postes.categories.keys())
        d.chart.dataLabelsAlignment = 'bottom'
        # d.chart.pointerLabelMode     = 'leftAndRight'
        d.chart.bgColor = None
        d.chart.plotColor = None
        d.chart.titleFontColor = black
        # d.rotate(90)
        d.drawOn(self.c, inch*0.3, inch*0.05)
    """

    def add_legend(self, text, x=-1, y=-1, size=9):

        self.c.setFont("Helvetica", size)  # Draw Title
        self.c.setFillColor("BLACK")
        self.c.drawString(x, y, text)

    def add_table(self,
                  dataframe,
                  x=-1,
                  y=-1,
                  tableHeight=-1,
                  indexName="Poste",
                  title=None,
                  noIndexLine=False,
                  coloring=False,
                  total=True,
                  letters='default',
                  custom_style=[]):
        """Ajoute un tableau a la feuille active.

        Le coin bas droite est représenté par (x,y)."""
        dataframe = dataframe.reset_index()
        numTable = dataframe.to_numpy().tolist()
        indexes = dataframe.columns.values.tolist()

        numTable.insert(0, indexes)
        tablestyle = Style(numTable, tableHeight, total)

        if (numTable[0][0] == "index"):
            numTable[0][0] = indexName

        if noIndexLine:
            self.change_index_names(letters, numTable, axis=1)
        else:
            self.change_index_names(letters, numTable, axis=0)

        if title is not None:
            lst = [i for i in range(len(numTable[0]) - 1)]
            numTable.insert(0, lst)
            numTable[0][0] = title
            if noIndexLine:
                tablestyle.delete_index_line()
            else:
                tablestyle.add_title_style()

            tablestyle.add_custom_style(
                ('FACE', (0, 1), (-1, 1), "Helvetica-Bold"))
            tablestyle.add_custom_style(
                ('BACKGROUND', (0, 1), (-1, 1), bleuciel))

        for i in range(len(numTable)):
            for j in range(len(numTable[i])):
                numTable[i][j] = str(numTable[i][j])

        if coloring:
            tablestyle.add_coloring(numTable)

        for i in custom_style:
            tablestyle.add_custom_style(i)

        t = Table(numTable, rowHeights=tablestyle.get_rowheights())
        t.setStyle(TableStyle(tablestyle.get_style()))
        w, h = t.wrapOn(self.c, 0, 0)  # Draw Table

        # Si la position n'est pas définie par l'utilisateur
        # alors on ecris la table au milieu de la page

        if (x == -1 or x == 'center'):
            x = (A4[1] / 2) - (w / 2)
        else:
            x = (x) - (w / 2)

        if (y == -1 or y == 'center'):
            y = (A4[0] / 2) - (h / 2)
        else:
            y = y - (h / 2)

        t.drawOn(self.c, x, y)

    def add_sidetitle(self, text):
        self.c.setFillColor("WHITE")
        self.c.setFont("Helvetica-Bold", 20)  # Draw Title
        self.c.drawString(inch * 1.1, A4[0] - inch * 1.14, text)
        self.c.setFillColor("BLACK")

    def new_page(self, titre, sousTitre):
        """Ecris le titre et le sous titre sur une feuille."""
        self.__background()
        self.draw_header()
        self.c.drawImage(self.logo,
                         A4[1] - inch * 2,
                         A4[0] - inch * 1.39,
                         width=50,
                         height=50)  # Draw Logo
        self.c.setFillColor("WHITE")
        self.c.setFont("Helvetica-Bold", 30)  # Draw Title
        self.c.drawCentredString(A4[1] / 2, A4[0] - inch, titre)
        self.c.setFont("Helvetica-Bold", 20)  # Draw Subtitle
        self.c.drawCentredString(A4[1] / 2, A4[0] - inch * 1.3, sousTitre)

    def save_page(self):
        """Sauvegarde la feuille active,

        une nouvelle feuille blanche est sélectionnée."""
        self.c.showPage()

    def save_pdf(self):
        self.c.save()

    def change_index_names(self, new_index, table, axis=0):
        """ axis = 0 -> rows
            1 -> columns """

        if new_index == 'default':
            new_index = index_default_table
        elif new_index == 'marge_a_avancement':
            new_index = index_marge_a_avancement
        elif new_index == 'marge_a_avancement_cumul':
            new_index = index_marge_a_avancement_cumul
        elif new_index == 'marge_fdc':
            new_index = index_marge_fdc
        elif new_index == 'globale':
            new_index = index_synthese
        elif new_index == 'globale_annee':
            new_index = index_synthese_annee
        else:
            return

        if not axis:
            for j in range(len(table[0])):
                if table[0][j] in new_index.keys():
                    table[0][j] = new_index[table[0][j]]
        else:
            for i in range(len(table)):
                if table[i][0] in new_index.keys():
                    table[i][0] = new_index[table[i][0]]
        return table
