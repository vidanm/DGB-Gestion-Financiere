from .basic_operations import is_in_dic

class Charges():
    """S'occupe de traiter le fichier excel contenant toutes les charges. Les méthodes commençant par _ sont des méthodes internes a la classe. Ne pas les utiliser en dehors."""
    
    def __init__(self,charges,planComptable,f):
        """Prends les charges lues par CustomReaderFile(), une instance de la classe PlanComptable(),et un fichier d'ecriture pour les codes manquants."""
        self._dicCharges = charges
        self._dicCharges = self._delete_code_without_poste(planComptable,f)
        self._dicCharges = self._associe_compte_poste(planComptable)
        self._dicChantiers = self._split_by_chantiers()


    def _write_missing_code_in_file(self,f,code):
        """Ecris dans un fichier externe le numéro de code spécifié en argument. C'est utilisé quand un code du fichier charges n'est pas présent dans le plan comptable."""
        f.write(str(code) + "\n")
    

    def _delete_code_without_poste(self,planComptable,f):
        """On elimine les lignes dont le numéro de compte n'est pas spécifié dans le plan comptable"""
        missing_codes = []
        charges = self._dicCharges

        for index,value in self._dicCharges['Général'].iteritems():
           
            if planComptable.get_poste_by_code(str(value)).empty:

                if (int(value/100000) == 7):
                    """Les codes comptables commencant par 7 sont des ventes et doivent
                    toujours être pris en compte en tant que tels."""
                    planComptable.ajoute_code(value,"Vente sans poste","Vente sans sous poste")
                    continue

                charges = charges.drop(index=index)
                
                if value not in missing_codes :
                    print("Numero : "+str(value) + " pas dans le plan comptable")
                    missing_codes.append(value)
                    self._write_missing_code_in_file(f,value)

        return charges


    def _associe_compte_poste(self,planComptable):
        """On associe les numéro de comptes comptable aux postes associés dans le plan comptable."""
        charges = self._dicCharges
        for index,value in self._dicCharges['Général'].iteritems():
            poste = planComptable.get_poste_by_code(str(value))['POSTE'].values[0]
            sousPoste = planComptable.get_poste_by_code(str(value))['SOUS POSTE'].values[0]
            charges.loc[index,'POSTE'] = poste
            charges.loc[index,'SOUS POSTE'] = sousPoste
        
        return charges
    

    def _split_by_chantiers(self):
        """On divise les données des charges dans un dictionnaire utilisant les code de chantier comme clé."""
        dicChantiers = {}
        nomChantiers = []
        for _,row in self._dicCharges.iterrows():
            value = row['Section analytique']
            
            if not is_in_dic(str(value),nomChantiers):
                nomChantiers.append(str(value))
        for nom in nomChantiers:
            dicChantiers[nom] = self._dicCharges.loc[self._dicCharges['Section analytique'] == nom]

        return dicChantiers
    
    
    def get_chantier_names(self):
        """Renvoie tout les noms de chantiers."""
        names = []
        for key in self._dicChantiers:
            names.append(key)
        return names

    def get_with_approximation(self,approx):
        """Renvoie le nom reel en fonction d'une approximation STRUCT -> 20-STRUCT0."""
        names = self.get_chantier_names()
        for name in names:
            if approx in name:    
                return name


    def get_raw_chantier(self,code):
        """Renvoie les données pour un chantier particulier."""
        return self._dicChantiers[code]

    
    def get_struct(self):
        return self._dicChantiers["20-STRUCT0"]
    

    def get_raw_charges(self):
        """Renvoie le tableau de charges."""
        return self._dicCharges
