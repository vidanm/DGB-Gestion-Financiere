import pandas as pd
import datetime as dt
from poste import *

def AssocieChantierComptable(dicComptable,dfChantier):
    data = { 
            'Budget' : "",
            'Dépenses du mois' : 0,
            'Dépenses cumulées' : 0,
            'RAD' : 0,
            'PFDC' : 0,
            'PFDC/Budget':0
        }
    
    sousPostes = {}
    postes = {}

    for index,value in dfChantier['Général'].iteritems():
        row = dicComptable[str(value)].T.squeeze()
        poste = row[0]
        sousPoste = row[1]

        if (poste not in postes):
            postes[poste] = sousPostes.copy()
            if (sousPoste not in postes[poste]):
                postes[poste][sousPoste] = data.copy()

    return postes;


dicComptable,dicComptStruct = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
dfChantier = RecupDfChantier("/home/vidan/Documents/DGB/Resultat_chantier/chantier/19-GP-ROSN.xlsx")

AssocieChantierComptable(dicComptable,dfChantier)
