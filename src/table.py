from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import PIL.Image
import os.path
import numpy as np
from poste import *
from plan_comptable import *

def background(c):
    c.setFillColorRGB(1,1,1)
    c.rect(0,0,A4[1],A4[0],fill=1)
    c.setFillColorRGB(0,0,0)

script_dir = os.path.dirname(os.path.abspath(__file__))
c = canvas.Canvas("simple_pdf.pdf",pagesize=(A4[1],A4[0]))
im = os.path.join(script_dir,'../images/DGB.jpeg')
background(c)
c.drawImage(im,0,A4[0]-inch*1.41)

plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
codes_missing = open("missing_numbers.txt","w")
cha = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",plan,codes_missing)
post = Postes(plan)
post.calcul_chantier(cha.get_raw_chantier('19-GP-ROSN'),6)
print(post.dicPostes['MO'])
data = post.dicPostes['MATERIELS']

# container for the 'Flowable' objects
elements = []

custom_dark = colors.Color(48/255,48/255,48/255)
custom_lightgray = colors.Color(220/255,220/255,220/255)
custom_white = colors.Color(245/255,245/255,245/255)

rowHeights = (len(data)+1)*[20]
rowHeights[0] = 35

numTable = np.array(data).tolist()
numTable.insert(0,np.array(post.dicPostes['MATERIELS'].columns.values).tolist()) #####
t=Table(numTable,rowHeights=rowHeights)
tablstl = [
        ('FACE',(0,0),(-1,-1),"Helvetica-Bold"),
        ('ALIGN',(0,0),(-1,-1),"CENTER"),
        ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
        ('BACKGROUND',(0,0),(-1,0),custom_dark),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white)
    ]

for i in range(1,len(data)+1):
    if (i%2 == 0):
        tablstl.append(('BACKGROUND',(0,i),(6,i),custom_lightgray))
    else:
        tablstl.append(('BACKGROUND',(0,i),(6,i),custom_white))

t.setStyle(TableStyle(tablstl))

t.wrapOn(c,0,0)
t.drawOn(c,A4[0]/6,A4[1]/4-inch*0.7)
c.setFont("Helvetica-Bold",50)
c.rotate(90)
c.drawCentredString(A4[0]/2,-A4[1]+inch*0.15,"MATERIELS")
c.setFont("Helvetica-Bold",20)
c.drawCentredString(A4[0]/2,-A4[1]+inch*0.8,"AOUT 2020 | 19-GP-ROSN")

c.showPage()
c.save()
