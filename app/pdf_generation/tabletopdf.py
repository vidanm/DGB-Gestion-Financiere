import locale
from .colors import *
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import PIL.Image
import os.path
import numpy as np

locale.setlocale(locale.LC_ALL,'fr_FR.utf8')
script_dir = os.path.dirname(os.path.abspath(__file__))

class TablePDF():
    
    def __init__(self,nom):
        self.nom = nom
        self.c = canvas.Canvas(nom,pagesize=(A4[1],A4[0]))
        #self.logo = os.path.join('../../images/DGB.jpeg')
        self.__background()
        self.tablestyle = TableStyle([
            ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
            ('ALIGN',(0,0),(-1,-1),"CENTER"),
            ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            ('BACKGROUND',(0,0),(-1,0),dark),
            ('TEXTCOLOR',(0,0),(-1,0),lightwhite),
            ('BACKGROUND',(1,1),(-1,-1),lightgrey)
            ])

    def __background(self):
        self.c.setFillColorRGB(1,1,1)
        self.c.rect(0,0,A4[1],A4[0],fill=1)
        self.c.setFillColorRGB(0,0,0)

    def new_page(self,titre,sousTitre,dataframe):
        rowHeights = (len(dataframe))*[20]
        rowHeights[0] = 35
        t = Table(dataframe.to_numpy().tolist(),rowHeights=rowHeights)
        t.setStyle(self.tablestyle)
        #TODO Rajouter la colonne des sous postes
        
        self.__background()
        #self.c.drawImage(self.logo,0,A4[0]-inch*1.41) #Draw Logo
        w,h = t.wrapOn(self.c,0,0) #Draw Table
        t.drawOn(self.c,(A4[1]/2)-(w/2),(A4[0]/2)-(h/2))

        self.c.setFont("Helvetica-Bold",30) #Draw Title
        self.c.drawCentredString(A4[1]/2,A4[0] - inch,titre) 

        self.c.setFont("Helvetica-Bold",20) #Draw Subtitle
        self.c.drawCentredString(A4[1]/2,A4[0]-inch*1.3,sousTitre)
        self.c.showPage()

    def save_pdf(self):
        self.c.save()
