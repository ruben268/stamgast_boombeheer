"""SEO (2026-10-28): oranje H1 met zoekterm boven de bestaande titel; bestaande titel wordt slogan (<p>) met identieke opmaak."""
import re
H = {
 "index.html":       ("Boomverzorger in Gent", "hero"),
 "diensten.html":    ("Bomen snoeien, vellen en advies in Gent", "page-hero"),
 "over-lode.html":   ("Gecertificeerd boomverzorger (ETW &amp; VETCERT)", "page-hero"),
 "aanpak.html":      ("Duurzaam boombeheer, stap voor stap", "page-hero"),
 "referenties.html": ("Reviews en realisaties", "page-hero"),
 "contact.html":     ("Offerte voor bomen snoeien of vellen", "page-hero"),
}
DONKER = {"aanpak.html", "referenties.html", "contact.html"}   # hero op diepgroen
for p, (h1, sect) in H.items():
    t = open(p, encoding="utf-8").read()
    assert t.count("<h1") == 1, p
    # selector .hero h1 / .page-hero h1 -> slogan-klasse
    t = re.sub(rf'\.{sect} h1\b', f'.{sect} .slogan-titel', t)
    t = re.sub(r'<h1>(.*?)</h1>', lambda m: f'<h1 class="zoekterm-h1">{h1}</h1>\n<p class="slogan-titel">{m.group(1)}</p>', t, count=1, flags=re.S)
    if p == "index.html":
        badge = '<div class="hero-badge"><i class="ti ti-award"></i> ETW + VETCERT gecertificeerd</div>\n'
        assert badge in t; t = t.replace(badge, "")
    kleur = "#F2A27E" if p in DONKER else "var(--oranje)"
    css = (f"    .zoekterm-h1 {{ font-size: 14px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; "
           f"color: {kleur}; line-height: 1.35; margin: 0 0 12px; }}\n    .slogan-titel {{ margin-top: 0; }}\n")
    t = t.replace("</style>", css + "</style>", 1)
    open(p, "w", encoding="utf-8").write(t)
print("ok")
