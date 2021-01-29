import locale

from .colors import *
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

import PIL.Image
import os.path
import numpy as np

locale.setlocale(locale.LC_ALL,'en_US.utf8')
script_dir = os.path.dirname(os.path.abspath(__file__))

class PDF():
    
    def __init__(self,nom):
        self.nom = nom
        self.c = canvas.Canvas(nom,pagesize=(A4[1],A4[0]))
        self.logo = os.path.join('images/DGB.jpeg')
        self.__background()
        self.tablestyle = TableStyle([
            ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
            ('GRID', (0,0), (-1,-1), 0.1, colors.black),
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
            ('LINEABOVE', (0,1), (-1,-1), 0.1, colors.black),
            ('FONTSIZE',(0,0),(-1,-1),8),
            ('ALIGN',(0,0),(-1,-1),"CENTER"),
            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            ('BACKGROUND',(0,0),(-1,0),bleuciel),
            ('TEXTCOLOR',(0,0),(-1,0),"BLACK"),
            ('BACKGROUND',(1,1),(-1,-1),"WHITE"),
            ('BACKGROUND',(0,-1),(-1,-1),yellow)
            ]

        for i in row_nom:
            style.append(('BACKGROUND',(0,i),(-1,i),'BLACK'))
            style.append(('TEXTCOLOR',(0,i),(0,i),lightwhite))

        return TableStyle(style)

    def new_page_synthese(self,titre,sousTitre,dataframe):
        return 0

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
    
    def create_bar_graph(self):
        '''d = Drawing(A4[0],A4[1])
        bar = VerticalBarChart()
        bar.x = 0
        bar.y = 50
        bar.width = 500
        bar.height = 500
        data = [[1,2,3,None,None,None,5,10,5,2,6,8,3,5],
                [10,5,2,6,8,3,5,10,5,2,6,8,3,5],
                [5,7,2,8,8,2,5,10,5,2,6,8,3,5],
                [2,10,2,1,8,9,5,10,5,2,6,8,3,5],
                ]
        bar.data = data
        bar.barWidth = 100
        bar.barSpacing = 20
        bar.groupSpacing = 50
        bar.categoryAxis.categoryNames = ['2015','2016','2017',
                                          '2018','2019','2020',
                                          '2021','2022','2023',
                                          '2024','2025','2026',
                                          '2027','2028']
        bar.bars[0].fillColor = lightgrey
        bar.bars[1].fillColor = lightwhite
        bar.bars[2].fillColor = lightgrey
        bar.bars.fillColor = dark
        d.add(bar,'')
        d.drawOn(self.c,0,0)
        '''

    def eliminate_zeros_add_euros(self,numTable):
        point = 0
        for i in range(1,len(numTable)):
            for j in range(1,len(numTable[0])):
                if (numTable[i][j] == 0):
                    numTable[i][j] = '--'
                else :
                    asStr= str(numTable[i][j])
                    numTable[i][j] = asStr + " €"
                        
        return numTable

    def add_struct_table(self,dataframe,row_noms,x='center',y='center'):
        dataframe = dataframe.reset_index()
        rowHeights = (len(dataframe)+1)*[12]
        rowHeights[0] = 20
        numTable = dataframe.to_numpy().tolist()
        numTable.insert(0,np.array(dataframe.columns.values).tolist())
        #self.eliminate_zeros_add_euros(numTable)
        
        t = Table(numTable,rowHeights=rowHeights)
        t.setStyle(self.struct_style(row_noms))
        w,h = t.wrapOn(self.c,0,0)
        
        

        if (x == -1 or x =='center'):
            x=(A4[1]/2)-(w/2)
        if (y == -1 or y == 'center'):
            y=(A4[0]/2)-(h/2)

        t.drawOn(self.c,x,y)

    def add_table(self,dataframe,x=-1,y=-1):
        """Ajoute un tableau a la feuille active. Le coin bas droite
        est représenté par (x,y)"""
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
        
        ''' Si la position n'est pas définie par l'utilisateur
        alors on ecris la table au milieu de la page '''
        if (x == -1 or x == 'center'):
            x=(A4[1]/2)-(w/2)
        if (y == -1 or y == 'center'):
            y=(A4[0]/2)-(h/2)

        t.drawOn(self.c,x,y)

    def add_barplot(self,dataframe,x=-1,y=-1):
        return 0   

    def add_sidetitle(self,text):
        self.c.setFillColor("WHITE")
        self.c.drawString(inch*1.1,A4[0]-inch*1.14,text)
        self.c.setFillColor("BLACK")

    def new_page(self,titre,sousTitre):
        '''Ecris le titre et le sous titre sur une feuille'''
        self.__background()
        self.draw_header()
        self.c.drawImage(self.logo,A4[1]-inch*2,A4[0]-inch*1.39,width=50,height=50) #Draw Logo
        self.c.setFillColor("WHITE")
        self.c.setFont("Helvetica-Bold",30) #Draw Title
        self.c.drawCentredString(A4[1]/2,A4[0] - inch,titre) 

        self.c.setFont("Helvetica-Bold",20) #Draw Subtitle
        self.c.drawCentredString(A4[1]/2,A4[0]-inch*1.3,sousTitre)
    
    def save_page(self):
        '''Sauvegarde la feuille active, 
        une nouvelle feuille blanche est sélectionnée'''
        self.c.showPage()


    def save_pdf(self):
        self.c.save()
