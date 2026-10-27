"""Voert de beslissingen (beslissingen.py) door in de echte pagina's."""
import re, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from suggesties import S
from beslissingen import B
EL = re.compile(r'^(<(\w+)(?:\s[^>]*)?>)(.*)(</\2>)$', re.S)
final = {}
for i,(page,cat,old,new,why) in enumerate(S,1):
    sid=f"S{i:02d}"; st,eig=B[sid]
    if st=="ok": f=new
    elif st=="eigen":
        m=EL.match(old); f = m.group(1)+eig+m.group(4) if m else eig
    else: continue
    t=open(page,encoding="utf-8").read()
    if t.count(old)!=1: sys.exit(f"{sid}: {t.count(old)}x")
    open(page,"w",encoding="utf-8").write(t.replace(old,f))
    final[sid]={"page":page,"old":old,"new":f}
json.dump(final,open(os.path.join(os.path.dirname(__file__),"doorgevoerd.json"),"w"),ensure_ascii=False,indent=1)
print(len(final),"doorgevoerd")
