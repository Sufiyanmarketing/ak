# Kunsten å overbevise – landingsside

Statisk landingsside for Krystallklart budskap. Åpne `index.html` i nettleseren, eller kjør `npx serve .`.

- `index.html` – innhold, SEO-metadata og strukturerte data (Course + FAQPage)
- `assets/css/styles.css` – design (navy / cyan / kobber)
- `assets/js/main.js` – meny, sticky CTA, scroll-animasjoner, FAQ
- `assets/img/` – bilder

## Før lansering
- Bytt plassholderbildene i `assets/img/` (`hero-anne-karin.webp`, `coaching.webp`) med ekte foto av Anne Karin.
- Legg inn lenke til PDF-presentasjonen («Last ned presentasjonen», merket `TODO` i `index.html`).
- Seksjonen «Hva tidligere deltakere sier» er kommentert ut – fyll inn ekte sitater og fjern kommentaren.
- Oppdater `canonical`-URL og `og:image` (absolutt URL) til endelig domene.

## Kajabi
`kajabi/kajabi-landing.html` er en selvstendig versjon (HTML + CSS + JS + bilder i én fil) som limes inn i en «Custom Code»-blokk i Kajabi. All CSS er avgrenset til `.kob`, så den ikke kolliderer med Kajabi-temaet. Bytt bilder ved å endre `--img-hero` / `--img-coach` øverst i `<style>`.

## Salgsside (ny design)
`sales-page.html` er en selvstendig salgsside (HTML + CSS + JS i én fil) bygget etter det nye referansedesignet, med bildene hentet direkte fra Kajabi/CDN. All CSS er avgrenset til `.ks`, så innholdet i `<div class="ks">` (sammen med `<style>` og `<script>`) kan også limes inn i en «Custom Code»-blokk i Kajabi.
- «Last ned presentasjonen» peker foreløpig til `#` (merket `TODO`) – legg inn lenken til PDF-en.
