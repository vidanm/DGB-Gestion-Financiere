import os
import pandas as pd

def RecupDictComptable(path):
    
    """ renvoie un tuple contenant les 2 dictionnaires de poste comptables
    Celui de la structure et celui des chantiers """

    dfAccountSite = pd.read_excel(path,header=1,usecols="A:D")
    dfAccountSite[['POSTE']] = dfAccountSite[['POSTE']].fillna(method='ffill')

    dfAccountStruct = pd.read_excel(path,header=1,usecols="E:H")
    dfAccountStruct[['POSTE.1']] = dfAccountStruct[['POSTE.1']].fillna(method='ffill')

    #On supprime toutes les lignes avec un sous poste nul
    dfAccountSite = dfAccountSite[pd.notnull(dfAccountSite['SOUS POSTE'])]
    dfAccountStruct = dfAccountStruct[pd.notnull(dfAccountStruct['SOUS POSTE.1'])]

    #On itere sur le plan, on instancie une dataframe pour chaque poste différent
    #Que l'on stocke dans un dictionnaire
    dicPosteSite = {}
    dicPosteStruct = {}
    prevPoste = ""
    for index, row in dfAccountSite.iterrows():
        if prevPoste != row['POSTE']:
            dfTemp = dfAccountSite.loc[dfAccountSite['POSTE'] == row['POSTE']]
            dfTemp = dfTemp.drop(columns='POSTE')
            #On enleve la colonne poste pour éviter la répétition
            dicPosteSite[row['POSTE']] = dfTemp
            prevPoste = row['POSTE']

    for index, row in dfAccountStruct.iterrows():
        if prevPoste != row['POSTE.1']:
            dfTemp = dfAccountStruct.loc[dfAccountStruct['POSTE.1'] == row['POSTE.1']]
            dfTemp = dfTemp.drop(columns='POSTE.1')
            dicPosteStruct[row['POSTE.1']] = dfTemp
            prevPoste = row['POSTE.1']

    return (dicPosteSite,dicPosteStruct)

