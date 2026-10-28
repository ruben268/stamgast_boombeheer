"""Echte Google-reviews (2026-10-28) op homepage en referenties. Locaties = die van de vroegere placeholders (OK van Ruben)."""
import re
R = {
 "ruben": ("RP","Ruben P.","Advies &amp; uitvoering","oktober 2026","Snel gereageerd en heel correct, vriendelijk advies over de bomen in onze tuin. Op een halve dag was de klus geklaard én tuin netjes opgeruimd. Een echte vakman, aanrader!"),
 "lotte": ("LS","Lotte S.","Advies","oktober 2026","Erg fijne samenwerking met Lode. Hij denkt graag met je mee, is betrouwbaar en communicatief, vraagt een eerlijke prijs en staat altijd klaar met advies. Ik zou hem absoluut aanbevelen!"),
 "joren": ("JS","Joren S.","Uitvoering","oktober 2026","Op de afspraak, faire prijs en echt vakmanschap!"),
 "jeroen":("JD","Jeroen D.","Snoeien","2021","Stamgast heeft knap werk verricht om onze krulwilg terug mooi in vorm te plaatsen. Fijne gast om mee samen te werken."),
 "nick":  ("ND","Nick D.","Ecologie &amp; beheer","2021","Boombeheer met respect voor de fauna!"),
}
HOME = ["ruben","lotte","nick","jeroen"]
REF  = ["ruben","lotte","joren","jeroen"]

t = open("index.html", encoding="utf-8").read()
pat = re.compile(r'<span class="t-dienst">[^<]*</span>\n<p class="t-tekst">[^<]*</p>\n<div class="t-auteur"><div class="t-avatar">[^<]*</div><div><div class="t-naam">[^<]*</div><div class="t-locatie">([^<]*)</div>')
m = pat.findall(t); assert len(m) == 4, m
it = iter(HOME)
def home(mm):
    a, n, d, _, x = R[next(it)]
    return f'<span class="t-dienst">{d}</span>\n<p class="t-tekst">"{x}"</p>\n<div class="t-auteur"><div class="t-avatar">{a}</div><div><div class="t-naam">{n}</div><div class="t-locatie">{mm.group(1)}</div>'
open("index.html", "w", encoding="utf-8").write(pat.sub(home, t))

t = open("referenties.html", encoding="utf-8").read()
pat = re.compile(r'<div class="r-avatar">[^<]*</div>\n<div><div class="r-naam">[^<]*</div><div class="r-meta">([^·<]*) · [^<]*</div></div>\n</div>\n<div class="r-sterren">★★★★★</div>\n</div>\n<span class="review-dienst">[^<]*</span>\n<p class="review-tekst">[^<]*</p>')
m = pat.findall(t); assert len(m) == 4, m
it = iter(REF)
def ref(mm):
    a, n, d, dt, x = R[next(it)]
    return (f'<div class="r-avatar">{a}</div>\n<div><div class="r-naam">{n}</div><div class="r-meta">{mm.group(1)} · {dt}</div></div>\n</div>\n'
            f'<div class="r-sterren">★★★★★</div>\n</div>\n<span class="review-dienst">{d}</span>\n<p class="review-tekst">"{x}"</p>')
open("referenties.html", "w", encoding="utf-8").write(pat.sub(ref, t))
print("ok")
