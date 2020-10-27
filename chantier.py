import pandas as pd
import datetime as dt
from poste import *

def AssocieChantierComptable(dicComptable,dfChantier):
    d = { 
            'Sous Poste' : [],
            'Budget' : [],
            'Dépenses du mois' : [],
            'Dépenses cumulées' : [],
            'RAD' : [],
            'PFDC' : [],
            'PFDC/Budget':[]
        }

    postes = {'MO':d}

    for index,value in dfChantier['Général'].iteritems():
        row = dicComptable[str(value)].T.squeeze()
        print(str(row)+"\n")
        
    return;

dicComptable,dicComptStruct = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")

dfChantier = RecupDfChantier("/home/vidan/Documents/DGB/Resultat_chantier/chantier/19-GP-ROSN.xlsx")

#print(dfChantier)
#print(dfAccountSite)
#print(dfAccountSite[dfAccountSite['N° DE COMPTE'] == 604922]['SOUS POSTE'])
AssocieChantierComptable(dicComptable,dfChantier)

