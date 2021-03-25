"""This file is necessary because heroku doesn't support locale_fr
so we need to calculate month name by hand"""


def get_month_name(i):
    switcher = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: 'Juin',
        7: 'Juillet',
        8: 'Aout',
        9: 'Septembre',
        10: 'Octobre',
        11: 'Novembre',
        12: 'Décembre'
    }
    return switcher.get(i, "Invalid Month")
