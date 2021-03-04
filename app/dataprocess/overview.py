import pandas as pd
import numpy as np
import os

class Synthese():

    def __init__(self,charges):
        """Calcule la synthese sur l'année de toutes les dépenses de tout les chantiers."""
        self.col = ['CHANTIER','BUDGET',"CA MOIS",'DEP DU MOIS',"MARGE MOIS","CA CUMUL",'DEP CUMULEES',"MARGE A FIN DE",'PFDC',"MARGE FDC"]

        self.charges = charges
        self.synthese_annee = pd.DataFrame(None,None,columns=self.col)
        self.synthese_cumul = self.synthese_annee.copy(deep=True)

        self.total_depenses_cumul = 0
        self.total_depenses_mois = 0
   
    
    def precalc_pfdc(self,mois,annee):
        """Rajout des csv des chantiers dont la synthese a deja ete calcules."""
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
        """Calcul de la synthese des dépenses d'une année en omettant la structure."""
        chantier_names = self.charges.get_chantier_names()
        chantier_csv = self.precalc_pfdc(mois,annee)
        
        for name in chantier_names:
            
            if 'DIV' in name or 'STRUCT' in name:
                continue

            chantier_line = ["",0,0,0,0,0,0,0,0,0]
            chantier_line[0] = name
            if name in chantier_csv.keys():
                chantier_line[4] = round(float(chantier_csv[name]),2)

            for _,row in self.charges.get_raw_chantier(name).iterrows():
                #On itere sur toutes les actions d'un chantier particulier
                date = row['Date']
                if (row['Journal'] == 'ACH') and (date.month <= mois) and (date.year == annee):
                    #Une action est une dépense si son champ journal est 'ACH'
                    chantier_line[3] += row['Débit'] - row['Crédit']
                    if (date.month == mois):
                        #Le calcul des dépenses prends en compte les avoirs
                        chantier_line[2] += row['Débit'] - row['Crédit']

            out = pd.DataFrame([chantier_line],columns=self.col)
            self.ajoute_synthese_annee(out)
        
        self.synthese_annee = self.synthese_annee.set_index("CHANTIER")
        self.ajoute_budget(budget)
        self.calcul_marges()
        self.synthese_annee = self.synthese_annee.round(2)
        self._calcul_total()

    def ajoute_budget(self,budget):
        """Ajoute les données dans la colonne budget de la synthèse."""
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            if name in budget.columns :
                for _,row in budget.iterrows():
                    self.synthese_annee.loc[name,"BUDGET"] += row[name]
    
    def calcul_marges(self):
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            if 'DIV' in name or 'STRUCT' in name:
                continue
            
            budget = self.synthese_annee.loc[name,"BUDGET"]
            pfdc = self.synthese_annee.loc[name,"PFDC"]
            depcum = self.synthese_annee.loc[name,"DEP CUMULEES"]
            
            if budget != 0:
                self.synthese_annee.loc[name,"MARGE THEORIQUE (€)"] =  round(budget - pfdc,2)
                self.synthese_annee.loc[name,"MARGE THEORIQUE (%)"] = round(pfdc*100/budget,2)
                self.synthese_annee.loc[name,"MARGE BRUTE (€)"] =  round(budget-depcum,2)
                self.synthese_annee.loc[name,"MARGE BRUTE (%)"] = round(depcum*100/budget,2)
    
    def _calcul_total(self):
        self.total_depenses_cumul = round(self.synthese_annee['DEP CUMULEES'].sum(),2)
        self.total_depenses_mois = round(self.synthese_annee['DEP DU MOIS'].sum(),2)
    
    def calcul_tableau_ca(self,camois,cacumul):
        """Doit etre appele apres le calcul de la synthese et le calcul du total. Se charge de mettre en forme le tableau du chiffre d'affaire."""
        camois = round(camois,2)
        cacumul = round(cacumul,2)
        self.total_ca_marge = pd.DataFrame(np.array([[camois,self.total_depenses_mois,camois-self.total_depenses_mois,round(100*(self.total_depenses_mois/camois),2)],[cacumul,self.total_depenses_cumul,round(cacumul-self.total_depenses_cumul,2),round(100*(self.total_depenses_cumul/cacumul),2)]]),columns=["CA","Depenses","Marge brute","Marge brute %"])
        s = pd.Series(["Mois","Année"])
        self.total_ca_marge = self.total_ca_marge.set_index(s)
        print(self.total_ca_marge)
