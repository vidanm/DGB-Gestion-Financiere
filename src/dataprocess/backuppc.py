import os
import pandas as pd
from basic_operations import *

class PlanComptable():
    
    def get_all_postes(self):
        '''Renvoie un dictionnaire avec les postes en clé et la liste des sous
        postes en définition '''

        postes = {}
        for key in self.__dicComptable:
            row = self.__dicComptable[key].T.squeeze()
            sousPoste = row[1]
            poste = row[0]
            if not is_in_dic(row[0],postes):
                postes[row[0]] = row[1]
            else :
                postes[row[0]].append(row[1])
        return poste

    def get_all_num(self):
        '''Renvoie tout les numéros de postes'''
        num = []
        for key in self.__dicComptable:
            num.append(key)
        return num

    def get_poste_by_code(self,code):
        '''Renvoie le poste en fonction du code donné'''
        if is_in_dic(code,self.__dicComptable):
            row = self.__dicComptable[code].T.squeeze()
            sousPoste = row[1]
            poste = row[0]
            return (poste,sousPoste)
        else:
            return "NOPE"

    def __init__(self,path):
        self.path = path
        self.__dicComptable = self.__read_comptable()

    def __read_comptable(self):
        '''Conversion Excel -> DataFrame pandas'''
        dfCompteSite = pd.read_excel(self.path,header=1,usecols="A:D")
        dfCompteSite[['POSTE']] = dfCompteSite[['POSTE']].fillna(method='ffill')
        dfCompteStruct = pd.read_excel(self.path,header=1,usecols="E:H")
        dfCompteStruct[['POSTE.1']] = dfCompteStruct[['POSTE.1']].fillna(method='ffill')

        #On supprime toutes les lignes avec un sous poste nul
        dfCompteSite = dfCompteSite[pd.notnull(dfCompteSite['N° DE COMPTE'])]
        dfCompteStruct = dfCompteStruct[pd.notnull(dfCompteStruct['N° DE COMPTE.1'])]
        dfCompteStruct = dfCompteStruct.rename(columns={'N° DE COMPTE.1': 'N° DE COMPTE','POSTE.1' : 'POSTE','SOUS POSTE.1' : 'SOUS POSTE'})
        dicSite = self.__traite_donnees(dfCompteSite)
        dicStruct = self.__traite_donnees(dfCompteStruct)
        return merge_two_dict(dicSite,dicStruct)

    def __traite_donnees(self,dfCompte):
        ''' Renvoie un dictionnaire qui associe sous poste etc. aux numéros de compte comme clé '''
        dicComptable = {}
        for index, row in dfCompte.iterrows():
            dfTemp = dfCompte.loc[dfCompte['N° DE COMPTE'] == row['N° DE COMPTE']]
            dfTemp = dfTemp.drop(columns='N° DE COMPTE')

            if ('/' in str(row['N° DE COMPTE'])):
                for num in str(row['N° DE COMPTE']).replace(" ","").split("/"):
                    dicComptable[str(num)] = dfTemp
            else:
                dicComptable[str(row['N° DE COMPTE'])] = dfTemp
        return dicComptable

planC = PlanComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
print(planC.get_poste_by_code('C'))
