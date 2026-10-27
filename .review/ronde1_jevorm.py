import sys, os, json, html
root = sys.argv[1]
R = {
"index.html": [
 ("zorgt voor uw bomen in", "zorgt voor je bomen in"),
 ("Wat kan Stamgast voor u doen?", "Wat kan Stamgast voor jou doen?"),
 ("Vakkundige snoeiwerken conform de ETW-normen. Lode snoeit gericht en naar de noden van uw boom", "Vakkundige snoeiwerken volgens de ETW-normen. Lode snoeit gericht en naar de noden van je boom"),
 ("Enkel indien nodig", "Enkel als het moet"),
 ("altijd in overleg met u.", "altijd in overleg met jou."),
 ("Klaar om uw bomen uit handen te geven?", "Klaar om je bomen uit handen te geven?"),
 ("bekijkt uw situatie en geeft u eerlijk advies", "bekijkt je situatie en geeft je eerlijk advies"),
],
"over-lode.html": [
 ("U weet altijd wat en waarom we iets gaan uitvoeren,", "Je weet altijd wat we gaan uitvoeren en waarom,"),
 ("Wil u met Lode samenwerken?", "Wil je met Lode samenwerken?"),
 ("Lode komt langs en geeft u eerlijk advies.", "Lode komt langs en geeft je eerlijk advies."),
],
"diensten.html": [
 ("Wat kan Stamgast voor u doen?", "Wat kan Stamgast voor jou doen?"),
 ("Van snoeien tot het daadwerkelijk verzorgen van de groeiplaats van uw boom", "Van snoeien tot het verzorgen van de groeiplaats van je boom"),
 ("Vakkundige snoeiwerken conform ETW-normen. Lode snoeit in de eerste plaats in functie van de boom, en diens toekomstbeeld.", "Vakkundige snoeiwerken volgens de ETW-normen. Lode snoeit in de eerste plaats in functie van de boom en zijn toekomst."),
 ("koppelt dit terug aan uw wensen", "koppelt dit terug aan jouw wensen"),
 ("Enkel indien nodig", "Enkel als het moet"),
 ("waar mogelijk trachten we de boom te behouden", "waar mogelijk proberen we de boom te behouden"),
 ("Goede groeiomstandigheden voor uw boom is key!", "Goede groeiomstandigheden voor je boom zijn key!"),
 ("Niet zeker welke dienst u nodig heeft?", "Niet zeker welke dienst je nodig hebt?"),
 ("Lode komt langs, bekijkt uw situatie en geeft eerlijk advies", "Lode komt langs, bekijkt je situatie en geeft eerlijk advies"),
],
"aanpak.html": [
 ("over wat uw boom echt nodig heeft", "over wat je boom echt nodig heeft"),
 ("<h3>U neemt contact op</h3>", "<h3>Neem contact op</h3>"),
 ("zonder dat u al meteen een afspraak hoeft te maken", "zonder dat je meteen een afspraak hoeft te maken"),
 ("bekijkt uw situatie en geeft u een eerlijk oordeel. Ook als dat betekent dat er niets hoeft te gebeuren. U staat nooit voor verrassingen.", "bekijkt je situatie en geeft je een eerlijk oordeel. Ook als dat betekent dat er niets hoeft te gebeuren. Je staat nooit voor verrassingen."),
 ("U ontvangt een transparante prijsopgave. Wat erin staat, is wat u betaalt. Lode legt uit wat er zal gebeuren en waarom — zodat u een weloverwogen beslissing kunt nemen.", "Je ontvangt een transparante prijsopgave. Wat erin staat, is wat je betaalt. Lode legt uit wat er zal gebeuren en waarom — zodat je bewust kan kiezen."),
 ("werkt conform de ETW-normen — veilig voor u, goed voor uw boom.", "werkt volgens de ETW-normen — veilig voor jou, goed voor je boom."),
 ("waar de boom staat, alsook diens omgeving. Lode bekijkt dit samen met u tijdens het plaatsbezoek en helpt u indien nodig op weg", "waar de boom staat, en van de omgeving. Lode bekijkt dit samen met jou tijdens het plaatsbezoek en helpt je waar nodig op weg"),
 ("Lode adviseert u op maat van uw specifieke situatie.", "Lode adviseert je op maat van jouw situatie."),
 ("U kunt bij Lode terecht voor zowat alle vragen omtrent bomen", "Je kan bij Lode terecht voor zowat alle vragen over bomen"),
 ("offerte op maat van uw situatie en budget", "offerte op maat van jouw situatie en budget"),
 ("Doorgaans binnen de 48u.", "Doorgaans binnen 2 werkdagen."),
 ("Lode bespreekt graag samen met u de opties en zoekt naar de passende snoeimethode voor uw boom</div>", "Lode bespreekt graag samen met jou de opties en zoekt naar de passende snoeimethode voor je boom.</div>"),
 ("Lode komt langs en geeft u eerlijk advies.", "Lode komt langs en geeft je eerlijk advies."),
],
"referenties.html": [
 ("wat Stamgast voor uw bomen kan doen", "wat Stamgast voor je bomen kan doen"),
],
"contact.html": [
 ("of Lode in uw gemeente actief is", "of Lode in jouw gemeente actief is"),
 ("<p>Vul het formulier in en Lode neemt zo snel mogelijk contact met u op.</p>", "<p>Vul het formulier in en Lode neemt zo snel mogelijk contact met je op.</p>"),
 ("Welke dienst(en) zoekt u?", "Welke dienst(en) zoek je?"),
 ("Beschrijf kort uw situatie", "Beschrijf kort je situatie"),
 ("Niet dringend — op uw tempo", "Niet dringend — op jouw tempo"),
 ("Uw gegevens worden enkel gebruikt voor deze aanvraag", "Je gegevens worden enkel gebruikt voor deze aanvraag"),
 ("Bedankt voor uw aanvraag!", "Bedankt voor je aanvraag!"),
 ("<p>Uw bericht is verstuurd. Lode neemt zo snel mogelijk contact met u op.</p>", "<p>Je bericht is verstuurd. Lode neemt zo snel mogelijk contact met je op.</p>"),
 ("Wat gebeurt er na uw aanvraag?", "Wat gebeurt er na je aanvraag?"),
 ("Lode leest uw aanvraag en neemt contact op", "Lode leest je aanvraag en neemt contact op"),
 ("Samen plannen jullie een plaatsbezoek in op een moment dat u past.", "Samen met Lode plan je een plaatsbezoek in op een moment dat jou past."),
 ("U krijgt eerlijk advies en, als er werk is,", "Je krijgt eerlijk advies en, als er werk is,"),
],
"cookies.js": [
 ("Met uw toestemming gebruiken we cookies", "Met jouw toestemming gebruiken we cookies"),
 ("Kies welke cookies u toestaat. U kunt uw keuze altijd wijzigen", "Kies welke cookies je toestaat. Je kan je keuze altijd wijzigen"),
 ("Onthoudt uw cookiekeuze.", "Onthoudt je cookiekeuze."),
],
}
log = []
for f, pairs in R.items():
    p = os.path.join(root, f); t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            sys.exit(f"FOUT {f}: {n}x gevonden: {old}")
        t = t.replace(old, new); log.append((f, old, new))
    open(p, "w", encoding="utf-8").write(t)
json.dump(log, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(log), "vervangingen")
