import os
import json

cveDir = os.path.join(os.path.dirname(os.getcwd()), 'cves')

for year in os.listdir(cveDir)[:-2]:
    # print(year)
    for k in os.listdir(os.path.join(cveDir, year)):
        # print(k)
        for jsnName in os.listdir(os.path.join(cveDir, year, k)):
            # print(jsnName)
            jsn = json.load(open(os.path.join(cveDir, year, k, jsnName), encoding='utf-8'))
            try:
                product = jsn['containers']['cna']['affected'][0]['product']
                version = jsn['containers']['cna']['affected'][0]['versions'][0]['version']
            except KeyError:
                product = 'n/a'
                version = 'unknown'

            if version not in ['unknown', 'n/a', 'unspecified'] and product not in ['n/a', 'unknown']:
                print(f'{jsnName}|{product}|{version}')
