#!/usr/bin/env python3
"""analyse.py — per-crossing attack risk in Hormuz from UKMTO weekly overviews, against the 1980s Tanker War; and whether a week's
attacks are followed by fewer transits (n=6 pairs: a sign check, not a test with power)."""
import csv, itertools, statistics as st
R=[r for r in csv.DictReader(l for l in open('weekly.csv') if not l.startswith('#'))]
for r in R:
    for k in ('out','in','ais','hormuz_inc','all_inc'): r[k]=int(r[k])
    r['tot']=r['out']+r['in']
inc=sum(r['hormuz_inc'] for r in R); tot=sum(r['tot'] for r in R); ais=sum(r['ais'] for r in R)
print(f"weeks {len(R)} ({R[0]['report']}..{R[-1]['report']}): Hormuz incidents {inc}, combined transits {tot}, AIS-observed {ais}")
print(f"per transit, combined denominator: {inc/tot:.2%}   per round-trip voyage (x2): {2*inc/tot:.2%}")
print(f"per transit, AIS-only denominator (upper bound; many struck ships run dark): {inc/ais:.2%}")
for r in R: print(f"  {r['report']}  inc {r['hormuz_inc']:2d}  transits {r['tot']}  ais {r['ais']:3d}  risk/transit {r['hormuz_inc']/r['tot']:.2%}")
print(f"incidents per week now: {inc/len(R):.1f} (Hormuz only, verified)   Tanker War 1987: 181 attacks in the whole Gulf = {181/52:.1f}/week (USNI Proceedings May 1989)")
print("Tanker War per-voyage share attacked: 'between 1% and 2%' of ships transiting Hormuz (O'Rourke, Proceedings May 1988); 'about one percent of Gulf voyages' (Walker 2000)")
# lagged sign check: incidents in week t vs combined transits in week t+1
x=[r['hormuz_inc'] for r in R[:-1]]; y=[r['tot'] for r in R[1:]]
def corr(a,b):
    ma,mb=st.mean(a),st.mean(b); return sum((p-ma)*(q-mb) for p,q in zip(a,b))/ (sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))**.5
c=corr(x,y); perms=list(itertools.permutations(y)); p=sum(1 for pp in perms if corr(x,pp)<=c)/len(perms)
print(f"lag-1: incidents(t) vs transits(t+1), n={len(x)}: r={c:+.2f}, exact permutation p(one-sided, r<=obs)={p:.3f} over {len(perms)} orders")
c0=corr([r['hormuz_inc'] for r in R],[r['tot'] for r in R]); print(f"same week: r={c0:+.2f} (n={len(R)})")
