"""Bouwt <pagina>-open.html naast elke pagina, met de tekstsuggesties gemarkeerd in context.
Gebruik: python3 .review/bouw_suggesties.py   (vanuit de repo-root)"""
import re, json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from open_punten import P

PAGES = ["index.html","over-lode.html","diensten.html","aanpak.html","referenties.html","contact.html"]
NAMEN = {"index.html":"Home","over-lode.html":"Over Lode","diensten.html":"Diensten","aanpak.html":"Aanpak","referenties.html":"Referenties","contact.html":"Contact"}
CATS = {"L":"Eigen voorstel Lode","A":"Afgewezen door Lode"}
EL = re.compile(r'^(<(\w+)(?:\s[^>]*)?>)(.*)(</\2>)$', re.S)

def split(s):
    m = EL.match(s)
    return (m.group(1), m.group(3), m.group(4)) if m else ("", s, "")

data, per_page = {}, {p: [] for p in PAGES}
for sid, page, cat, old, new, why in P:
    per_page[page].append(sid)
    data[sid] = {"page": page, "cat": cat, "why": why, "old": old, "new": new}

def sug_span(sid, inner, extra=""):
    return f'<span class="sg sg-{data[sid]["cat"]}{extra}" data-id="{sid}" tabindex="0">{inner}</span>'

out_data = {}
for page in PAGES:
    t = open(page, encoding="utf-8").read()
    for sid in per_page[page]:
        d = data[sid]; old, new = d["old"], d["new"]
        n = t.count(old)
        if n != 1: sys.exit(f"{sid} {page}: {n}x gevonden -> {old[:60]}")
        if new is None:                                   # opmerking zonder tekstvoorstel
            o1, oi, o2 = split(old)
            rep = o1 + sug_span(sid, oi) + o2
            out_data[sid] = {**d, "old_i": oi, "new_i": None}
        elif new.startswith(old):                         # toevoeging (bv. extra checkbox)
            add = new[len(old):]
            add = re.sub(r'(/>\s*)([^<]+)(</label>)', lambda m: m.group(1) + sug_span(sid, m.group(2), " sg-add") + m.group(3), add, count=1)
            rep = old + add
            out_data[sid] = {**d, "old_i": "(nieuw toegevoegd)", "new_i": re.sub(r'<[^>]+>', '', new[len(old):]).strip()}
        else:
            o1, oi, o2 = split(old); n1, ni, n2 = split(new)
            if o1 and o1 == n1 and o2 == n2:
                rep = o1 + sug_span(sid, ni) + o2
            elif o1 and n1 and o2 == n2:                  # zelfde tag, ander attribuut
                rep = n1 + sug_span(sid, ni) + n2
            else:
                oi, ni = old, new
                rep = sug_span(sid, ni)
            out_data[sid] = {**d, "old_i": oi, "new_i": ni}
        t = t.replace(old, rep, 1)
    # navigatie naar de suggestieversies, niet indexeren
    for p in PAGES:
        t = re.sub(rf'href="{re.escape(p)}(#[^"]*)?"', lambda m, p=p: f'href="{p[:-5]}-open.html{m.group(1) or ""}"', t)
    t = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', t)
    t = t.replace('<script src="cookies.js"></script>', '')   # geen banner/analytics op reviewpagina's
    t = t.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow"/>', 1)
    open(page[:-5] + "-open.html", "w", encoding="utf-8").write(t)

# laag (css + balk + popup + js) injecteren
LAAG = open(os.path.join(os.path.dirname(__file__), "laag_open.html"), encoding="utf-8").read()
for page in PAGES:
    f = page[:-5] + "-open.html"; t = open(f, encoding="utf-8").read()
    links = "".join(
        f'<a href="{p[:-5]}-open.html" class="{"actief" if p == page else ""}">{NAMEN[p]} <span>{len(per_page[p])}</span></a>' for p in PAGES)
    laag = (LAAG.replace("{{DATA}}", json.dumps(out_data, ensure_ascii=False))
                .replace("{{NAMEN}}", json.dumps(NAMEN, ensure_ascii=False))
                .replace("{{CATS}}", json.dumps(CATS, ensure_ascii=False))
                .replace("{{LINKS}}", links).replace("{{TOTAAL}}", str(len(P))))
    t = t.replace("</body>", laag + "\n</body>", 1)
    open(f, "w", encoding="utf-8").write(t)
print(len(P), "open punten:", {NAMEN[p]: len(v) for p, v in per_page.items()})
