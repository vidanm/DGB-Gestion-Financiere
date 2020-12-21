import os
import pandas as pd
import numpy as np
from .basic_operations import *
from .read_file import read_comptable

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
        self.__dfComptable = read_comptable(path)


