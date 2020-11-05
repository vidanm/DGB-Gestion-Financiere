from plan_comptable import *

class Postes():
    def __init__(self,planComptable):
        pc = planComptable.get_dataframe()
        nomPostes = []
        self.dicPostes = {}
        for index,row in pc.iterrows():
            value = row['POSTE']
            if not is_in_dic(str(value),nomPostes):
                nomPostes.append(str(value))

        for nom in nomPostes:
            self.dicPostes[nom] = pc.loc[pc['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','EX.','N° DE COMPTE','EX. '])
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['Depenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0

    

plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
post = Postes(plan)
print(post.dicPostes['MO'])
