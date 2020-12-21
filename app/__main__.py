from dataprocess.charges import *
from dataprocess.synthese import *
import pandas as pd
import datetime as dt

codes_missing = open("missing_numbers.txt","w")
plan = PlanComptable('/home/vidan/DGBGesfinFlask/var/plan.xlsx')
charges = Charges("/home/vidan/DGBGesfinFlask/var/charges",plan,codes_missing)
synt = Synthese(charges)
synt.calcul_synthese_annee(8,2020)
print(synt.synthese_annee)
