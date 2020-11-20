from .plan_comptable import *
from .basic_operations import *

class Charges():
    
    def __init__(self,path,planComptable,f):
        self.__dicCharges = self.__read_charges(path)
        self.__dicCharges = self.__delete_code_without_poste(planComptable,f)
        self.__dicCharges = self.__associe_chantier_poste(planComptable)
        self.__dicChantiers = self.__split_by_chantiers()

    def __read_charges(self,path):
        charges = pd.read_excel(path)
        charges = charges.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
        charges = charges.fillna(0)
        charges['POSTE'] = ''
        charges['SOUS POSTE'] = ''
        return charges

    def __write_missing_code_in_file(self,f,code):
        f.write(str(code) + "\n")

    def __delete_code_without_poste(self,planComptable,f):
        missing_codes = []
        charges = self.__dicCharges

        for index,value in self.__dicCharges['Général'].iteritems():
            if planComptable.get_poste_by_code(str(value)).empty :
                print("Ligne " + str(index) + " non prise en compte")
                charges = charges.drop(index=index)
                
                if value not in missing_codes :
                    print("Numero : "+str(value) + " pas dans le plan comptable")
                    missing_codes.append(value)
                    self.__write_missing_code_in_file(f,value)

        return charges

    def __associe_chantier_poste(self,planComptable):
        charges = self.__dicCharges
        for index,value in self.__dicCharges['Général'].iteritems():
            poste = planComptable.get_poste_by_code(str(value))['POSTE'].values[0]
            sousPoste = planComptable.get_poste_by_code(str(value))['SOUS POSTE'].values[0]
            charges.loc[index,'POSTE'] = poste
            charges.loc[index,'SOUS POSTE'] = sousPoste
        
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
        
    def get_raw_chantier(self,code):
        return self.__dicChantiers[code]


