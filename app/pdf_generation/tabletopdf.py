import locale
from .colors import black,lightwhite,bleu,bleuciel,yellow
from rlextra.graphics.quickchart import QuickChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import os.path
import numpy as np

locale.setlocale(locale.LC_ALL,'en_US.utf8')
script_dir = os.path.dirname(os.path.abspath(__file__))

class PDF():

    def __init__(self,nom):
        """Permets la generation des différents pdf ( synthese / structure etc. )"""
        self.nom = nom
        self.c = canvas.Canvas(nom,pagesize=(A4[1],A4[0]))
        self.logo = os.path.join('images/DGB.jpeg')
        self.__background()
        self.tablestyle = TableStyle([
            ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
            ('GRID', (0,0), (-1,-1), 0.1, black),
            ('FONTSIZE',(0,0),(-1,-1),8),
            ('ALIGN',(0,0),(-1,-1),"CENTER"),
            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            ('BACKGROUND',(0,0),(-1,0),bleuciel),
            ('TEXTCOLOR',(0,0),(-1,0),"BLACK"),
            ('BACKGROUND',(1,1),(-1,-1),"WHITE"),
            ('BACKGROUND',(0,-1),(-1,-1),yellow)
            ])

    def __background(self):
        self.c.setFillColorRGB(1,1,1)
        self.c.rect(0,0,A4[1],A4[0],fill=1)
        self.c.setFillColorRGB(0,0,0)

    def struct_style(self,row_nom):
        style = [
            ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
            ('GRID', (0,0), (-1,-1), 0.1, "BLACK"),
            ('FONTSIZE',(0,0),(-1,-1),6),
            ('ALIGN',(0,0),(-1,-1),"CENTER"),
            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            ('BACKGROUND',(0,0),(-1,0),bleuciel),
            ('TEXTCOLOR',(0,0),(-1,0),"BLACK"),
            ('BACKGROUND',(1,1),(-1,-1),"WHITE"),
            ('BACKGROUND',(0,-1),(-1,-1),yellow),
            ('TOPPADDING',(0,0),(-1,-1),6)
            ]

        for i in row_nom:
            style.append(('BACKGROUND',(0,i),(-1,i),bleu))
            style.append(('TEXTCOLOR',(0,i),(-1,i),bleu))
            style.append(('TEXTCOLOR',(0,i),(0,i),lightwhite))

        return TableStyle(style)

    def draw_header(self):
        self.c.setFillColor(bleu)
        self.c.rect(inch,A4[0]-inch*1.5,A4[1]-2*inch,inch,fill=1)
        self.c.setFillColorRGB(0,0,0)

    def ajoute_total(self,numTable):
        total = [ [0] * 7 ]
        for i in range(1,len(numTable)):
            for j in range(1,len(numTable[0])):
                total[0][j] += numTable[i][j];

        total[0][0] = 'Total'
        numTable.append(total[0])

    def create_bar_syntgraph(self,width,height,synt):
        pfdc = synt["PFDC"].tolist()
        budget = synt["BUDGET"].tolist()
        dep = synt["DEP CUMULEES"].tolist()
        
        d = Drawing(width,height)
        d.add(QuickChart(),name='chart')
        d.chart.height               = height
        d.chart.width                = width
        d.chart.seriesNames          ='PFDC','Budget','Dépenses cumulées'
        d.chart.seriesRelation       = 'sidebyside'
        d.chart.dataLabelsFontSize   = 10
        d.chart.legendFontSize = 10
        d.chart.chartColors = [bleu,bleuciel,yellow]
        d.chart.data                 = [pfdc,budget,dep]
        d.chart.chartType='column'
        d.chart.titleText            = ''
        d.chart.xTitleText           = ''
        d.chart.xAxisFontSize        = 10
        d.chart.xAxisLabelAngle      = 30
        d.chart.yAxisFontSize        = 10
        #d.chart.yAxisLabelAngle      = 30
        d.chart.categoryNames        = synt.index.tolist()
        d.chart.dataLabelsAlignment        = 'bottom'
        #d.chart.pointerLabelMode     = 'leftAndRight'
        d.chart.bgColor              = None
        d.chart.plotColor            = None
        d.chart.titleFontColor       = black
        #d.rotate(90)
        d.drawOn(self.c,inch,inch*0.1)



    def create_bar_gesprevgraph(self,width,height,postes):
        pfdc = []
        budget = []
        dep = []

        for key in postes.categories.keys():
            if key != "GESPREV" and key != "FACTURATION CLIENT":
                pfdc.append(postes.categories[key].iloc[-1]["PFDC"])
                budget.append(postes.categories[key].iloc[-1]["Budget"])
                dep.append(postes.categories[key].iloc[-1]["Dépenses de l'année"])

        d = Drawing(width,height)
        d.add(QuickChart(),name='chart')
        d.chart.height               = height
        d.chart.width                = width
        d.chart.seriesNames          ='PFDC','Budget','Dépenses cumulées'
        d.chart.seriesRelation       = 'sidebyside'
        d.chart.dataLabelsFontSize   = 10
        d.chart.legendFontSize = 10
        d.chart.chartColors = [bleu,bleuciel,yellow]
        d.chart.data                 = [pfdc,budget,dep]
        d.chart.chartType='column'
        d.chart.titleText            = ''
        d.chart.xTitleText           = ''
        d.chart.xAxisFontSize        = 10
        d.chart.xAxisLabelAngle      = 30
        d.chart.yAxisFontSize        = 10
        #d.chart.yAxisLabelAngle      = 30
        d.chart.categoryNames        = list(postes.categories.keys())
        d.chart.dataLabelsAlignment        = 'bottom'
        #d.chart.pointerLabelMode     = 'leftAndRight'
        d.chart.bgColor              = None
        d.chart.plotColor            = None
        d.chart.titleFontColor       = black
        #d.rotate(90)
        d.drawOn(self.c,inch,inch*0.1)

    def eliminate_zeros_add_euros(self,numTable):
        for i in range(1,len(numTable)):
            for j in range(1,len(numTable[0])):
                if (numTable[i][j] == 0):
                    numTable[i][j] = '--'
                else :
                    asStr= str(numTable[i][j])
                    numTable[i][j] = asStr + " €"
                    
        return numTable

    def convert_struct_string(self,numTable):
        for i in range(0,len(numTable)):
            for j in range(0,len(numTable[i])):
                if (type(numTable[i][j]) is float):
                    if (j>2):
                        numTable[i][j] = "{:.2f}".format(numTable[i][j])+" %" if numTable[i][j] != 0 else "/"
                    else:
                        numTable[i][j] = "{:.2f}".format(numTable[i][j])+" €" if numTable[i][j] != 0 else "/"
        return numTable
    


    def add_struct_table(self,dataframe,row_noms,x='center',y='center',size=1):
        dataframe = dataframe.reset_index()
        rowHeights = (len(dataframe)+1)*[11*size]
        rowHeights[0] = 18
        numTable = dataframe.to_numpy().tolist()
        numTable.insert(0,np.array(dataframe.columns.values).tolist())
        numTable = self.convert_struct_string(numTable)
        #self.eliminate_zeros_add_euros(numTable)
        
        t = Table(numTable,rowHeights=rowHeights)
        t.setStyle(self.struct_style(row_noms))
        w,h = t.wrapOn(self.c,0,0)
        
        

        if (x == -1 or x =='center'):
            x=(A4[1]/2)-(w/2)
        if (y == -1 or y == 'center'):
            y=(A4[0]/2)-(h/2)-inch*0.8
        
        t.drawOn(self.c,x,y)

    def add_table(self,dataframe,x=-1,y=-1):
        """Ajoute un tableau a la feuille active. Le coin bas droite est représenté par (x,y)."""
        #TODO Rajouter la colonne des sous postes
        dataframe = dataframe.reset_index()
        rowHeights = (len(dataframe)+1)*[12]
        rowHeights[0] = 20
        numTable = dataframe.to_numpy().tolist()
        numTable.insert(0,np.array(dataframe.columns.values).tolist())
        #self.ajoute_total(numTable)
        #self.eliminate_zeros_add_euros(numTable)

        t = Table(numTable,rowHeights=rowHeights)
        t.setStyle(self.tablestyle)
        w,h = t.wrapOn(self.c,0,0) #Draw Table
        
        #Si la position n'est pas définie par l'utilisateur alors on ecris la table au milieu de la page

        if (x == -1 or x == 'center'):
            x=(A4[1]/2)-(w/2)
        if (y == -1 or y == 'center'):
            y=(A4[0]/2)-(h/2)

        t.drawOn(self.c,x,y)


    def add_sidetitle(self,text):
        self.c.setFillColor("WHITE")
        self.c.drawString(inch*1.1,A4[0]-inch*1.14,text)
        self.c.setFillColor("BLACK")

    def new_page(self,titre,sousTitre):
        """Ecris le titre et le sous titre sur une feuille."""
        self.__background()
        self.draw_header()
        self.c.drawImage(self.logo,A4[1]-inch*2,A4[0]-inch*1.39,width=50,height=50) #Draw Logo
        self.c.setFillColor("WHITE")
        self.c.setFont("Helvetica-Bold",30) #Draw Title
        self.c.drawCentredString(A4[1]/2,A4[0] - inch,titre)

        self.c.setFont("Helvetica-Bold",20) #Draw Subtitle
        self.c.drawCentredString(A4[1]/2,A4[0]-inch*1.3,sousTitre)
    
    def save_page(self):
        """Sauvegarde la feuille active, une nouvelle feuille blanche est sélectionnée."""
        self.c.showPage()


    def save_pdf(self):
        self.c.save()
