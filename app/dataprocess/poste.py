'''OBSOLETE ???'''

from .read_file import read_budget
from .basic_operations import is_in_dic
import pandas as pd

class Postes():
    

    def __init__(self,planComptable,charges,codeChantier):
        pc = planComptable.get_dataframe()
        self.codeChantier = codeChantier
        self.dfBudget = read_budget("/home/vidan/Documents/DGB/Resultat_chantier/Prevision/Budget.xlsx")
        self.nomPostes = []
        self.dicPostes = {}
        for index,row in pc.iterrows():
            value = row['POSTE']
            if not is_in_dic(str(value),self.nomPostes):
                self.nomPostes.append(str(value))

        for nom in self.nomPostes:
            self.dicPostes[nom] = pc.loc[pc['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','EX.','N° DE COMPTE','EX. '])
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['Dépenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0
            self.dicPostes[nom]['%CA MOIS'] = 0
            self.dicPostes[nom]['%CA Cumul'] = 0
            self.dicPostes[nom] = self.dicPostes[nom].set_index('SOUS POSTE')
    
    

    def _depenses_mois(self,row):
        '''Rajoute la dépense de la ligne row dans la case dépenses du mois'''
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses du mois"] += round(row['Débit'] - row['Crédit'],2)
        return 0

    

    def _depenses_annee(self,row):
        '''Rajoute la dépense de la ligne row dans la case dépenses de l'année'''
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses de l'année"] += round(row['Débit'] - row['Crédit'],2)
        return 0

    

    def calcul_chantier(self,dfChantier,mois,annee):
        ''' Calcul les dépenses du mois et de l'année pour le chantier'''
    
        

        for index,row in dfChantier.iterrows():
            date = row['Date']
            if (date.year == annee):
        
                self._depenses_annee(row)
                if (date.month == mois):
                    self._depenses_mois(row)
        #self._calcul_total_chantier(mois)

    def calcul_structure(self,dfStructure,mois,annee):
        for index,row in dfStructure.iterrows():
            date = row['Date']
            if (date.year == annee):
                self._depenses_annee(row)
                if (date.month == mois):
                    self._depenses_mois(row)

    

    def _ajoute_budget_chantier(self,dfBudget):
        '''Ajoute le budget dans les cases de postes correspondantes'''
        for index,row in dfBudget.iterrows():
            self.dicPostes[row['POSTE']].loc[row['SOUS-POSTE'],"Budget"] += round(row[self.codeChantier])

        return 0

    """ OBSOLETE ? 
    def _ajoute_chiffre_affaire(self,mois,annee):
        ca = ChiffreAffaire(self.charges)
        ca_mois = ca.calcul_ca_mois(mois,annee)
        ca_annee = ca.calcul_ca_annee(annee)
        for nom in self.nomPostes:
            for index,row in self.dicPostes[nom].iterrows():
                depenses_mois = self.dicPostes[nom].loc[row.name,'Dépenses du mois']
                depenses_cumul = self.dicPostes[nom].loc[row.name,"Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,'%CA MOIS'] = depenses_mois / ca_mois
                self.dicPOstes[nom].loc[row.name,'%CA Cumul'] = depenses_cumul / ca_annee
    """

    def calcul_pfdc_budget(self):
        '''Calcul le pfdc et l'ecart pfdc budget'''
        for nom in self.nomPostes:
            for index,row in self.dicPostes[nom].iterrows():
                print(row)
                pfdc = row['RAD'] + row["Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,"PFDC"] = round(pfdc)
                self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"] = row['Budget'] - pfdc
        self._ajoute_budget_chantier(self.dfBudget)



    def round_2dec_df(self):
        '''Arrondi tout les nombres à 2 chiffres après la virgule'''
        for nom in self.nomPostes:
            self.dicPostes[nom] = self.dicPostes[nom].round(2)


    def get_postes_names(self): 
        return self.nomPostes



    def _calcul_total_chantier(self,mois):
        '''Calcul du total des dépenses'''
        totalmois = 0
        totalannee = 0
        for poste in self.dicPostes:
            for sousPoste in poste:
                totalannee += round(self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses de l'année"],2)
                totalmois += round(self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses du mois"],2)
        total = pd.DataFrame([[0,totalmois,totalannee,0,0,0]])
        self.dicPostes.append(total)

