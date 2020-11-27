import sys
import locale
import calendar
sys.path.append("/home/vidan/Documents/DGB/Gesfin/src")
import front.pdf.colors as cl
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import PIL.Image
import os.path
import numpy as np
from dataprocess.plan_comptable import *
from dataprocess.poste import *

locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
script_dir = os.path.dirname(os.path.abspath(__file__))

class PDFCharges():

    def __background(self,c):
        c.setFillColorRGB(1,1,1)
        c.rect(0,0,A4[1],A4[0],fill=1)
        c.setFillColorRGB(0,0,0)
    
    def __init__(self,nomPdf,nomChantier,mois,annee):
        self.mois = mois
        self.annee = annee
        self.nomChantier = nomChantier
        self.c = canvas.Canvas(nomPdf,pagesize=(A4[1],A4[0]))
        self.logo = os.path.join(script_dir,'../../../images/DGB.jpeg')
        self.postes = None
        self.__background(self.c)
        self.__calcul_donnees(nomChantier,mois,annee)

    def __calcul_donnees(self,nomChantier,mois,annee):
        plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
        codes_missing = open("missing_numbers.txt","w")
        charges = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",plan,codes_missing)
        self.postes = Postes(plan)
        self.postes.calcul_chantier(charges.get_raw_chantier(nomChantier),mois,annee)
        
    def round_numtable(self,numTable):
        for i in range (1,len(numTable)):
            for j in range (1,len(numTable[0])):
                if (numTable[i][j] == 0):
                    numTable[i][j] = '-'
                else :
                    numTable[i][j] = round(numTable[i][j],2)
        return numTable

    def __format_table(self,poste,data):
        '''Formate des données dataframe en une données numpy
        exploitable par reportlab'''
        rowHeights = (len(data)+1)*[20]
        rowHeights[0] = 35
        numTable = data.to_numpy().tolist()
        numTable.insert(0,np.array(self.postes.dicPostes[poste].columns.values).tolist())
        numTable[0].insert(0,"Sous-poste")
        numTable = self.round_numtable(numTable)
        return Table(numTable,rowHeights=rowHeights)
    
    def __define_table_style(self,table,data):
        '''Définis comment va être affiché le tableau donné en argument 
        sur le pdf'''
        tabstl = [
                ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
                ('ALIGN',(0,0),(-1,-1),"CENTER"),
                ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
                ('BACKGROUND',(0,0),(-1,0),cl.dark),
                ('TEXTCOLOR',(0,0),(-1,0),cl.lightwhite),
                ('BACKGROUND',(1,1),(-1,-1),cl.lightgrey)
            ]

        table.setStyle(TableStyle(tabstl))
        return table


    def __genere_poste_pdf(self,poste):
        '''Genere le pdf pour un poste particulier'''
        data = self.postes.dicPostes[poste].reset_index()
        t = self.__format_table(poste,data)
        t = self.__define_table_style(t,data)
        return t
        
    def genere_pdf(self):
        for poste in self.postes.dicPostes:
            self.__background(self.c)
            self.c.drawImage(self.logo,0,A4[0]-inch*1.41)
            t = self.__genere_poste_pdf(poste)
            w,h = t.wrapOn(self.c,0,0)
            t.drawOn(self.c,(A4[1]/2)-(w/2),(A4[0]/2)-(h/2))
            self.c.setFont("Helvetica-Bold",30)
            #self.c.rotate(90)
            self.c.drawCentredString(A4[1]/2,A4[0] - inch,str(poste))
            self.c.setFont("Helvetica-Bold",20)
            self.c.drawCentredString(A4[1]/2,A4[0] - inch *1.3,calendar.month_name[self.mois] + " " + str(self.annee) + " | " + self.nomChantier )
            self.c.showPage()
        self.c.save()
    
#pdf = PDFCharges("DGB.pdf","19-GP-ROSN",6,2020)
#pdf.genere_pdf()

