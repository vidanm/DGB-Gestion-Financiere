import os
import pandas as pd
import numpy as np
from .basic_operations import *

class PlanComptable():
    
    

    def get_poste_by_code(self,code):
        '''Renvoie le poste en fonction du code donné'''
        return self.__dfComptable.loc[self.__dfComptable['N° DE COMPTE'].str.contains(code,na=False)]

    
    
    def get_dataframe(self):
        return self.__dfComptable

    

    def ajoute_code(self,code,poste,sous_poste):
        row = pd.DataFrame(np.array([[code,poste,sous_poste]]),
            columns=['N° DE COMPTE','POSTE','SOUS POSTE'])
        self.__dfComptable = self.__dfComptable.append(row,ignore_index=True)


    

    def __init__(self,path):
        self.path = path
        self.__dfComptable = self.__read_comptable()

    

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
        dfCompteSite = dfCompteSite.append(dfCompteStruct,ignore_index=True)
        dfCompteSite['N° DE COMPTE'] = dfCompteSite['N° DE COMPTE'].apply(str)
        
        values = {'SOUS POSTE':'Sous poste non défini'}
        dfCompteSite = dfCompteSite.fillna(value=values)
        return dfCompteSite

