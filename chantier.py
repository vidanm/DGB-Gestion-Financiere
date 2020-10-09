import pandas as pd
import datetime as dt
from poste import *

chantier = pd.read_excel("~/Documents/DGB/Resultat_chantier/chantier/19-GP-ROSN.xlsx")
chantier = chantier.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°','Section analytique'])

dicAccountSite,dicAccountStruct = RecupDictComptable("/home/vidan/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")

print(chantier)
