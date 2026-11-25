import csv, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=[r for r in csv.DictReader(l for l in open('weekly.csv') if not l.startswith('#'))]
lab=[r['report'][5:].replace('-','.')[::-1].replace('.', '.',1) for r in R]
lab=[f"{r['report'][8:]}.{r['report'][5:7]}" for r in R]
v=[100*int(r['hormuz_inc'])/(int(r['out'])+int(r['in'])) for r in R]
fig,ax=plt.subplots(figsize=(12,6.3),dpi=100); fig.patch.set_facecolor('white')
ax.axhspan(1,2,color='#d9d9d9',zorder=0); ax.text(2.5,1.5,'1980s Tanker War:\n1–2% of ships transiting\nHormuz attacked',va='center',ha='center',zorder=3,fontsize=11,color='#444')
b=ax.bar(lab,v,width=0.6,color='#2a6fdb',zorder=2)
for x,(val,r) in enumerate(zip(v,R)): ax.text(x,val+0.08,f"{val:.1f}%\n{r['hormuz_inc']}/{int(r['out'])+int(r['in'])}",ha='center',fontsize=10,color='#222')
ax.set_ylabel('verified attacks per transit, %',fontsize=11); ax.set_ylim(0,4.6)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color='#eee',zorder=0); ax.set_xlabel('UKMTO weekly report (transits: 7 days ending ~2 days before)',fontsize=10)
ax.set_title('Strait of Hormuz, 7 weeks to 18 Nov 2026: one verified attack per ~50 transits',fontsize=14,loc='left',pad=26)
ax.text(0,1.015,'41 attacks / 1,943 transits pooled. Weekly bars are rough: attack and transit windows are offset by ~2 days.',transform=ax.transAxes,fontsize=10,color='#444',va='bottom')
fig.text(0.01,0.01,'Data: UKMTO VRA weekly overviews (attacks verified from primary sources; transits = AIS + US-stated, unverified). 1980s: O\'Rourke, USNI Proceedings 1988. errata.page',fontsize=8.5,color='#555')
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig('hormuz_risk.png')
