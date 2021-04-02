# DGB Construction | Gestion Financière

![DGB LOGO](https://github.com/vidanm/DGB-Gestion/blob/master/images/DGB.jpeg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d9c8b09c33b40bb8db12b0d60a397c9)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vidanm/DGB_Gesfin&amp;utm_campaign=Badge_Grade)

## Installation

Aucune installation requise, le programme est disponible [ici](https://dgb-gestionfinanciere.herokuapp.com/)


## Utilisation

Le programme nécessite plusieurs fichiers pour générer les synthèses, qu'il faudra importer via l'outil import.   
Ils sont :
1. Le plan comptable [ *Champ PlanComptable de l'outil d'imports.* ]
2. Une extraction de un ou plusieurs chantiers [ *Champ Charges* ]
3. **Optionnel** Le budget des différents chantiers [ *Champ Budget* ]
4. **Optionnel** La masse salariale [ *Champ MasseSalariale* ]

La structure attendue des différents fichiers est définie dans [Structure](##Structure).

**Dû a la structure complexe du fichier de masse salariale, le temps d'éxécution de l'importation peut être long.
Éviter d'importer Charges et Masse Salariale en même temps**

## Structure

Les fichiers excel doivent être importés sous le format .xls et non .xlsx .

### Plan comptable
![Example Plan](https://i.ibb.co/MsZhghm/screenshot.png)
1.  Les intitulés de postes doivent se trouver sur la 1ère colonne pour le section chantier et la 5ème colonne pour la section structure.
2.  Les noms de colonnes doivent se trouver sur la 2e ligne.
3.  **Une seule ligne par sous poste !** Pour avoir plusieurs compte pour un sous poste, respecter le format suivant :

`NOM DU SOUS POSTE | NUMERO 1 / NUMERO 2 / NUMERO 3`

### Extractions chantiers
![Example extraction](https://i.ibb.co/1Jm39y7/screenshot.png)
1.  Vérifier la présence des champs ‘Journal’ / ‘Général’ / ‘Date’ / ‘Débit’ / ‘Crédit’ / ‘Section analytique’.
2.  Le nom ( *La section analytique* ) des charges qui concernent les dépenses de la structure doivent comporter 'STRUCT'.

### Budget
Les noms des postes et des sous postes doivent **obligatoirement** correspondre aux noms donnés dans le plan
comptable. Exemple : "Sous traitant MO" est différent de "Sous traitant Main d'oeuvre"

### Masse salariale
![Example Masse Salariale](https://i.ibb.co/6Y1ZDtx/screenshot.png)

## Bogues
Si après une requête, la page suivante s'affiche :

![Heroku bug](https://i.ibb.co/TK2Bpz0/screenshot.png)

Vérifiez les points suivants :
1. Vous avez bien importé les fichiers préalables ( Au moins le plan comptable et une extraction )
2. La structure des fichiers fournis corresponds bien à celle décrite ci-dessus ( Pas de colonnes supplémentaires ou manquantes )

Si cette erreur survient après l'import d'une extraction et de la masse salariale en même temps, réessayer en important l'un puis l'autre.

