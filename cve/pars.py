import os
import json


cveDir = os.path.join(os.path.dirname(os.getcwd()), 'cves')

for year in os.listdir(cveDir)[:-2]:
    # print(year)
    for k in os.listdir(os.path.join(cveDir, year)):
        # print(k)
        for jsnName in os.listdir(os.path.join(cveDir, year, k)):
            # print(jsnName)
            jsn = json.load(open(os.path.join(cveDir, year, k, jsnName)))
            try:
                product = jsn['containers']['cna']['affected'][0]['product']
            except KeyError:
                product = 'n/a'

            if product != 'n/a':
                print(product)