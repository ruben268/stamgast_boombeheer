# Ronde 3 (2026-10-27): bijsturingen van Ruben na zijn eigen controle.
# (pagina, huidige tekst, nieuwe tekst, reden-sleutel of eigen reden voor Lode)
JOUW = "Waar het over je bomen of je situatie gaat, schrijven we bewust ‘jouw’: voor veel mensen zijn hun bomen dierbaar, en ‘jouw’ klinkt dan persoonlijker dan ‘je’."
KLANT = "Hier bewust ‘de klant’: de zin gaat over hoe Stamgast samenwerkt, niet over één bezoeker in het bijzonder."
S22 = "De zin ‘maar alsnog kunnen behouden’ liep wat stroef. Nu opgesplitst in kortere zinnen; ‘hier’ maakt duidelijk dat de boom bij Stamgast wél behouden kon worden."
R3 = [
 ("index.html", "zorgt voor je bomen in", "zorgt voor jouw bomen in", ["JE", JOUW]),
 ("index.html", '<span class="tag-waarschuwing">Enkel als het moet</span>', '<span class="tag-waarschuwing">Enkel indien nodig</span>', None),
 ("index.html", "Eenvoudig, eerlijk en altijd in overleg met jou.", "Eenvoudig, eerlijk en altijd in overleg met de klant.", [KLANT]),
 ("index.html", "Klaar om je bomen uit handen te geven?", "Klaar om jouw bomen uit handen te geven?", ["JE", JOUW]),
 ("diensten.html", "groeiplaats van je boom — altijd met eerlijk advies vooraf.", "groeiplaats van jouw boom — altijd met eerlijk advies vooraf.", ["JE", JOUW, "S18"]),
 ("diensten.html", 'display:inline-block;">Enkel als het moet</span>', 'display:inline-block;">Enkel indien nodig</span>', None),
 ("diensten.html", "Een beuk van meer dan een eeuw oud. Door anderen reeds afgeschreven en alsnog behouden. De boom staat er vandaag nog steeds, gezond en veilig.",
  "Een beuk van meer dan een eeuw oud. Door anderen reeds afgeschreven, maar hier alsnog kunnen behouden. De boom staat er vandaag nog steeds, gezond en veilig.", [S22]),
 ("diensten.html", "<p>Lode komt langs, bekijkt je situatie en geeft eerlijk advies", "<p>Lode komt langs, bekijkt jouw situatie en geeft eerlijk advies", ["JE", JOUW]),
 ("aanpak.html", "over wat je boom echt nodig heeft, daarna de correcte uitvoering.", "over wat jouw boom echt nodig heeft, daarna de correcte uitvoering.", ["JE", JOUW, "S27"]),
 ("aanpak.html", "Lode komt ter plaatse, bekijkt je situatie en geeft je een eerlijk oordeel.", "Lode komt ter plaatse, bekijkt jouw situatie en geeft je een eerlijk oordeel.", ["JE", JOUW]),
 ("aanpak.html", "veilig voor jou, goed voor je boom.", "veilig voor jou, goed voor jouw boom.", ["JE", JOUW]),
 ("referenties.html", "wat Stamgast voor je bomen kan doen", "wat Stamgast voor jouw bomen kan doen", ["JE", JOUW]),
 ("contact.html", "Beschrijf kort je situatie", "Beschrijf kort jouw situatie", ["JE", JOUW]),
]
if __name__ == "__main__":
    for page, old, new, _ in R3:
        t = open(page, encoding="utf-8").read()
        if t.count(old) != 1: raise SystemExit(f"{page}: {t.count(old)}x -> {old}")
        open(page, "w", encoding="utf-8").write(t.replace(old, new))
    print(len(R3), "aanpassingen")
