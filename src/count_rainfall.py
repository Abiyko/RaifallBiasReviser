def make_dict(revisedDict_SSDB):
    rainfall_val = {}
    for month in revisedDict_SSDB:
        if month not in rainfall_val:
            rainfall_val[month] = {}

        monthly_list = revisedDict_SSDB[month]

        for element in monthly_list:
            element = round(float(element))
            if element in rainfall_val[month]:
                rainfall_val[month][element] += 1
            else:
                rainfall_val[month][element] = 1
                
    return rainfall_val

if __name__ == '__main__':
    make_dict()