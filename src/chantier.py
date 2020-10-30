import pandas as pd
import datetime as dt
from poste import *
import os

def ChargesParChantier(dfCharges):
    ''' Sachant que le fichier charges contient les charges de tout les chantiers 
    diférents On va créer une structure de données regroupant les dépenses par 
    chantier '''
    dicChantiers = {}
    for index,value in dfCharges['Section analytique'].iteritems():
        if DansDictionnaire(str(value),dicChantiers):
            dicChantiers[str(value)].append(dfCharges.iloc[[index]])
        else :
            dicChantiers[str(value)] = pd.DataFrame(dfCharges.iloc[[index]])
    
    return dicChantiers

def SupprimeLigneCodeSansPoste(dfCharges,fichier):
    ''' Supprime les lignes dont le numéro de compte n'est associé a aucun
    poste du plan comptable '''
    codesManquants = []
    for index,value in dfCharges['Général'].iteritems():
        if not DansDictionnaire(str(value),dicComptable):
            print("Ligne non prise en compte")
            dfCharges = dfCharges.drop(index=index)
            if value not in codesManquants:
                print("Numero : "+ str(value) + " pas dans le plan comptable")
                codesManquants.append(value)
                EcrisCodeSansPoste(fichier,value)
    return dfCharges

def EcrisCodeSansPoste(fichier,code):
    '''Ecris le code manquant dans un fichier'''
    fichier.write(str(code) + "\n")

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
        row = dicComptable[str(value)].T.squeeze()
        poste = row[0]
        sousPoste = row[1]
        if (poste not in postes):
            postes[poste] = sousPostes.copy()
        if (sousPoste not in postes[poste]):
            postes[poste][sousPoste] = data.copy()
        
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
        #print(poste)
        #print(sousPoste)
        date = dt.date.strftime(dfCharges['Date'][index],'%b/%m/%y')
        postes[poste][sousPoste]["Dépenses de l'année"] += dfCharges['Débit'][index] - dfCharges['Crédit'][index]

dicComptable = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
dfCharges = RecupDfChantier("/home/vidan/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx")


fichier = open("code_manquants.txt","w")
dfCharges = SupprimeLigneCodeSansPoste(dfCharges,fichier)
dicChantiers = ChargesParChantier(dfCharges)
postes = ChargesChantierParPostes(dicComptable,dfCharges)
CalculDepensesChantierParPostes(postes,dicComptable,dfCharges)
fichier.close()
#os.system("libreoffice code_manquants.txt")
