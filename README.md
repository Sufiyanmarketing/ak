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

## Al Anab Al Ahmer Cafeteria
`cafeteria/index.html` – single-file website for Al Anab Al Ahmer Cafeteria (Al Majaz, Sharjah). No online ordering: Call / WhatsApp buttons, full menu with category filter, and a Google Maps location section. Menu items and prices live in the `MENU` array in the page's `<script>`.
