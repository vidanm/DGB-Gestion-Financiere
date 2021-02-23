from .colors import *
from reportlab.lib.colors import PCMYKColor, Color, CMYKColor, black, red
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String, Line
from reportlab.lib.validators import Auto
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace,Font, registerFont
from reportlab.lib.formatters import DecimalFormatter
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label

class PDBHorizontalBarChart(HorizontalBarChart):
    ''' PFDC DEPENSES BUDGET '''
    def __init__(drawing, width,height,data, categoryNames):
        HorizontalBarChart.__init__(drawing)
        drawing.width = width
        drawing.height = height
        drawing.fillColor = None
        #drawing.reversePlotOrder = 1

        #chart bar
        drawing.groupSpacing = 4
        drawing.barWidth = 5
        drawing.barSpacing = 0
        drawing.bars.fillColor = [bleu,bleuciel,yellow]
        drawing.bars.strokeWidth = 0
        drawing.bars.strokeColor = None
        drawing.barLabels.angle = 0
        drawing.barLabelFormat = DecimalFormatter(2, suffix='%')
        drawing.barLabels.boxAnchor = 'w'
        drawing.barLabels.boxFillColor = None
        drawing.barLabels.boxStrokeColor = None
        drawing.barLabels.dx = 5
        drawing.barLabels.dy = 0
        drawing.barLabels.boxTarget = 'hi'
        drawing.valueAxis.labels.f
        drawing.
        drawing.
