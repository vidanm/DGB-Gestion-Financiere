"Dual Bar charts on one canvas."
from reportlab.lib.colors import PCMYKColor, black
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.formatters import DecimalFormatter
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label

class SpecialHorizontalBarChart(HorizontalBarChart):
    def __init__(drawing, _fontName, _fontSize, color):
        """ BarChart from reportlab gallery """
        HorizontalBarChart.__init__(drawing)
        drawing.x                       = 45
        drawing.y                       = 24
        drawing.width                   = 52
        drawing.height                  = 154
        drawing.fillColor               = None
        drawing.reversePlotOrder = 1

        # chart bars
        drawing.barLabels.fontName      = _fontName
        drawing.barLabels.fontSize      = _fontSize
        drawing.groupSpacing            = 4
        drawing.barWidth                = 5
        drawing.barSpacing              = 0
        drawing.bars.fillColor          = color
        drawing.bars.strokeWidth        = 0
        drawing.bars.strokeColor        = None
        drawing.barLabels.angle         = 0
        drawing.barLabelFormat          = DecimalFormatter(2, suffix='%')
        drawing.barLabels.boxAnchor     ='w'
        drawing.barLabels.boxFillColor  = None
        drawing.barLabels.boxStrokeColor= None
        drawing.barLabels.dx            = 5
        drawing.barLabels.dy            = 0
        drawing.barLabels.boxTarget     = 'hi'
        # apply colours
        #for i, _ in enumerate(drawing.data ): drawing.bars[i].fillColor = color
        # value axis
        drawing.valueAxis.labels.fontName       = _fontName
        drawing.valueAxis.labels.fontSize       = _fontSize
        #drawing.valueAxis.strokeDashArray       = (5,0)
        drawing.valueAxis.visibleAxis          = False
        drawing.valueAxis.visibleGrid           = False
        drawing.valueAxis.visibleTicks          = False
        #drawing.valueAxis.gridStrokeDashArray   = (0,1,0)
        #drawing.valueAxis.valueStep             = 200
        #drawing.valueAxis.strokeWidth           = 0.25
        #drawing.valueAxis.gridStrokeWidth       = 0.25
        #drawing.valueAxis.gridStrokeDashArray   = (1,1,1)
        #drawing.valueAxis.avoidBoundFrac        = 0#1#0.5
        #drawing.valueAxis.rangeRound            ='both'
        #drawing.valueAxis.gridStart             = 13
        #drawing.valueAxis.gridEnd               = 342
        #drawing.valueAxis.labelTextFormat        = DecimalFormatter(1, suffix=None, prefix=None)
        #drawing.valueAxis.labels.boxAnchor       = 'autoy'
        drawing.valueAxis.forceZero              = True
        #drawing.valueAxis.labels.boxAnchor       = 'e'
        #drawing.valueAxis.labels.dx              = 0
        drawing.valueAxis.visibleLabels          = 0
        # category axis
        drawing.categoryAxis.labels.fontName = _fontName
        drawing.categoryAxis.labels.fontSize = _fontSize+0.5
        drawing.categoryAxis.strokeDashArray        = (5,0)
        #drawing.categoryAxis.gridStrokeDashArray = (1,1,1)
        drawing.categoryAxis.visibleGrid         = False
        drawing.categoryAxis.visibleTicks        = False # hidding the ticks remove the label
        drawing.categoryAxis.tickLeft            = 0    # a workaround is to set the tick length
        drawing.categoryAxis.tickRight           = 0    # to zero.
        drawing.categoryAxis.strokeWidth         = 0.25
        drawing.categoryAxis.labelAxisMode       ='low'
        drawing.categoryAxis.labels.textAnchor   ='end'
        drawing.categoryAxis.labels.fillColor    = black
        drawing.categoryAxis.labels.angle        = 0
        #drawing.chart.categoryAxis.tickShift          = 1
        drawing.categoryAxis.labels.dx           = -5
        drawing.categoryAxis.labels.dy           = 0
        #drawing.categoryAxis.strokeDashArray     = (0,1,0)
        drawing.categoryAxis.labels.boxAnchor    = 'e'
        drawing.categoryAxis.labels.leading      = 5
        #drawing.categoryAxis.labels.dx           = -10
        #drawing.categoryAxis.labels.dy           = -5
        drawing.categoryAxis.reverseDirection    = 1
        drawing.categoryAxis.joinAxisMode='left'
        drawing.data = [[10.9, 10.84, 15.99, 18.75, 14.75, 9.1300000000000008, 9.2100000000000009, 5.21, 2.3500000000000001, 2.8799999999999999, 0.0], [8.9900000000000002, 11.210000000000001, 11.859999999999999, 17.0, 12.59, 11.4, 12.279999999999999, 4.7199999999999998, 4.4699999999999998, 5.4900000000000002, 0.0]]
        drawing.categoryAxis.categoryNames       =[ 'Consumer\nStaples', 'Consumer\nDiscretionary', 'Energy', 'Financials', 'Health Care', 'Industrials', 'Information\nTechnology', 'Materials', 'Telecomm.\nServices', 'Utilities', 'Other']

