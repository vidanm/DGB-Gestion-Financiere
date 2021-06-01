from reportlab.platypus import Table, TableStyle
from .colors import black, lightwhite, bleu, bleuciel, yellow

class Style():
    
    def __init__(self,table,tableHeight=-1,total=True):
        self.tablestyle = [
            ('FACE', (0, 0), (-1, -1), "Helvetica-Bold"),
            ('FACE', (1, 1), (-1,-2), "Helvetica"),
            ('GRID', (0, 0), (-1, -1), 0.1, black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), "CENTER"),
            ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
            ('BACKGROUND', (0, 0), (-1, 0), bleuciel),
            ('TEXTCOLOR', (0, 0), (-1, 0), "BLACK"),
            ('BACKGROUND', (1, 1), (-1, -1), "WHITE"),
            ]
        self.tableHeight = tableHeight
        self.tablelen = len(table)

        if tableHeight != -1:
            self.rowheights = (self.tablelen ) *\
                [min([int(tableHeight/(self.tablelen + 1)), 30])]
        else:
            self.rowheights = (self.tablelen) * [12]
        self.rowheights[0] = self.rowheights[0] * 1.4

        if total:
            self.add_total_style()

    def add_total_style(self):
        self.tablestyle.append(('BACKGROUND', (0, -1), (-1, -1), yellow))

    def add_title_style(self):
        self.rowheights.insert(
            0, min([int(self.tableHeight/(self.tablelen)), 30]))

        self.tablestyle.append(('SPAN', (0, 0), (-1, 0)))
        self.tablelen += 1

    def add_coloring(self, table):
        for i in range(self.tablelen):
            for j in range(len(table[i])):
                if table[i][j][0].isnumeric():
                    self.tablestyle.append(
                        ('TEXTCOLOR', (j, i), (j+1, i+1), "GREEN"))
                elif table[i][j][0] == '-':
                    self.tablestyle.append(
                        ('TEXTCOLOR', (j, i), (j+1, i+1), "RED"))
                else:
                    self.tablestyle.append(
                        ('TEXTCOLOR', (j, i), (j+1, i+1), "BLACK"))

    def get_style(self):
        return self.tablestyle

    def get_rowheights(self):
        return self.rowheights

    def add_custom_style(self, elem):
        """elem could be a list of styles or just one element."""
        if isinstance(elem, list):
            for i in elem:
                self.tablestyle.append(i)
        else:
            self.tablestyle.append(elem)

    def delete_index_line(self):
        self.tablestyle.append(('SPAN', (0, 0), (-1, 1)))
        self.rowheights.insert(
            0, min([int(self.tableHeight/(self.tablelen)), 30]))

        self.rowheights[0] = self.rowheights[0] / 3
        self.tablelen += 1
