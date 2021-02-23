import sys
sys.path.append("/home/vidan/Documents/DGB/Gesfin/src")
from dataprocess.charges import Charges
from dataprocess.chiffreaffaire import ChiffreAffaire
from dataprocess.plan_comptable import PlanComptable

plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
codes_missing = open("missing_numbers.txt","w")
charges = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",plan,codes_missing)
ca = ChiffreAffaire(charges)

print(ca.calcul_ca_mois(6,2020))
print(ca.calcul_ca_annee(2020))
