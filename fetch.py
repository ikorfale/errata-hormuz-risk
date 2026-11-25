#!/usr/bin/env python3
"""fetch.py — full daily history of Strait of Hormuz transits from IMF PortWatch (ArcGIS FeatureServer), paged."""
import json, urllib.parse, urllib.request, datetime as dt
U='https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query?'
rows=[]; off=0
while True:
    q=urllib.parse.urlencode({'where':"portname='Strait of Hormuz'",'outFields':'date,n_total,n_tanker,n_cargo,capacity_tanker',
        'orderByFields':'date ASC','resultOffset':off,'resultRecordCount':2000,'f':'json'})
    r=urllib.request.Request(U+q,headers={'User-Agent':'errata-lab/1.0'})
    d=json.load(urllib.request.urlopen(r,timeout=60))
    if 'features' not in d: raise SystemExit('bad answer: '+json.dumps(d)[:300])
    f=[x['attributes'] for x in d['features']]; rows+=f; off+=len(f)
    if len(f)<2000 and not d.get('exceededTransferLimit'): break
for x in rows:
    if isinstance(x['date'],(int,float)): x['date']=dt.datetime.fromtimestamp(x['date']/1000,dt.timezone.utc).date().isoformat()
json.dump(rows,open('data_hormuz.json','w'))
print(len(rows),rows[0]['date'],rows[-1]['date'])
