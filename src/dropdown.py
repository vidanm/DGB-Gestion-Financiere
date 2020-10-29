import sys

from PyQt5 import QtCore, QtWidgets


def create_menu(d, menu):
    if isinstance(d, list):
        for e in d:
            create_menu(e, menu)
    elif isinstance(d, dict):
        for k, v in d.items():
            sub_menu = QtWidgets.QMenu(k, menu)
            menu.addMenu(sub_menu)
            create_menu(v, sub_menu)
    else:
        action = menu.addAction(d)
        action.setIconVisibleInMenu(False)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        d = [{"Nouveau": ["Bilan Chantier", "Bilan Structure", "Synthese","Gestion previsionnelle","Masse salariale"]},
                {"Importer Feuille.." : ["Chantier","Structure","Plan Comptable","Budget"]},
                "Ouvrir...",
                {"Récemments Ouverts" : ["NULL"]},
                "Exporter",
                { "Exporter sous.." : ["pdf","xlsx","csv"]}
                ]

        menu = QtWidgets.QMenu(self)
        create_menu(d, menu)

        button = QtWidgets.QPushButton()
        button.setMenu(menu)
        button.setText("Fichier");
        #menu.triggered.connect(lambda action: button.setText(action.text()))
        
        lay = QtWidgets.QHBoxLayout(self)
        lay.addWidget(button)
        lay.addStretch()

        self.resize(640, 480)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
