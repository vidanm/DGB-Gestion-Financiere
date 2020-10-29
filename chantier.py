import pandas as pd
import datetime as dt
from poste import *

MOIS
ANNEE

def AssocieChantierComptable(dicComptable,dfChantier):
    data = { 
            'Budget' : "",
            'Dépenses du mois' : 0,
            "Dépenses de l'année" : 0,
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

def CalculDepenses(postes,dicComptable,dfChantier):
    '''On va calculer pour tout les mois et on va stocker tout ces mois dans un tableau pour ne pas avoir
    a refaire l'operation a chaque foi'''
    for index, value in dfChantier['Général'].iteritems():
        row = dicComptable[str(value)].T.squeeze()
        poste = row[0]
        sousPoste = row[1]
        date = dt.strptime(dfChantier['Date'][index],'%b/%-m/%y')
        
    
        postes[poste][sousPoste]["Dépenses de l'année"] += dfChantier['Débit'][index] - dfChantier['Crédit'][index]



dicComptable,dicComptStruct = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
dfChantier = RecupDfChantier("/home/vidan/Documents/DGB/Resultat_chantier/chantier/19-GP-ROSN.xlsx")

AssocieChantierComptable(dicComptable,dfChantier)
