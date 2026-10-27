"""Controleversie voor Lode: <pagina>-controle.html.
Vergelijkt elke pagina met de basisversie (BASIS) en markeert alle tekstwijzigingen,
met de reden erbij (ronde 1 = je-vorm, ronde 2 = tekstsuggesties S01–S50).
Gebruik (vanuit repo-root): python3 .review/bouw_controle.py"""
import re, os, sys, json, ast, difflib, subprocess, html
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
from suggesties import S
from beslissingen import B, WAAROM_LODE

BASIS = "3355d903e6d7"
PAGES = ["index.html","over-lode.html","diensten.html","aanpak.html","referenties.html","contact.html"]
NAMEN = {"index.html":"Home","over-lode.html":"Over Lode","diensten.html":"Diensten","aanpak.html":"Aanpak","referenties.html":"Referenties","contact.html":"Contact"}
TOK = re.compile(r'<[^>]+>|[^<\s]+|\s+')

# ---- redenen ronde 1 (je-vorm) ----
src = open(os.path.join(HIER, "ronde1_jevorm.py"), encoding="utf-8").read()
R1 = ast.literal_eval(re.search(r'^R = (\{.*?^\})', src, re.S | re.M).group(1))
JE = "Aanspreekvorm: de website spreekt bezoekers nu aan met ‘je’ in plaats van ‘u’. Dat is persoonlijker en past bij een lokale vakman. (Privacy- en cookiebeleid blijven bewust in de u-vorm.)"
EXTRA = [
 ("Wil u", "‘Wil u’ was eigenlijk ook taalkundig fout (‘Wilt u’)."),
 ("conform", "‘Conform’ is administratieve taal; ‘volgens’ zegt hetzelfde, eenvoudiger."),
 ("Enkel indien nodig", "‘Indien nodig’ is formeel; ‘als het moet’ klinkt natuurlijker."),
 ("trachten", "‘Trachten’ is formeel; ‘proberen’ is gewone spreektaal."),
 ("is key", "Grammatica: ‘groeiomstandigheden … zijn’ (meervoud)."),
 ("48u", "Reactietijd gelijkgetrokken met de contactpagina, waar ‘doorgaans binnen 2 werkdagen’ staat."),
 ("U neemt contact op", "De stap is nu een oproep, net als de tekst eronder (‘Bel, mail of vul het formulier in’)."),
 ("Samen plannen jullie", "‘Jullie’ sprak de bezoeker in het meervoud aan. Nu staat er duidelijk dat de klant en Lode samen plannen."),
 ("alsook diens", "‘Alsook diens’ en ‘indien’ zijn stijve woorden, vervangen door spreektaal."),
 ("omtrent", "‘Omtrent’ werd ‘over’: eenvoudiger."),
 ("diens toekomstbeeld", "‘Diens toekomstbeeld’ werd ‘zijn toekomst’: eenvoudiger."),
 ("daadwerkelijk", "Het overbodige woord ‘daadwerkelijk’ is geschrapt."),
 ("weloverwogen beslissing", "‘Een weloverwogen beslissing kunt nemen’ werd ‘bewust kan kiezen’: korter."),
 ("specifieke situatie", "‘Specifieke’ was overbodig."),
]
def reden_r1(old):
    r = []
    if re.search(r'\b([Uu]|[Uu]w)\b', re.sub(r'<[^>]+>', '', old)): r.append(JE)
    r += [t for k, t in EXTRA if k in old]
    return r or [JE]

# ---- alle gekende wijzigingen: (pagina, nieuwe snippet in eindversie, redenen) ----
changes = []
for page, pairs in R1.items():
    for old, new in pairs:
        if page in PAGES: changes.append((page, new, reden_r1(old)))
done = json.load(open(os.path.join(HIER, "doorgevoerd.json"), encoding="utf-8"))
why = {f"S{i:02d}": w for i, (_, _, _, _, w) in enumerate(S, 1)}
for sid, d in done.items():
    changes.append((d["page"], d["new"], [WAAROM_LODE.get(sid, why[sid])]))

from ronde3 import R3
for page, _, new, keys in R3:
    if keys:
        changes.append((page, new, [JE if k == "JE" else WAAROM_LODE.get(k, why.get(k, k)) for k in keys]))

def strip(h): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h))).strip()

