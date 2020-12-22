from .plan_comptable import *
from .charges import *
import datetime as dt
from .read_file import read_budget
from .postesparent import ParentPoste

class ChantierPoste(ParentPoste):

    def __init__(self,planComptable,dfChantier):
        super.__init__(planComptable)
        self.charges = dfChantier
        for nom in self.nomPostes:
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0

    
    def _calcul_chantier
