from reportlab.lib.formatters import DecimalFormatter
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label

def SyntheseChart():
    hb = HorizontalBarChart()
    hb.barLabels = ["Label 1","Label 2","Label 3"]
    hb.barWidth = 5
    hb.barSpacing = 2
    hb.x = 45
    hb.y = 45
    hb.width = 50
    hb.height = 150
    hb.fillColor = None
    hb.data [[110,11,1164,558,56,210],[45,655,234,12,102,458],[4567,845,32,12,456,849]]
    hb.save("hello.pdf")
