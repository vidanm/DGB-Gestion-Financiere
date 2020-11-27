from .plan_comptable import *
from .basic_operations import *

class Charges():
    '''
    S'occupe de traiter le fichier excel contenant toutes les charges

    Les méthodes commençant par __ sont des méthodes internes a la classe
    Ne pas les utiliser en dehors.
    '''
    
    def __init__(self,path,planComptable,f):
        self.__dicCharges = self.__read_charges(path)
        self.__dicCharges = self.__delete_code_without_poste(planComptable,f)
        self.__dicCharges = self.__associe_chantier_poste(planComptable)
        self.__dicChantiers = self.__split_by_chantiers()

    def __read_charges(self,path):
        '''Associe les données excel aux champs de la classe'''

        charges = pd.read_excel(path)
        charges = charges.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
        charges = charges.fillna(0)
        charges['POSTE'] = ''
        charges['SOUS POSTE'] = ''
        return charges

    def __write_missing_code_in_file(self,f,code):
        '''Ecris dans un fichier externe le numéro de code spécifié en argument.
        C'est utilisé quand un code du fichier charges n'est pas présent dans le
        plan comptable'''
        f.write(str(code) + "\n")

    def __delete_code_without_poste(self,planComptable,f):
        '''On elimine les lignes dont le numéro de compte n'est pas spécifié
        dans le plan comptable'''
        missing_codes = []
        charges = self.__dicCharges

        for index,value in self.__dicCharges['Général'].iteritems():
           
            if planComptable.get_poste_by_code(str(value)).empty:

                if (int(value/100000) == 7):
                    '''Les codes comptables commencant par 7 sont des ventes et doivent
                    toujours être pris en compte en tant que tels'''
                    planComptable.ajoute_code(value,"Vente sans poste","Vente sans sous poste")
                    continue

                print("Ligne " + str(index) + " non prise en compte")
                charges = charges.drop(index=index)
                
                if value not in missing_codes :
                    print("Numero : "+str(value) + " pas dans le plan comptable")
                    missing_codes.append(value)
                    self.__write_missing_code_in_file(f,value)

        return charges

    def __associe_chantier_poste(self,planComptable):
        '''On associe les numéro de comptes comptable aux postes associés dans le        plan comptable'''
        charges = self.__dicCharges
        for index,value in self.__dicCharges['Général'].iteritems():
            poste = planComptable.get_poste_by_code(str(value))['POSTE'].values[0]
            sousPoste = planComptable.get_poste_by_code(str(value))['SOUS POSTE'].values[0]
            charges.loc[index,'POSTE'] = poste
            charges.loc[index,'SOUS POSTE'] = sousPoste
        
        return charges
    
    def __split_by_chantiers(self):
        '''On divise les données des charges dans un dictionnaire utilisant les code        de chantier comme clé'''
        dicChantiers = {}
        nomChantiers = []
        for index,row in self.__dicCharges.iterrows():
            value = row['Section analytique']
            if not is_in_dic(str(value),nomChantiers):
                nomChantiers.append(str(value))
        for nom in nomChantiers:
            dicChantiers[nom] = self.__dicCharges.loc[self.__dicCharges['Section analytique'] == nom]

        return dicChantiers
    
    def get_chantier_names(self):
        names = []
        for key in self.__dicChantiers:
            names.append(key)
        return names

    def get_raw_chantier(self,code):
        '''Renvoie les données pour un chantier particulier'''
        return self.__dicChantiers[code]

    def get_raw_charges(self):
        '''Renvoie le tableau de charges'''
        return self.__dicCharges
