def merge_two_dict(d1,d2):
    d3 = d1.copy()
    d3.update(d2)
    return d3

def is_in_dic(a,dic):
    for key in dic:
        if key == a:
            return True
    return False
