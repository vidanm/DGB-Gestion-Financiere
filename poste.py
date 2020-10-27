import os
import pandas as pd


def RecupDictComptable(path):
    
    dfAccountSite = pd.read_excel(path,header=1,usecols="A:D")
    dfAccountSite[['POSTE']] = dfAccountSite[['POSTE']].fillna(method='ffill')

    dfAccountStruct = pd.read_excel(path,header=1,usecols="E:H")
    dfAccountStruct[['POSTE.1']] = dfAccountStruct[['POSTE.1']].fillna(method='ffill')

    #On supprime toutes les lignes avec un sous poste nul
    dfAccountSite = dfAccountSite[pd.notnull(dfAccountSite['N° DE COMPTE'])]
    dfAccountStruct = dfAccountStruct[pd.notnull(dfAccountStruct['N° DE COMPTE.1'])]

    """
    
    renvoie un tuple contenant les 2 dictionnaires de poste comptables
    Celui de la structure et celui des chantiers

    """

    #On itere sur le plan, on instancie une dataframe pour chaque numéro de compte
    #différent,
    #Que l'on stocke dans un dictionnaire
    dicPosteSite = {}
    dicPosteStruct = {}
    for index, row in dfAccountSite.iterrows():
        dfTemp = dfAccountSite.loc[dfAccountSite['N° DE COMPTE'] == row['N° DE COMPTE']]
        dfTemp = dfTemp.drop(columns='N° DE COMPTE')

        if ('/' in str(row['N° DE COMPTE'])):
            for num in str(row['N° DE COMPTE']).replace(" ","").split("/"):
                dicPosteSite[num] = dfTemp
        else: 
            dicPosteSite[str(row['N° DE COMPTE'])] = dfTemp

    for index, row in dfAccountStruct.iterrows():
        dfTemp = dfAccountStruct.loc[dfAccountStruct['N° DE COMPTE.1'] == row['N° DE COMPTE.1']]
        dfTemp = dfTemp.drop(columns='N° DE COMPTE.1')
               
        if ('/' in str(row['N° DE COMPTE.1'])):
            for num in str(row['N° DE COMPTE.1']).replace(" ","").split("/"):
                dicPosteSite[num] = dfTemp
        else: 
            dicPosteSite[row['N° DE COMPTE.1']] = dfTemp

    return (dicPosteSite,dicPosteStruct)


def RecupDfChantier(path):
    chantier = pd.read_excel(path)
    chantier = chantier.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°','Section analytique'])
    return chantier

