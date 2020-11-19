import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import PIL.Image
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))

def hello(c):
    c.translate(inch, inch)
    c.setFont("Times-Roman",25)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.drawString(0.3*inch,inch,"Hello World")
    print(os.path.join(script_dir,'DGB.jpeg'))
    im = PIL.Image.open(os.path.join(script_dir, 'DGB.jpeg'))
    c.drawImage(os.path.join(script_dir,"DGB.jpeg"),-inch,inch*9.3)

c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