data, per_page, n = {}, {p: [] for p in PAGES}, 0
for page in PAGES:
    a = subprocess.run(["git", "show", f"{BASIS}:{page}"], capture_output=True, text=True, check=True).stdout
    b = open(page, encoding="utf-8").read()
    A, Bt = TOK.findall(a), TOK.findall(b)
    ops = [o for o in difflib.SequenceMatcher(None, A, Bt, autojunk=False).get_opcodes() if o[0] != "equal"]
    # samenvoegen binnen hetzelfde tekstblok (geen tag tussen twee wijzigingen)
    regs = []
    for _, i1, i2, j1, j2 in ops:
        if regs and not any(t.startswith("<") for t in Bt[regs[-1][3]:j1]) and not any(t.startswith("<") for t in A[regs[-1][1]:i1]):
            regs[-1][1], regs[-1][3] = i2, j2
        else:
            regs.append([i1, i2, j1, j2])
    offs = [0]
    for t in Bt: offs.append(offs[-1] + len(t))
    spans_pos = []
    for page_c, new, rs in changes:
        if page_c != page: continue
        for m in re.finditer(re.escape(new), b): spans_pos.append((m.start(), m.end(), rs))
    inserts = []
    for i1, i2, j1, j2 in regs:
        n += 1; wid = f"W{n:02d}"
        s0, s1 = offs[j1], offs[j2]
        rs = []
        for k0, k1, r in spans_pos:
            if (k0 < s1 and s0 < k1) if s1 > s0 else (k0 <= s0 <= k1):
                rs += [x for x in r if x not in rs]
        if not rs: print("ZONDER REDEN:", page, repr("".join(Bt[j1:j2])[:80]))
        oldh, newh = "".join(A[i1:i2]), "".join(Bt[j1:j2])
        def node(T, x1, x2):   # volledige tekst van het tekstblok rond de wijziging (context in de popup)
            while x1 > 0 and not T[x1 - 1].startswith("<"): x1 -= 1
            while x2 < len(T) and not T[x2].startswith("<"): x2 += 1
            return strip("".join(T[x1:x2]))
        ctxo, ctxn = node(A, i1, i2), node(Bt, j1, j2)
        if "<" in newh:   # toegevoegd element (vinkje): enkel de tekst erin markeren
            m = re.search(r'(/>\s*)([^<]+)(</label>)', newh)
            newh_m = newh[:m.start(2)] + f'<span class="wz wz-nieuw" data-id="{wid}" tabindex="0">{m.group(2)}</span>' + newh[m.end(2):]
            data[wid] = {"page": page, "old": "", "new": strip(m.group(2)), "oldh": None, "newh": m.group(2), "rs": rs, "nieuw": True}
            inserts.append((j1, j2, newh_m))
        else:
            data[wid] = {"page": page, "old": ctxo, "new": ctxn, "oldh": oldh, "newh": newh, "rs": rs}
            inserts.append((j1, j2, f'<span class="wz" data-id="{wid}" tabindex="0">{newh}</span>'))
        per_page[page].append(wid)
    out = list(Bt)
    for j1, j2, rep in reversed(inserts):
        out[j1:j2] = [rep]
    t = "".join(out)
    for p in PAGES:
        t = re.sub(rf'href="{re.escape(p)}(#[^"]*)?"', lambda m, p=p: f'href="{p[:-5]}-controle.html{m.group(1) or ""}"', t)
    t = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', t)
    t = t.replace('<script src="cookies.js"></script>', '')
    t = t.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow"/>', 1)
    open(page[:-5] + "-controle.html", "w", encoding="utf-8").write(t)

LAAG = open(os.path.join(HIER, "laag_lode.html"), encoding="utf-8").read()
for page in PAGES:
    f = page[:-5] + "-controle.html"; t = open(f, encoding="utf-8").read()
    links = "".join(f'<a href="{p[:-5]}-controle.html" class="{"actief" if p == page else ""}">{NAMEN[p]} <span>{len(per_page[p])}</span></a>' for p in PAGES)
    laag = (LAAG.replace("{{DATA}}", json.dumps(data, ensure_ascii=False)).replace("{{NAMEN}}", json.dumps(NAMEN, ensure_ascii=False))
                .replace("{{LINKS}}", links).replace("{{TOTAAL}}", str(n)))
    open(f, "w", encoding="utf-8").write(t.replace("</body>", laag + "\n</body>", 1))
json.dump(data, open(os.path.join(HIER, "controle.json"), "w"), ensure_ascii=False, indent=1)
print(n, "wijzigingen:", {NAMEN[p]: len(v) for p, v in per_page.items()})
