from .charges import *
from .read_file import read_budget
import pandas as pd
import datetime as dt


class Synthese():
    
    def __init__(self,charges):

        self.col = ['CHANTIER','BUDGET','DEP DU MOIS','DEP CUMULEES','PFDC','MARGE THEORIQUE (€)','MARGE THEORIQUE (%)','MARGE BRUTE (€)','MARGE BRUTE (%)']

        self.charges = charges
        self.synthese_annee = pd.DataFrame(None,None,columns=self.col)
        self.synthese_cumul = self.synthese_annee.copy(deep=True)
    
    
    def csv_of_precalculated_chantiers(self,annee,mois):
        chantier_csv = {}
        if (os.path.exists("bibl/"+date)):
            for filename in os.listdir('bibl/'+annee):
                code = filename[0:-7]
                chantier_csv[code] = pd.read_csv("bibl/"+annee+"/"+filename,index_col=0)
        return chantier_csv

    def ajoute_synthese_annee(self,data):
        self.synthese_annee = self.synthese_annee.append(data,ignore_index=True)


    def calcul_synthese_annee(self,mois,annee):
        chantier_names = self.charges.get_chantier_names()
        #2020-06 -> 2020-6 chantier_csv = self.csv_of_precalculated_chantiers(annee,mois)
        for name in chantier_names:
            
            if 'DIV' in name or 'STRUCT' in name or name in chantier_csv.keys:
                continue

            chantier_line = ["",0,0,0,0,0,0,0,0]
            chantier_line[0] = name

            for index,row in self.charges.get_raw_chantier(name).iterrows():
                date = row['Date']
                if (row['Journal'] == 'ACH') and (date.month <= mois) and (date.year == annee):
                    chantier_line[3] += row['Débit'] - row['Crédit']
                    if (date.month == mois):
                        chantier_line[2] += row['Débit'] - row['Crédit']
            
            out = pd.DataFrame([chantier_line],columns=self.col)
            self.ajoute_synthese_annee(out)
        
        self.synthese_annee = self.synthese_annee.set_index("CHANTIER")
        self.ajoute_budget()
        self.synthese_annee = self.synthese_annee.round(2)
        
    

    def ajoute_budget(self):
        dfBudget = read_budget("var/budget.xls")
        chantier_names = self.charges.get_chantier_names()
        print(self.synthese_annee)
        for name in chantier_names:
            if name in dfBudget.columns :
                for index,row in dfBudget.iterrows():
                    #print(name)
                    #print(row[name])
                    print(self.synthese_annee.loc[name])
                    self.synthese_annee.loc[name,"BUDGET"] += row[name]
    
    #def calcul_pfdc(self):
        
    #def calcul_marges(self):
