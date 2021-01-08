
# Logiciel de gestion financière DGB
![DGB LOGO](https://github.com/vidanm/DGB-Gestion/blob/master/images/DGB.jpeg)

### Dépendances
- Python
- Pandas
- Flask
- Reportlab

### Fonctionnalités

#### Synthèse Chantier
###### Récapitulatif des dépenses par postes et sous postes

#### Bilan Structure
##### Récapitulatif des dépenses de la structure par postes et sous postes

#### Synthèse Globale
###### Récapitulatif des dépenses par chantier sur le mois et l'année
La synthèse globale ne prendra en compte que les chantiers dont la propre synthèse de chantier a déjà été générée.

### Instructions de bonne utilisation

#### Le Plan Comptable
- Les intitulés de lignes doivent se trouver sur la 1ère colonne pour le section chantier et la 5ème colonne pour la section structure
- Les intitulés de colonnes doivent se trouver sur la 2ème ligne

#### Chantiers / Comptes de charges / Structure
- Vérifier la présence des champs ‘Journal’ / ‘Général’ / ‘Date’ / ‘Débit’ / ‘Crédit’ / ‘Section analytique’
- La section analytique des lignes de charges de la structure doivent comporter 'STRUCT'

#### Budget
- Les noms des postes et des sous postes doivent impérativement correspondre aux noms donnés dans le plan
comptable. Exemple : "Sous traitant MO" est différent de "Sous traitant Main d'oeuvre"


## Présentation
### HTML
![HTML Example](https://github.com/vidanm/DGB-Gestion/blob/master/images/htmlExample.png)

### Reportlab
![Reportlab Example](https://github.com/vidanm/DGB-Gestion/blob/master/images/Materiels.png)
