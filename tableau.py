from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
import pandas as pd

class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        horHeaders = []
        for i,key in enumerate(self.data):
            horHeaders.append(key)
            for j, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(str(item))
                self.setItem(j, i, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

 
def main(args):
    chantier = pd.read_excel("~/Documents/DGB/Resultat_chantier/chantier/19-GP-ROSN.xlsx")
    chantier = chantier.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°','Section analytique'])
    app = QApplication(args)
    table = TableView(chantier, 315, 7)
    table.setStyleSheet("QHeaderView::section { border: 1px dotted light-grey}")
    table.show()
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)
    print(a)
