import pyopenstates
import cfg

# pyopenstates.set_api_key(cfg.API_KEY_OPENSTATES)
# print(pyopenstates.get_metadata("CT"))


import urllib
from urllib.request import Request, urlopen


# link =  r"https://datausa.io/api/data?drilldowns=Nation&measures=Population"
link =  r"https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest"
import pandas as pd
import json
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
webpage = json.loads(webpage.decode('utf8').replace("'", '"'))
df = pd.json_normalize(webpage["data"])
print(df)

# f = urllib.request.urlopen(link)
# myfile = f.read()
# print(myfile)