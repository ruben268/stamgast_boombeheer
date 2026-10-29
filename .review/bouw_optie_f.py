"""Voorbeeldpagina's optie F (USP's met losse oranje V-tjes, zonder knoppen): <pagina>-optie-f.html
Gebruik vanuit repo-root: python3 .review/bouw_optie_f.py"""
import re
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
CSS = """
    .usp-lijst { list-style: none; padding: 0; margin: 28px 0 0; display: grid; gap: 12px; }
    .usp-lijst li { display: flex; align-items: center; gap: 12px; font-size: 16px; line-height: 1.4; color: var(--tekst); margin: 0; }
    .usp-lijst b { font-weight: 600; }
    .usp-lijst .v { width: 22px; height: 22px; flex-shrink: 0; color: var(--oranje); display: inline-flex; }
    .usp-lijst .v svg { width: 22px; height: 22px; }
    .page-donker .usp-lijst li { color: rgba(255,255,255,.92); }
    .page-donker .usp-lijst .v { color: #F2A27E; }
"""
USP = {
 "diensten.html":    ["<b>ETW-gecertificeerd</b> boomverzorger", "<b>Eerlijk advies</b> vooraf, ook als er niets moet gebeuren", "Actief in <b>Oost- en West-Vlaanderen</b>"],
 "over-lode.html":   ["<b>European Tree Worker</b> sinds 2017", "<b>VETCERT</b>-specialist in veterane bomen", "<b>Stamgast Boombeheer</b> sinds 2021"],
 "aanpak.html":      ["<b>Plaatsbezoek</b> voor een correcte prijsbepaling", "<b>Offerte</b> zonder verborgen kosten", "<b>Uitvoering door Lode zelf</b>, volgens de ETW-normen"],
 "referenties.html": ["<b>Echte reviews</b>, rechtstreeks van Google", "<b>Van snoeien tot stormschade</b>: een greep uit het werk", "<b>Projecten</b> in Oost- en West-Vlaanderen"],
}
DONKER = {"aanpak.html", "referenties.html"}
PAGES = ["index.html","over-lode.html","diensten.html","aanpak.html","referenties.html","contact.html"]
for p in PAGES:
    t = open(p, encoding="utf-8").read()
    if p in USP:
        t = t.replace("</style>", CSS + "</style>", 1)
        if p in DONKER: t = t.replace('<section class="page-hero">', '<section class="page-hero page-donker">', 1)
        m = re.search(r'(<p class="slogan-titel">.*?</p>\n<p>.*?</p>)\n', t, re.S); assert m, p
        lst = '\n<ul class="usp-lijst">' + "".join(f'<li><span class="v">{CHECK}</span><span>{x}</span></li>' for x in USP[p]) + '</ul>'
        t = t.replace(m.group(1), m.group(1) + lst, 1)
    # offerteknoppen springen direct naar het formulier op de contactpagina
    t = re.sub(r'(<a class="(?:nav-cta|mobiel-cta|btn-primair|btn-wit)" href=")contact\.html"', r'\1contact.html#offerte"', t)
    if p == "contact.html":
        anker = '<section class="sectie">\n<div class="wrapper">\n<div class="contact-grid">'
        assert t.count(anker) == 1
        t = t.replace(anker, anker.replace('<section class="sectie">', '<section class="sectie" id="offerte" style="scroll-margin-top:24px">'), 1)
    for q in PAGES:
        t = re.sub(rf'href="{re.escape(q)}(#[^"]*)?"', lambda mm, q=q: f'href="{q[:-5]}-optie-f.html{mm.group(1) or ""}"', t)
    t = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', t)
    t = t.replace('<script src="cookies.js"></script>', '')
    t = t.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow"/>', 1)
    open(p[:-5] + "-optie-f.html", "w", encoding="utf-8").write(t)
print("ok")
