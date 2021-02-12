from .charges import *
import pandas as pd
import datetime as dt
import codecs

class Synthese():
    
    def __init__(self,charges):

        self.col = ['CHANTIER','BUDGET','DEP DU MOIS','DEP CUMULEES','PFDC','MARGE THEORIQUE (€)','MARGE THEORIQUE (%)','MARGE BRUTE (€)','MARGE BRUTE (%)']

        self.charges = charges
        self.synthese_annee = pd.DataFrame(None,None,columns=self.col)
        self.synthese_cumul = self.synthese_annee.copy(deep=True)
    
    
    def precalc_pfdc(self,mois,annee):
        '''Rajout des csv des chantiers dont la synthese a deja ete calcules'''
        chantier_csv = {}
        date = str(annee) + "-" + (str(mois) if len(str(mois)) == 2 else "0"+str(mois))
        if (os.path.exists("bibl/"+date)):
            for filename in os.listdir('bibl/'+date):
                code = filename[0:-7]
                with open("bibl/"+date+"/"+filename,'rb') as file:
                    chantier_csv[code] = file.read()

        return chantier_csv

    def ajoute_synthese_annee(self,data):
        self.synthese_annee = self.synthese_annee.append(data,ignore_index=True)

    def calcul_synthese_annee(self,mois,annee,budget):
        
        chantier_names = self.charges.get_chantier_names()
        chantier_csv = self.precalc_pfdc(mois,annee)
        
        for name in chantier_names:
            
            if 'DIV' in name or 'STRUCT' in name:
                continue

            chantier_line = ["",0,0,0,0,0,0,0,0]
            chantier_line[0] = name
            
            if name in chantier_csv.keys():
                chantier_line[4] = round(float(chantier_csv[name]),2)

            for index,row in self.charges.get_raw_chantier(name).iterrows():
                date = row['Date']
                if (row['Journal'] == 'ACH') and (date.month <= mois) and (date.year == annee):
                    chantier_line[3] += row['Débit'] - row['Crédit']
                    if (date.month == mois):
                        chantier_line[2] += row['Débit'] - row['Crédit']
            
            out = pd.DataFrame([chantier_line],columns=self.col)
            self.ajoute_synthese_annee(out)
        
        self.synthese_annee = self.synthese_annee.set_index("CHANTIER")
        self.ajoute_budget(budget)
        self.calcul_marges()
        self.synthese_annee = self.synthese_annee.round(2)
        
    

    def ajoute_budget(self,budget):
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            if name in budget.columns :
                for index,row in budget.iterrows():
                    self.synthese_annee.loc[name,"BUDGET"] += row[name]
    
    def calcul_marges(self):
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            if 'DIV' in name or 'STRUCT' in name:
                continue
            
            budget = self.synthese_annee.loc[name,"BUDGET"]
            pfdc = self.synthese_annee.loc[name,"PFDC"]
            depcum = self.synthese_annee.loc[name,"DEP CUMULEES"]
            

            print(type(budget))
            print(type(pfdc))

            if budget != 0:
                self.synthese_annee.loc[name,"MARGE THEORIQUE (€)"] =  round(budget - pfdc,2)
                self.synthese_annee.loc[name,"MARGE THEORIQUE (%)"] = round(pfdc*100/budget,2)
                self.synthese_annee.loc[name,"MARGE BRUTE (€)"] =  round(budget-depcum,2)
                self.synthese_annee.loc[name,"MARGE BRUTE (%)"] = round(depcum*100/budget,2)

    def calcul_tableau_ca(chiffreAffaire):
        pass
