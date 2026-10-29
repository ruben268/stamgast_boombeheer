"""Optie F definitief (2026-10-29): USP-lijst met oranje V-tjes in de page-hero + offerteknoppen -> contact.html#offerte."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), "bouw_optie_f.py"), encoding="utf-8").read()
ns = {}; exec(src.split("DONKER =")[0], ns)          # haalt CHECK, CSS en USP uit de voorbeeld-generator
CHECK, CSS, USP = ns["CHECK"], ns["CSS"], ns["USP"]
DONKER = {"aanpak.html", "referenties.html"}
PAGES = ["index.html","over-lode.html","diensten.html","aanpak.html","referenties.html","contact.html",
         "privacybeleid.html","cookiebeleid.html"]

css = open("style.css", encoding="utf-8").read()
if ".usp-lijst" not in css:
    css = css.rstrip() + "\n\n/* USP-lijst met oranje V-tjes in de page-hero (optie F, okt 2026) */\n" + \
          "\n".join(l.strip() for l in CSS.strip().splitlines()) + "\n"
    open("style.css", "w", encoding="utf-8").write(css)

for p in PAGES:
    t = open(p, encoding="utf-8").read()
    if p in USP and 'class="usp-lijst"' not in t:
        if p in DONKER:
            assert t.count('<section class="page-hero">') == 1, p
            t = t.replace('<section class="page-hero">', '<section class="page-hero page-donker">', 1)
        m = re.search(r'(<p class="slogan-titel">.*?</p>\n<p>.*?</p>)\n', t, re.S); assert m, p
        lst = '\n<ul class="usp-lijst">' + "".join(f'<li><span class="v">{CHECK}</span><span>{x}</span></li>' for x in USP[p]) + '</ul>'
        t = t.replace(m.group(1), m.group(1) + lst, 1)
    t = re.sub(r'(<a class="(?:nav-cta|mobiel-cta|btn-primair|btn-wit)" href=")contact\.html"', r'\1contact.html#offerte"', t)
    if p == "contact.html" and 'id="offerte"' not in t:
        anker = '<section class="sectie">\n<div class="wrapper">\n<div class="contact-grid">'
        assert t.count(anker) == 1
        t = t.replace(anker, anker.replace('<section class="sectie">', '<section class="sectie" id="offerte" style="scroll-margin-top:24px">'), 1)
    open(p, "w", encoding="utf-8").write(t)
print("ok")
