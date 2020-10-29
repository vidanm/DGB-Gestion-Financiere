import pandas as pd
import datetime as dt
from poste import *


def DansDictionnaire(num,dic):
    ''' Vérifie si le code de compte num est bien dans le plan comptable '''
    for key in dic:
        if key == str(num):
            return True
    return False


def ChargesParChantier(dfCharges):
    ''' Sachant que le fichier charges contient les charges de tout les chantiers 
    diférents On va créer une structure de données regroupant les dépenses par 
    chantier '''
    dicChantiers = {}
    for index,value in dfCharges['Section analytique'].iteritems():
        print(value)
        if DansDictionnaire(value,dicChantiers):
            dicChantiers[str(value)].append(dfCharges[[index]])
        else :
            dicChantiers[str(value)] = pd.DataFrame(dfCharges[[index]])
    
    return dicChantiers


def ChargesChantierParPostes(dicComptable,dfCharges):
    ''' Renvoie une structure de données regroupant par chantier, les dépenses 
    et les postes associés aux numéros de compte '''

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

    for index,value in dfCharges['Général'].iteritems():
        if DansDictionnaire(value,dicComptable):
            row = dicComptable[str(value)].T.squeeze()
            poste = row[0]
            sousPoste = row[1]

            if (poste not in postes):
                postes[poste] = sousPostes.copy()
                if (sousPoste not in postes[poste]):
                    postes[poste][sousPoste] = data.copy()
        else :
            #ERREUR LE NUMERO N'EST PAS DANS LE PLAN COMPTABLE
            print("Numero : "+str(value)+" pas dans le plan comptable")
            print("La dépense ne sera pas prise en compte")
            dfCharges.drop(index=index) #On supprime la ligne
    return postes;

def CalculDepensesChantierParPostes(postes,dicComptable,dfCharges):
    '''On va calculer pour tout les mois et on va stocker tout ces mois dans 
    un tableau pour ne pas avoir a refaire l'operation a chaque fois'''
    
    '''On suppose ici qu'on a supprimé les lignes avec des numéros de compte 
    hors plan comptable'''
    for index, value in dfCharges['Général'].iteritems():    
        row = dicComptable[str(value)].T.squeeze()
        poste = row[0]
        sousPoste = row[1]
        print(poste)
        print(sousPoste)
        date = dt.date.strftime(dfCharges['Date'][index],'%b/%m/%y')
        postes[poste][sousPoste]["Dépenses de l'année"] += dfCharges['Débit'][index] - dfCharges['Crédit'][index]

dicComptable,dicComptStruct = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
dfCharges = RecupDfChantier("/home/vidan/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx")
#ChargesParChantier(dfCharges)
postes = ChargesChantierParPostes(dicComptable,dfCharges)
CalculDepensesChantierParPostes(postes,dicComptable,dfCharges)
