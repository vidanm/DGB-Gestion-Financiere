from plan_comptable import *
from basic_operations import *

class Charges():
    
    def __init__(self,path,planComptable,f):
        self.__dicCharges = self.__read_charges(path)
        self.__dicCharges = self.__delete_code_without_poste(planComptable,f)
        self.__dicChantiers = self.__split_by_chantiers()

    def __read_charges(self,path):
        charges = pd.read_excel(path)
        charges = charges.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
        return charges

    def __write_missing_code_in_file(self,f,code):
        f.write(str(code) + "\n")

    def __delete_code_without_poste(self,planComptable,f):
        missing_codes = []
        charges = self.__dicCharges

        for index,value in self.__dicCharges['Général'].iteritems():
            if planComptable.get_poste_by_code(str(value)).empty :
                print("Ligne " + str(index) + " non prise en compte")
                charges = self.__dicCharges.drop(index=index)
                
                if value not in missing_codes :
                    print("Numero : "+str(value) + " pas dans le plan comptable")
                    missing_codes.append(value)
                    self.__write_missing_code_in_file(f,value)
        return charges

    
    def __split_by_chantiers(self):
        
        dicChantiers = {}
        nomChantiers = []
        for index,row in self.__dicCharges.iterrows():
            value = row['Section analytique']
            if not is_in_dic(str(value),nomChantiers):
                nomChantiers.append(str(value))

        for nom in nomChantiers:
            dicChantiers[nom] = self.__dicCharges.loc[self.__dicCharges['Section analytique'] == nom]

        return dicChantiers
    
    def calcul_chantier(self,code):
        return 0

    def get_raw_chantier(self,code):
        return self.__dicChantiers[code]



pc = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")

print(pc.get_poste_by_code('627102'))
print(pc.get_dataframe())
codes_missing = open("missing_numbers.txt","w")
c = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",pc,codes_missing)

