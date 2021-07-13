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

## Structure des fichiers
Les fichiers fournis doivent respecter un certain format.
Tous doivent être importés sous le format .xls et non .xlsx.

### Plan comptable
![Example Plan](https://i.ibb.co/MsZhghm/screenshot.png)
1.  Les intitulés de postes doivent se trouver sur la 1ère colonne pour le section chantier et la 5ème colonne pour la section structure.
2.  Les noms de colonnes doivent se trouver sur la 2e ligne.
3.  **Une seule ligne par sous poste !** Pour avoir plusieurs compte pour un sous poste, respecter le format suivant :
`NOM DU SOUS POSTE | NUMERO 1 / NUMERO 2 / NUMERO 3`
4. Il faut, pour l'instant, supprimer le tableau ci joint, du plan comptable :
![Tableau a supprimer](https://i.ibb.co/XSj13ky/screenshot.png)
5. Les cellules POSTE doivent être fusionnées pour éviter les erreurs de calcul.


### Extractions chantiers
![Example extraction](https://i.ibb.co/1Jm39y7/screenshot.png)
1.  Vérifier la présence des champs ‘Journal’ / ‘Général’ / ‘Date’ / ‘Débit’ / ‘Crédit’ / ‘Section analytique’.
2.  Le nom ( *La section analytique* ) des charges qui concernent les dépenses de la structure doivent comporter 'STRUCT'.

### Budget
1. Le nom des postes et des sous postes doivent **obligatoirement** correspondre aux noms donnés dans le plan
comptable. Exemple : "Sous traitant MO" est différent de "Sous traitant Main d'oeuvre"
2. Le prix de vente est lu comme un poste contenant les sous postes : Vente / Avenants / Prorata, dans l'application
tout est additionné pour calculer le prix de vente.
3. La deuxième feuille comprends les données Marché/Avenants pour certains postes ( Intervenants / MO ) et Quantité/Prix unitaire pour d'autres ( Bois Beton Aciers )

### Masse salariale
![Example Masse Salariale](https://i.ibb.co/6Y1ZDtx/screenshot.png)

## Bogues
Si après une requête, la page suivante s'affiche :

![Heroku bug](https://i.ibb.co/TK2Bpz0/screenshot.png)

Vérifiez les points suivants :
1. Vous avez bien importé les fichiers préalables ( Au moins le plan comptable et une extraction )
2. La structure des fichiers fournis corresponds bien à celle décrite ci-dessus ( Pas de colonnes supplémentaires ou manquantes )
3. Les cellules sont bien fusionnées dans le plan comptable

Si malgré les vérifications le programme ne fonctionne toujours pas : Déconnectez vous puis réimportez les fichiers.

## À savoir
Tout les fichiers importés sont supprimés a la déconnexion.
Il faut donc bien les réimporter a chaque nouvelle connexion.