class BarChart11(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------
        Dual Bar charts on one canvas. Bar charts are just another widget in ReportLab's library
        you could add as many of them as you want in your drawing:

        - The two charts share one legend.

        This chart was built with our [Diagra](http://www.reportlab.com/software/diagra/) solution.

        Not the kind of chart you looking for? Go [up](..) for more charts, or to see different types of charts click on [ReportLab Chart Gallery](/chartgallery/).
    '''
    def __init__(self,width=264,height=190,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        # font
        self._fontNameBook = 'Helvetica'
        self._fontNameDemi = 'Helvetica'
        self._fontSize = 5
        # colours
        color = PCMYKColor(0,51, 100, 1)
        # chart
        self._add(self,SpecialHorizontalBarChart(self._fontNameBook, self._fontSize,color),name='chart1',validate=None,desc=None)
        self.chart1.bars[0].fillColor = PCMYKColor(100,60,0,50,alpha=85)
        self.chart1.bars[1].fillColor = PCMYKColor(66,13,0,22,alpha=85)
        # chart 2
        '''self._add(self,SpecialHorizontalBarChart(self._fontNameBook, self._fontSize,color),name='chart2',validate=None,desc=None)
        self.chart2.x = 182
        self.chart2.data = [[0.85999999999999999, 5.2599999999999998, 2.1899999999999999, 0.94999999999999996, 8.4600000000000009, 11.220000000000001, 3.25, 3.2799999999999998, 8.7400000000000002, 14.4, 41.380000000000003], [0.050000000000000003, 3.0299999999999998, 0.26000000000000001, 0.01, 1.3799999999999999, 3.2599999999999998, 0.01, 0.0, 0.0, 92.0, 0.0]]
        self.chart2.categoryAxis.categoryNames       = ['Asset Backed\nSecurities', 'US\nTreasury/Agency', 'Commercial\nMortgage Backed', 'High Yield\nCorporate', 'Investment Grade\nCorporate', 'Mortgage Backed', 'Govt Emerging\nMarkets', 'Non US Currency', 'TIPS', 'Cash', 'Other']
        self.chart2.bars[0].fillColor = PCMYKColor(100,60,0,50,alpha=85)
        self.chart2.bars[1].fillColor = PCMYKColor(100,0,90,50,alpha=85)'''
        # legend
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.fontName         = self._fontNameBook
        self.legend.fontSize         = self._fontSize+0.5
        self.legend.boxAnchor        = 'nw'
        self.legend.x                = 3
        self.legend.y                = 18
        self.legend.deltax           = 0
        self.legend.deltay           = 10
        self.legend.columnMaximum    = 3
        self.legend.alignment        = 'right'
        self.legend.strokeWidth      = 0
        self.legend.strokeColor      = None
        self.legend.autoXPadding     = 0
        self.legend.dx               = 4
        self.legend.dy               = 4
        self.legend.variColumn       = True
        self.legend.dxTextSpace      = 4
        self.legend.variColumn       = True
        #self.legend.subCols.minWidth = self.chart1.width/2
        #self.legend.colorNamePairs   = Auto(obj=self.chart1)
        self.legend.colorNamePairs   = [(PCMYKColor(100,60,0,50,alpha=85), u'PFDC'), (PCMYKColor(66,13,0,22,alpha=85), u'Depenses'), (PCMYKColor(100,0,90,50,alpha=85), u'Budget')]
        self.legend.deltay           = 5
        self.legend.y                = 20
        #self.chart1.categoryAxis.reverseDirection     = 1
        #self.chart1.reversePlotOrder = 1
        # label1
        self._add(self,Label(),name='label1',validate=None,desc=None)
        self.label1.boxAnchor      = 'nw'
        self.label1.x              = 0 #self.chart1.x
        self.label1.y              = self.height
        self.label1.fontName       = self._fontNameDemi
        self.label1.fontSize       = 8
        self.label1._text          = 'Synthese'
        # label2
        '''self._add(self,Label(),name='label2',validate=None,desc=None)
        self.label2.x              = self.chart2.x-self.chart1.x
        self.label2.y              = self.height
        self.label2.fontName       = self._fontNameDemi
        self.label2.fontSize       = 8
        self.label2.angle          = 0
        #self.label2.boxAnchor = 's'
        self.label2.textAnchor     ='middle'
        self.label2.boxAnchor      = 'nw'
        self.label2._text          = 'Fixed Income Composition'
'''
if __name__=="__main__": #NORUNTESTS
    BarChart11().save(formats=['pdf'],outDir='.',fnRoot=None)
