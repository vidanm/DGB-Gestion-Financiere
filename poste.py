""" 
ATTENTION
DANS LE PLAN COMPTABLE SI 2 NUMEROS COMPTABLES SONT ASSOCIES A 2 SOUS POSTE DIFFERENTS
LE PROGRAMME NE FONCTIONNERA PAS 
"""

import os
import pandas as pd


def RecupDictComptable(path):
    '''Recupere le plan comptable et traite les données pour en
    faciliter l'exploitation'''

    dfCompteSite = pd.read_excel(path,header=1,usecols="A:D")
    dfCompteSite[['POSTE']] = dfCompteSite[['POSTE']].fillna(method='ffill')

    dfCompteStruct = pd.read_excel(path,header=1,usecols="E:H")
    dfCompteStruct[['POSTE.1']] = dfCompteStruct[['POSTE.1']].fillna(method='ffill')

    #On supprime toutes les lignes avec un sous poste nul
    dfCompteSite = dfCompteSite[pd.notnull(dfCompteSite['N° DE COMPTE'])]
    dfCompteStruct = dfCompteStruct[pd.notnull(dfCompteStruct['N° DE COMPTE.1'])]
    dfCompteStruct = dfCompteStruct.rename(columns={'N° DE COMPTE.1': 'N° DE COMPTE','POSTE.1' : 'POSTE','SOUS POSTE.1' : 'SOUS POSTE'})
    
    '''On itere sur le plan, on instancie une dataframe pour chaque numéro de compte
    différent, Que l'on stocke dans un dictionnaire '''

    dicComptable = {}
    
    for index, row in dfCompteSite.iterrows():
        #Traitement de la partie gauche du plan
        dfTemp = dfCompteSite.loc[dfCompteSite['N° DE COMPTE'] == row['N° DE COMPTE']]
        dfTemp = dfTemp.drop(columns='N° DE COMPTE')

        if ('/' in str(row['N° DE COMPTE'])):
            for num in str(row['N° DE COMPTE']).replace(" ","").split("/"):
                dicComptable[str(num)] = dfTemp
        else: 
            dicComptable[str(row['N° DE COMPTE'])] = dfTemp

    for index, row in dfCompteStruct.iterrows():
        #Traitement de la partie droite du plan
        dfTemp = dfCompteStruct.loc[dfCompteStruct['N° DE COMPTE'] == row['N° DE COMPTE']]
        dfTemp = dfTemp.drop(columns='N° DE COMPTE')

        if ('/' in str(row['N° DE COMPTE'])):
            for num in str(row['N° DE COMPTE']).replace(" ","").split("/"):
                dicComptable[str(num)] = dfTemp
        else: 
            dicComptable[str(row['N° DE COMPTE'])] = dfTemp

    return dicComptable


def RecupDfChantier(path):
    chantier = pd.read_excel(path)
    chantier = chantier.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
    return chantier

