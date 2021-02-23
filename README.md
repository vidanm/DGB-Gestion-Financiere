# Logiciel de gestion financière DGB
![DGB LOGO](https://github.com/vidanm/DGB-Gestion/blob/master/images/DGB.jpeg)

https://dgb-gestionfinanciere.herokuapp.com/

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d9c8b09c33b40bb8db12b0d60a397c9)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vidanm/DGB_Gesfin&amp;utm_campaign=Badge_Grade)

## Dépendances
- [Pandas](https://github.com/pandas-dev/pandas)
- [Flask](https://github.com/pallets/flask)
- [Reportlab](https://github.com/MrBitBucket/reportlab-mirror)

## Fonctionnalités

  - Synthèse Chantier
  > Récapitulatif des dépenses par postes et sous postes

  - Bilan Structure
  > Récapitulatif des dépenses de la structure par postes et sous postes

  - Synthèse Globale
  > Récapitulatif des dépenses par chantier sur le mois et l'année 
  > La synthèse globale ne prendra en compte que les chantiers dont la propre synthèse de chantier a déjà été générée.

## Imports des fichiers excel

Les fichiers Excel doivent être importés sous le format .xls et non .xlsx .

Ils doivent respecter le format de nommage suivant : INTITULE-ANNEE.xls
( Exemple : CHARGES-2020.xls )

### Le Plan Comptable
1. Les intitulés de lignes doivent se trouver sur la 1ère colonne pour le section chantier et la 5ème colonne pour la section structure.

2. Les intitulés de colonnes doivent se trouver sur la 2ème ligne.

3. UNE SEULE LIGNE PAR SOUS POSTE ! Pour avoir plusieurs compte pour un sous poste, respecter le format suivant :
`NOM DU SOUS POSTE | NUMERO 1 / NUMERO 2 / NUMERO 3`

### Chantiers / Comptes de charges / Structure
1. Vérifier la présence des champs ‘Journal’ / ‘Général’ / ‘Date’ / ‘Débit’ / ‘Crédit’ / ‘Section analytique’.

2. La section analytique des lignes de charges de la structure doivent comporter 'STRUCT'.

### Budget
1. Les noms des postes et des sous postes doivent impérativement correspondre aux noms donnés dans le plan
comptable. Exemple : "Sous traitant MO" est différent de "Sous traitant Main d'oeuvre"

## Présentation

![HTML Example](https://github.com/vidanm/DGB_Gesfin/blob/master/images/Capture%20d%E2%80%99%C3%A9cran%20de%202021-01-29%2015-53-25.png)
![HTML Example 2](https://github.com/vidanm/DGB_Gesfin/blob/master/images/Capture%20d%E2%80%99%C3%A9cran%20de%202021-01-29%2015-52-55.png)
