from .postesparent import ParentPoste
import pandas as pd

class ChantierPoste(ParentPoste):

    def __init__(self,planComptable,charges,codeChantier):
        """Trie les charges d'un chantier par postes."""
        super(ChantierPoste,self).__init__(planComptable.get_pc_chantier())
        self.charges = charges.get_raw_chantier(codeChantier)
        self.codeChantier = codeChantier
        for nom in self.nomPostes:
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0

    def calcul_chantier(self,mois,annee,dfBudget):
        for _,row in self.charges.iterrows():
            date = row['Date']
            if (date.year == annee):
                super(ChantierPoste,self)._depenses_annee(row)
                if (date.month == mois):
                    super(ChantierPoste,self)._depenses_mois(row)
        self._ajoute_budget_chantier(dfBudget)
        #self.calcul_pfdc_budget()
        #self.calcul_total_chantier(mois)

    def _ajoute_budget_chantier(self,dfBudget):
        """Ajoute le budget dans les cases de postes correspondantes."""

        for _,row in dfBudget.iterrows():
            try :
                self.dicPostes[row['POSTE']].loc[row['SOUS-POSTE'],"Budget"] += round(row[self.codeChantier])
            except :
                raise ValueError("Le couple " + row['POSTE'] + " : " + row['SOUS-POSTE'] + "n'est pas présent dans le plan comptable")

    def ajoute_rad(self,poste,sousposte,rad):
        if rad.replace('.','').isnumeric():
            self.dicPostes[poste].loc[sousposte,"RAD"] = float(rad)

    def calcul_pfdc_budget(self):
        """Calcul le pfdc et l'ecart pfdc budget."""
        for nom in self.nomPostes:
            for _,row in self.dicPostes[nom].iterrows():
                pfdc = row['RAD'] + row["Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,"PFDC"] = pfdc
                self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def ajoute_total_poste(self,nom):
        totalmois = 0
        totalannee = 0
        totalbudget = 0
        totalrad = 0
        totalpfdc = 0
        totalecart = 0
        for index,row in self.dicPostes[nom].iterrows():
            totalannee += self.dicPostes[nom].loc[row.name,"Dépenses de l'année"]
            totalmois += self.dicPostes[nom].loc[row.name,"Dépenses du mois"]
            totalbudget += self.dicPostes[nom].loc[row.name,"Budget"]
            totalrad += self.dicPostes[nom].loc[row.name,"RAD"]
            totalpfdc += self.dicPostes[nom].loc[row.name,"PFDC"]
            totalecart += self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"]

        total = pd.DataFrame(
                {"Dépenses de l'année":[totalannee],
                    "Dépenses du mois":[totalmois],
                    "Budget":[totalbudget],
                    "RAD":[totalrad],
                    "PFDC":[totalpfdc],
                    "Ecart PFDC/Budget":[totalecart]},["TOTAL"])
        self.dicPostes[nom] = self.dicPostes[nom].append(total)

    def calcul_total_chantier(self):
        """Calcul du total des dépenses."""
        for nom in self.nomPostes:
            self.ajoute_total_poste(nom)

    def calcul_ges_prev(self):
        """Calcul la gestion previsionnelle une fois que ttes les autres données ont été calculées."""
        for nom in self.nomPostes:
            if nom != "PRODUITS":
                if self.nomPostes.index(nom) == 0:
                    gesprev = pd.DataFrame(columns=self.dicPostes[nom].columns.copy())
                line = self.dicPostes[nom].iloc[-1]
                line.name = nom
                gesprev = gesprev.append(line,ignore_index=False)

        self.nomPostes.append("GESPREV")
        self.dicPostes["GESPREV"] = gesprev
        self.ajoute_total_poste("GESPREV")

