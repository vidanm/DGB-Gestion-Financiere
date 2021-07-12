import pandas as pd

def qt_tab_bois():
    col = ["Type de bois","Surface coffrante plancher","M² consommé mois",
            "M² consommé cumul","Ratio consommation","PU Moyen","Ratio €/m² coffre"]
    exemple = ["Contreplaqué",0,0,0,0,0,0]
    return pd.DataFrame([exemple],col)

def qt_tab_beton():
    col = ["Type de beton","Quantité du mois m³","Quantité cumul m³",
            "m³ etude","Quantité restante","PFDC","Ecart",
            "PU Moyen etudes","PU Moyen chantier"]
    
    exemple = [
            ["Gros Beton",0,0,0,0,0,0,0,0],
            ["C 25/30",0,0,0,0,0,0,0,0,0],
            ["C 30/37",0,0,0,0,0,0,0,0,0],
            ["C 40/50",0,0,0,0,0,0,0,0,0],
            ["C 50/60",0,0,0,0,0,0,0,0,0]
            ]

    return pd.DataFrame(exemple,col)

def qt_tab_aciers():
    col = ["Type d'aciers","Dépenses du mois (kg)","Dépenses cumulées (kg)",
            "Budget (kg)","RAD (kg)","PFDC (kg)","Ecart (kg)",
            "PU Moyen etudes","PU Moyen chantier"]
    
    exemple = [
            ["Aciers HA",0,0,0,0,0,0,0,0],
            ["Aciers Trellis",0,0,0,0,0,0,0,0]
            ]
    pass
