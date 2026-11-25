# Sterk Rygg · Black Week 2026 · e-poster

HTML-e-poster i samme design som kampanjesiden (`../black-week-checkout.html`).
Alle knapper går til **https://www.naprapatmaiken.no/black-week** med UTM-merking
(`utm_campaign=black-week-2026`, `utm_content=<kode>`).

- `build_emails.py`: kilden. Endre tekst, dato eller lenker her og kjør `python3 emails/build_emails.py`.
- `out/*.html`: ferdige e-poster, én fil per utsendelse.
- `out/index.html`: oversikt med lenke til hver e-post.

## Sendeplan (Oslo-tid)

| Kode | Når | Til | Emne | Forhåndsvisning | Fil |
|---|---|---|---|---|---|
| E-0 | Ons 25. nov 10:00 (anbefalt 13:00) | A + B | Fredag åpner jeg noe for deg | Bare for deg som har vært på foredraget mitt. | `e0-forvarsel.html` |
| K-1 | Tor 26. nov 10:00 | Kjøpere 1.–26. nov | Du får noe ekstra fra meg | Fordi du ble med i november. | `k1-novemberkjopere.html` |
| E-1 | Fre 27. nov 07:00 | A + B | Black Week: Sterk Rygg for 5 490 kr | Og to ting du bare får denne uka. | `e1-apning.html` |
| SMS-1 | Fre 27. nov 12:00 | Åpnet E-1, ikke kjøpt, SMS-samtykke | – | – | se under |
| E-2 | Lør 28. nov 08:00 | A | «Klarer jeg å følge det?» | Det spørsmålet får jeg oftest. | `e2-innvendingen.html` |
| E-3 | Søn 29. nov 09:00 | A | Hva som skjer på oppstartssendingen | 45 minutter som gjør starten lett. | `e3-oppstartssendingen.html` |
| E-4 | Man 30. nov 08:00 | A + B | Siste dag | Tilbudet stenger i kveld kl. 23:59. | `e4-siste-dag.html` |
| E-5 | Man 30. nov 17:00 | A | Stenger i kveld | Et par timer igjen. | `e5-siste-sjanse.html` |
| SMS-2 | Man 30. nov 20:00 | Klikket, ikke kjøpt, SMS-samtykke | – | – | se under |
| E-6 | Man 30. nov 22:30 | Klikket, ikke kjøpt (A + B) | 90 minutter igjen | Så stenger tilbudet. | `e6-90-minutter.html` |
| E-7a | Tir 1. des 09:00 | Black Week-kjøpere | Velkommen til Sterk Rygg | Her starter du. | `e7a-velkommen.html` |
| E-7b | Tir 1. des 09:00 | A, ikke kjøpt | Takk for at du fulgte med | Kampanjen er over. | `e7b-takk.html` |

A = har vært på foredraget. B = registrert, aldri deltatt.
Kjøpere tas ut av alle salgs-e-poster så snart de kjøper. Tag `black-week-2026-optout` tas ut av resten av kampanjen.

E-0 står til kl. 10:00 i planen, men Maikens frist for å svare er kl. 12:00 samme dag. Send den 13:00, eller få godkjenning før.

## SMS (bare til kontakter med dokumentert SMS-samtykke)

**SMS-1, fre 12:00**
> Hei {{first_name}}, Maiken her. Sterk Rygg for 5 490 kr + oppstartssending med meg, bare til mandag: [kort lenke]

**SMS-2, man 20:00**
> Maiken her. Sterk Rygg for 5 490 kr stenger kl. 23:59 i kveld: [kort lenke]

## Fyll inn før utsending

Søk etter disse i `build_emails.py`, bygg på nytt:

- `SESSION`: dato for oppstartssendingen, nå «onsdag 9. desember kl. 19» (bekreftet).
- `{{OPTOUT_URL}}`: lenke som setter tag `black-week-2026-optout`.
- `{{UKE1_OKT1_URL}}`: Uke 1, økt 1 i portalen (E-7a).
- `{{KALENDER_URL}}`: kalenderfil for oppstartssendingen (E-7a).
- `{{first_name}}`: bytt til flettefeltet e-postverktøyet bruker hvis det er et annet.

## Sjekk med Maiken

- E-3 lover «vi gjør den første økta sammen». Kampanjesiden sier bare portal + spørsmål. Velg én versjon.
- E-2 skriver «Torbjörn», kampanjesiden «Torbjørn». Velg én skrivemåte, og sjekk at begge har sagt ja til å bli sitert.
