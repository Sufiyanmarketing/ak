#!/usr/bin/env python3
"""Bygger Black Week-e-postene (HTML) for Sterk Rygg.

Kjor:  python3 emails/build_emails.py
Resultat: emails/out/*.html + emails/out/index.html (forhandsvisning)

Designet folger kampanjesiden (black-week-checkout.html):
mork header, rosa aksent, kremfarget bakgrunn, hvitt innholdskort.
Alt er tabellbasert med inline-stiler, slik e-postklienter krever.
"""
import html
import os

# ---------------------------------------------------------------- innstillinger
CAMPAIGN_URL = "https://www.naprapatmaiken.no/black-week"
SESSION = "onsdag 9. desember kl. 19"          # bekreftet
DEADLINE = "23:59"
OPTOUT_URL = "{{OPTOUT_URL}}"                  # lenke som setter tag black-week-2026-optout
WEEK1_URL = "{{UKE1_OKT1_URL}}"                # lenke til Uke 1, okt 1 i portalen
CALENDAR_URL = "{{KALENDER_URL}}"              # .ics / kalenderlenke til oppstartssendingen
IMG_URL = ("https://kajabi-storefronts-production.s3.amazonaws.com/file-uploads/"
           "sites/171479/images/6ae4f24-c220-4b1f-6f2-7234c172365_download_7_.jpeg")

INK, SOFT, MUTED = "#1F1A24", "#4A4350", "#7A7280"
PINK, PINK_DARK, PINK_SOFT = "#FF66C4", "#E04EAB", "#FFD9F0"
DARK, CREAM, LINE = "#0F0C13", "#FAF6F4", "#EBE3E3"
SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"
SANS = "Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"


def link(url, code):
    """Legger paa UTM-parametre paa kampanjelenker."""
    if not url.startswith("http"):
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=email&utm_medium=email&utm_campaign=black-week-2026&utm_content={code.lower()}"


# ---------------------------------------------------------------- byggeklosser
def p(text, size=17, color=SOFT, mt=0):
    return (f'<p style="margin:{mt}px 0 16px;font-family:{SANS};font-size:{size}px;'
            f'line-height:1.6;color:{color};">{text}</p>')


def h(text, size=24):
    return (f'<h2 style="margin:0 0 16px;font-family:{SERIF};font-size:{size}px;'
            f'line-height:1.25;font-weight:700;color:{INK};">{text}</h2>')


def bullets(items):
    rows = "".join(
        f'<tr><td valign="top" style="padding:7px 12px 7px 0;width:24px;">'
        f'<div style="width:22px;height:22px;border-radius:11px;background:{PINK_DARK};color:#fff;'
        f'font-family:{SANS};font-size:12px;font-weight:700;line-height:22px;text-align:center;">&#10003;</div></td>'
        f'<td style="padding:7px 0;font-family:{SANS};font-size:16px;line-height:1.5;color:{SOFT};'
        f'border-bottom:1px solid {LINE};">{i}</td></tr>' for i in items)
    return f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin:4px 0 20px;">{rows}</table>'


def numbered(items):
    out = ""
    for n, (title, body) in enumerate(items, 1):
        out += (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" '
                f'style="margin:0 0 12px;background:{CREAM};border:1px solid {LINE};border-radius:14px;">'
                f'<tr><td style="padding:16px 18px;font-family:{SANS};">'
                f'<div style="font-size:11px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;color:{PINK_DARK};">{n}</div>'
                f'<div style="margin-top:4px;font-size:17px;font-weight:700;color:{INK};">{title}</div>'
                f'<div style="margin-top:4px;font-size:15px;line-height:1.55;color:{SOFT};">{body}</div>'
                f'</td></tr></table>')
    return out


def cta(text, url, code):
    u = html.escape(link(url, code))
    text = text.replace("5 490 kr", "5&nbsp;490&nbsp;kr")
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin:8px 0 22px;">'
            f'<tr><td align="center">'
            f'<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{u}" style="height:56px;v-text-anchor:middle;width:360px;" arcsize="25%" fillcolor="{PINK_DARK}" stroke="f"><center style="color:#ffffff;font-family:Arial,sans-serif;font-size:18px;font-weight:bold;">{text}</center></v:roundrect><![endif]-->'
            f'<!--[if !mso]><!-->'
            f'<a href="{u}" style="display:inline-block;background:{PINK_DARK};color:#ffffff;font-family:{SANS};'
            f'font-size:18px;font-weight:700;line-height:1.3;padding:17px 30px;border-radius:14px;text-decoration:none;">{text}</a>'
            f'<!--<![endif]--></td></tr></table>')


def offer_box(code, closing):
    """Prisboks i samme stil som prisblokken paa kampanjesiden."""
    perk = (lambda t: f'<td width="50%" style="padding:4px;"><div style="background:{DARK};border-radius:12px;'
            f'padding:12px;font-family:{SANS};font-size:14px;font-weight:600;color:#ffffff;text-align:center;">{t}</div></td>')
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" '
            f'style="margin:8px 0 22px;border:2px solid {PINK};border-radius:20px;background:#ffffff;">'
            f'<tr><td style="background:{PINK_DARK};border-radius:18px 18px 0 0;padding:12px;text-align:center;'
            f'font-family:{SANS};font-size:12px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;color:#ffffff;">'
            f'&#128420; Black Week-pris</td></tr>'
            f'<tr><td style="padding:20px 20px 4px;text-align:center;font-family:{SANS};">'
            f'<div style="font-size:15px;color:{MUTED};">Vanlig pris <s>6&nbsp;990 kr</s></div>'
            f'<div style="font-family:{SERIF};font-size:52px;font-weight:800;line-height:1.1;color:{INK};margin:6px 0;">'
            f'5&nbsp;490 <span style="font-size:20px;color:{MUTED};">kr</span></div>'
            f'<div style="display:inline-block;background:{PINK_SOFT};color:#B83585;font-size:14px;font-weight:800;'
            f'padding:6px 14px;border-radius:100px;">1&nbsp;500 kr lavere enn vanlig</div></td></tr>'
            f'<tr><td style="padding:14px 16px 4px;"><table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>'
            f'{perk("&#127909; Oppstartssending<br>live med Maiken")}{perk("&#8987; 6 måneders<br>tilgang")}'
            f'</tr></table></td></tr>'
            f'<tr><td style="padding:12px 20px 0;">{cta("Bli med i Sterk Rygg for 5 490 kr", CAMPAIGN_URL, code)}</td></tr>'
            f'<tr><td style="padding:0 20px 18px;text-align:center;font-family:{SANS};font-size:13px;color:{MUTED};">'
            f'{closing} &middot; 14 dagers garanti</td></tr></table>')


def deadline_bar(text):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin:0 0 22px;">'
            f'<tr><td style="background:{DARK};border-radius:14px;padding:14px 18px;text-align:center;'
            f'font-family:{SANS};font-size:15px;font-weight:700;color:#ffffff;">'
            f'<span style="color:{PINK};">&#9679;</span>&nbsp; {text}</td></tr></table>')


def quote(text, who):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin:4px 0 20px;">'
            f'<tr><td style="border-left:3px solid {PINK};padding:4px 0 4px 18px;">'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:18px;line-height:1.5;color:{INK};">«{text}»</div>'
            f'<div style="margin-top:8px;font-family:{SANS};font-size:14px;font-weight:700;color:{MUTED};">&mdash; {who}</div>'
            f'</td></tr></table>')


def session_card():
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" '
            f'style="margin:4px 0 22px;background:{DARK};border:2px solid {PINK};border-radius:18px;">'
            f'<tr><td style="padding:20px;font-family:{SANS};">'
            f'<div style="font-size:11px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;color:{PINK};">Bare denne uka</div>'
            f'<div style="margin-top:6px;font-family:{SERIF};font-size:22px;font-weight:700;color:#ffffff;">Oppstartssending med Maiken</div>'
            f'<div style="margin-top:6px;font-size:15px;line-height:1.55;color:#D9D3DE;">{SESSION.capitalize()} &middot; 45 minutter live. '
            f'Maiken viser deg hvor du starter i kurset og svarer på spørsmålene dine. Opptak hvis du ikke kan være med.</div>'
            f'</td></tr></table>')


def sign():
    return (f'<p style="margin:24px 0 0;font-family:{SERIF};font-style:italic;font-size:22px;color:{PINK_DARK};">'
            f'Klem fra Maiken</p>')


def header(tag):
    return (f'<tr><td style="background:{DARK};background-image:linear-gradient(180deg,#17131C,#241E2B);'
            f'border-radius:20px 20px 0 0;padding:30px 24px 28px;text-align:center;">'
            f'<div style="display:inline-block;border:1px solid #4A4350;border-radius:100px;padding:6px 14px;'
            f'font-family:{SANS};font-size:11px;font-weight:800;letter-spacing:2.4px;text-transform:uppercase;color:#ffffff;">'
            f'<span style="color:{PINK};">&#9679;</span>&nbsp; {tag}</div>'
            f'<div class="hero" style="margin-top:16px;font-family:{SANS};font-size:40px;font-weight:800;letter-spacing:6px;'
            f'line-height:1;color:#ffffff;text-transform:uppercase;">Black Week</div>'
            f'<div style="margin-top:8px;font-family:{SANS};font-size:15px;font-weight:800;letter-spacing:8px;'
            f'color:{PINK};text-transform:uppercase;">Sterk Rygg</div></td></tr>')


def photo():
    return (f'<tr><td style="padding:0;"><img src="{IMG_URL}" width="600" alt="Maiken Lund trener ved en innsjø" '
            f'style="display:block;width:100%;max-width:600px;height:auto;border:0;"></td></tr>')


def footer(campaign=True):
    opt = (f'Får du for mange e-poster nå? <a href="{OPTOUT_URL}" style="color:{PINK};">Jeg vil ikke ha e-poster om '
           f'denne kampanjen</a>, så står du fortsatt på lista mi.<br><br>' if campaign else "")
    return (f'<tr><td style="background:{DARK};border-radius:0 0 20px 20px;padding:22px 24px;text-align:center;'
            f'font-family:{SANS};font-size:13px;line-height:1.6;color:#B8B0BE;">{opt}'
            f'&copy; 2026 Maiken Lund &middot; Naprapat</td></tr>')


def kajabi_safe(doc):
    """Kajabi fjerner stil paa <div>. Gjor om alle div-er (unntatt preheader)
    til <span> (inline-block) eller <p style="margin:0">."""
    import re
    out, stack, i = [], [], 0
    for m in re.finditer(r'<div((?: class="[^"]*")?) style="([^"]*)">|</div>', doc):
        out.append(doc[i:m.start()])
        cls, style = m.group(1), m.group(2)
        if m.group(0) == "</div>":
            out.append(f"</{stack.pop()}>")
        elif cls == ' class="preheader"':
            out.append(m.group(0)); stack.append("div")
        elif "display:inline-block" in style:
            out.append(f'<span{cls} style="{style}">'); stack.append("span")
        else:
            out.append(f'<p{cls} style="margin:0;{style}">'); stack.append("p")
        i = m.end()
    out.append(doc[i:])
    return "".join(out)


def page(subject, preview, tag, body, with_photo=False, campaign=True):
    pre = html.escape(preview) + "&#847;&zwnj;&nbsp;" * 15
    return kajabi_safe(f"""<!doctype html>
<html lang="nb" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<title>{html.escape(subject)}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  body{{margin:0;padding:0;background:{CREAM};}}
  a{{color:{PINK_DARK};}}
  @media (max-width:620px){{ .wrap{{width:100%!important;}} .pad{{padding:24px 20px!important;}} .hero{{font-size:30px!important;letter-spacing:3px!important;}} }}
</style>
</head>
<body style="margin:0;padding:0;background:{CREAM};">
<div class="preheader" style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">{pre}</div>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background:{CREAM};">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" cellpadding="0" cellspacing="0" width="100%" style="width:100%;max-width:600px;background:#ffffff;border-radius:20px;">
{header(tag)}
{photo() if with_photo else ""}
<tr><td class="pad" style="padding:32px 36px;">
{body}
</td></tr>
{footer(campaign)}
</table>
</td></tr></table>
</body></html>
""")


HI = p("Hei {{first_name}}.", color=INK)
CLOSE = f"Stenger mandag kl. {DEADLINE}"

# ---------------------------------------------------------------- e-postene
EMAILS = [
    dict(code="K-1", file="k1-novemberkjopere", when="Tor 26. nov kl. 10:00",
         to="Alle som kjøpte Sterk Rygg 1.–26. nov (tag black-week-2026-buyer)",
         subject="Du får noe ekstra fra meg", preview="Fordi du ble med i november.",
         tag="Til deg som ble med", campaign=False,
         body=HI + p("Fredag starter jeg en Black Week-kampanje for de som har vært på foredraget mitt, men ikke blitt med i Sterk Rygg ennå. Du ble med før det, og da skal ikke du komme dårligere ut.")
         + p("Derfor får du det samme ekstra som de som blir med denne uka:")
         + session_card()
         + bullets(["<b>6 måneders tilgang</b> i stedet for 4. Det er allerede satt på kontoen din."])
         + p("Du trenger ikke gjøre noe. Lenken til sendingen kommer på e-post.") + sign()),

    dict(code="E-0", file="e0-forvarsel", when="Ons 25. nov kl. 10:00 (anbefalt 13:00, etter Maikens frist kl. 12)",
         to="A + B", subject="Fredag åpner jeg noe for deg",
         preview="Bare for deg som har vært på foredraget mitt.", tag="Bare for lista",
         body=HI + p("Du har vært på foredraget mitt om ryggen, og fredag åpner jeg noe som bare går ut til deg og de andre på lista mi.")
         + p("Det kommer ikke i annonser, og det ligger ikke på nettsiden.")
         + deadline_bar("Mer om det fredag morgen")
         + p("Mellom fredag og mandag sender jeg flere e-poster enn jeg pleier. Vil du stå over akkurat denne kampanjen, kan du trykke på lenken nederst. Da står du fortsatt på lista mi, og får vanlige e-poster fra meg etterpå.")
         + sign()),

    dict(code="E-1", file="e1-apning", when="Fre 27. nov kl. 07:00", to="A + B",
         subject="Black Week: Sterk Rygg for 5 490 kr", preview="Og to ting du bare får denne uka.",
         tag="Åpent nå", with_photo=True,
         body=HI + p(f"Fra nå og fram til mandag kl. {DEADLINE} kan du bli med i Sterk Rygg for 5 490 kr. Det er 1 500 kr lavere enn vanlig.")
         + p("I tillegg får du to ting som bare finnes denne uka:")
         + numbered([("Oppstartssending med meg", f"{SESSION.capitalize()}. 45 minutter live, der jeg viser deg hvor du starter i kurset, og svarer på spørsmålene dine. Opptak hvis du ikke kan være med."),
                     ("6 måneders tilgang", "i stedet for 4.")])
         + p("Sterk Rygg er ryggkurset mitt på 9 uker. Uke for uke viser jeg deg SBI-metoden, øvelsene jeg selv bygget ryggen opp igjen med etter prolapsen min: styrke i kjernemusklene, bevegelighet og ro i kroppen. Du trener hjemme, i ditt tempo, og møter meg på live-sendinger underveis.", mt=8)
         + p("Dette tilbudet går bare til lista mi. Foredraget og salgssiden går som vanlig med vanlig pris.")
         + offer_box("E-1", CLOSE)
         + p("Du har 14 dagers garanti som vanlig. Passer det ikke for deg, får du pengene tilbake.")
         + p(f"Tilbudet stenger mandag kl. {DEADLINE}.") + sign()),

    dict(code="E-2", file="e2-innvendingen", when="Lør 28. nov kl. 08:00", to="A",
         subject="«Klarer jeg å følge det?»", preview="Det spørsmålet får jeg oftest.", tag="Black Week",
         body=HI + p("Når jeg snakker med de som vurderer Sterk Rygg, er det ett spørsmål som går igjen: «Klarer jeg å følge det, sånn helt alene hjemme?»")
         + p("Det er et godt spørsmål. Mange har fått øvelser før, på et ark fra fysioterapeuten, og så har arket blitt liggende.")
         + p("Torbjörn sa det sånn da jeg snakket med ham i sommer:")
         + quote("Det er alltid lettere å se det visuelt og følge med, enn å bare se det på en skisse. Og så er det lettere å motivere seg når man kan gjøre det i lag med noen.", "Torbjörn")
         + p("Det er derfor kurset er bygget som det er. Du gjør øvelsene sammen med meg på video, uke for uke, med tre faste økter i uka. Du begynner helt nede, og øker gradvis. Rigmor sa det så fint:")
         + quote("Du må ingenting. Ta det som er komfortabelt for deg.", "Rigmor")
         + p("Og denne uka får du noe ekstra: en oppstartssending med meg, der jeg viser deg nøyaktig hvor du starter. Da slipper du å lure på det.")
         + offer_box("E-2", CLOSE) + sign()),

    dict(code="E-3", file="e3-oppstartssendingen", when="Søn 29. nov kl. 09:00", to="A",
         subject="Hva som skjer på oppstartssendingen", preview="45 minutter som gjør starten lett.",
         tag="Oppstartssendingen",
         body=HI + p(f"Jeg vil fortelle deg hva du faktisk får på oppstartssendingen {SESSION}, for den er det viktigste i tilbudet denne uka.")
         + numbered([("Portalen", "Jeg viser deg hvor uke 1 ligger, hvilke økter du gjør først, og hva du kan la ligge til senere."),
                     ("Første økt sammen", "Så gjør vi den første økta sammen, rolig og i ditt tempo, så du ser hvordan øvelsene skal kjennes."),
                     ("Spørsmålene dine", "Til slutt svarer jeg på spørsmålene dine. Om det er noe med din rygg du lurer på, eller hvordan du får plass til tre økter i uka, tar vi det der.")])
         + p("Kan du ikke være med live, får du opptaket.", mt=8)
         + p("Sammen med 6 måneders tilgang betyr det at du har god tid til å komme i gang, og noen å spørre når du gjør det.")
         + offer_box("E-3", f"Stenger i morgen kl. {DEADLINE}") + sign()),

    dict(code="E-4", file="e4-siste-dag", when="Man 30. nov kl. 08:00", to="A + B",
         subject="Siste dag", preview=f"Tilbudet stenger i kveld kl. {DEADLINE}.", tag="Siste dag",
         body=HI + p("I dag er siste dag du kan bli med i Sterk Rygg for 5 490 kr.")
         + p("Du får:")
         + bullets(["<b>Sterk Rygg</b>, ryggkurset mitt på 9 uker",
                    f"<b>Oppstartssending med meg</b> {SESSION}",
                    "<b>6 måneders tilgang</b> i stedet for 4",
                    "<b>14 dagers garanti</b>"])
         + deadline_bar(f"Stenger i kveld kl. {DEADLINE}")
         + p(f"I kveld kl. {DEADLINE} stenger tilbudet, og prisen er 6 990 kr igjen. Oppstartssendingen og de ekstra månedene får du bare denne uka.")
         + offer_box("E-4", f"Stenger i kveld kl. {DEADLINE}") + sign()),

    dict(code="E-5", file="e5-siste-sjanse", when="Man 30. nov kl. 17:00", to="A",
         subject="Stenger i kveld", preview="Et par timer igjen.", tag="Stenger i kveld",
         body=HI + p(f"Black Week-tilbudet stenger i kveld kl. {DEADLINE}.")
         + p("Har du lurt på om du skal ta steget, er dette en god dag. Du får oppstartssendingen med meg, så du vet hvor du skal begynne, og 14 dagers garanti hvis det ikke passer.")
         + offer_box("E-5", f"Stenger i kveld kl. {DEADLINE}") + sign()),

    dict(code="E-6", file="e6-90-minutter", when="Man 30. nov kl. 22:30", to="Klikket, ikke kjøpt (A + B)",
         subject="90 minutter igjen", preview="Så stenger tilbudet.", tag="90 minutter igjen",
         body=HI + deadline_bar("Om 90 minutter stenger tilbudet")
         + cta("Bli med i Sterk Rygg for 5 490 kr", CAMPAIGN_URL, "E-6") + sign()),

    dict(code="E-7a", file="e7a-velkommen", when="Tir 1. des kl. 09:00", to="Black Week-kjøpere", campaign=False,
         subject="Velkommen til Sterk Rygg", preview="Her starter du.", tag="Velkommen",
         body=HI + p("Så fint at du er med!", color=INK)
         + p("Start her. Det er alt du trenger å gjøre i dag:")
         + cta("Uke 1, økt 1", WEEK1_URL, "E-7a")
         + session_card()
         + p(f'<a href="{CALENDAR_URL}" style="color:{PINK_DARK};font-weight:700;">Legg oppstartssendingen inn i kalenderen</a>')
         + p("Lurer du på noe før det, kan du svare på denne e-posten.") + sign()),

    dict(code="E-7b", file="e7b-takk", when="Tir 1. des kl. 09:00", to="A, ikke kjøpt", campaign=False,
         subject="Takk for at du fulgte med", preview="Kampanjen er over.", tag="Takk",
         body=HI + p("Black Week-kampanjen er over, og jeg vil bare si takk for at du leste med.")
         + p("Jeg fortsetter å sende deg e-poster om rygg og trening som vanlig. Og vil du se foredraget mitt igjen, går det hver lørdag kl. 10.")
         + sign()),
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    cards = ""
    for i, e in enumerate(EMAILS):
        doc = page(e["subject"], e["preview"], e["tag"], e["body"],
                   with_photo=e.get("with_photo", False), campaign=e.get("campaign", True))
        with open(os.path.join(out, e["file"] + ".html"), "w", encoding="utf-8") as f:
            f.write(doc)
        os.makedirs(os.path.join(out, "txt"), exist_ok=True)
        with open(os.path.join(out, "txt", f"{e['code']}-{e['file']}.txt"), "w", encoding="utf-8") as f:
            f.write(f"EMNE: {e['subject']}\nFORHÅNDSVISNING: {e['preview']}\nNÅR: {e['when']}\n"
                    f"TIL: {e['to']}\n\n===== HTML (kopier alt under denne linjen) =====\n\n{doc}")
        esc = html.escape(doc)
        cards += f"""
<section class="card" id="{e['file']}">
  <div class="head"><span class="code">{e['code']}</span>
    <div><div class="when">{html.escape(e['when'])}</div><div class="to">Til: {html.escape(e['to'])}</div></div></div>
  <div class="field"><label>Emne</label>
    <div class="row"><input readonly id="s{i}" value="{html.escape(e['subject'])}"><button data-copy="s{i}">Kopier emne</button></div></div>
  <div class="field"><label>Forhåndsvisningstekst</label>
    <div class="row"><input readonly id="p{i}" value="{html.escape(e['preview'])}"><button data-copy="p{i}">Kopier</button></div></div>
  <div class="field"><label>HTML</label>
    <div class="row"><textarea readonly id="h{i}">{esc}</textarea><button class="big" data-copy="h{i}">Kopier HTML</button></div></div>
  <details><summary>Vis e-posten</summary><iframe title="{html.escape(e['subject'])}" srcdoc="{esc}" loading="lazy"></iframe></details>
</section>"""
    nav = "".join(f'<a href="#{e["file"]}">{e["code"]}</a>' for e in EMAILS)
    index = f"""<!doctype html><html lang="nb"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Black Week e-poster</title>
<style>
:root{{--ink:#1F1A24;--muted:#7A7280;--pink:#E04EAB;--line:#EBE3E3;--cream:#FAF6F4;--dark:#0F0C13;}}
*{{box-sizing:border-box}}
body{{font-family:Arial,Helvetica,sans-serif;background:var(--cream);color:var(--ink);margin:0;padding:0 16px 40px;}}
header{{max-width:880px;margin:0 auto;padding:28px 0 8px;}}
h1{{font-size:24px;margin:0 0 6px}} header p{{color:var(--muted);margin:0 0 14px}}
nav{{position:sticky;top:0;z-index:5;background:var(--dark);padding:10px;border-radius:12px;display:flex;flex-wrap:wrap;gap:6px;max-width:880px;margin:0 auto 18px;}}
nav a{{color:#fff;text-decoration:none;font-weight:700;font-size:13px;padding:6px 10px;border-radius:8px;background:#2A2433}}
.card{{max-width:880px;margin:0 auto 18px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;scroll-margin-top:70px}}
.head{{display:flex;gap:12px;align-items:center;margin-bottom:12px}}
.code{{background:var(--pink);color:#fff;font-weight:800;border-radius:10px;padding:8px 12px;font-size:15px}}
.when{{font-weight:700}} .to{{color:var(--muted);font-size:14px}}
.field{{margin-top:10px}} label{{display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:4px}}
.row{{display:flex;gap:8px;align-items:stretch}}
input,textarea{{flex:1;min-width:0;font:15px/1.4 Arial,sans-serif;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--cream);color:var(--ink)}}
textarea{{height:80px;font:12px/1.4 monospace;resize:vertical}}
button{{flex-shrink:0;background:var(--dark);color:#fff;border:0;border-radius:10px;padding:0 14px;font-weight:700;font-size:14px;cursor:pointer;min-height:44px}}
button.big{{background:var(--pink)}} button.ok{{background:#2E7D4F}}
details{{margin-top:12px}} summary{{cursor:pointer;font-weight:700;color:var(--pink)}}
iframe{{width:100%;height:900px;border:1px solid var(--line);border-radius:12px;margin-top:10px;background:var(--cream)}}
@media(max-width:560px){{.row{{flex-direction:column}} button{{min-height:44px}}}}
</style></head><body>
<header><h1>Sterk Rygg · Black Week 2026</h1>
<p>Trykk «Kopier emne» og «Kopier HTML», og lim inn i e-postverktøyet. Alle tider er Oslo-tid.</p></header>
<nav>{nav}</nav>
{cards}
<script>
document.querySelectorAll('button[data-copy]').forEach(function(b){{
  b.addEventListener('click',function(){{
    var el=document.getElementById(b.dataset.copy), t=b.textContent;
    function done(){{b.textContent='Kopiert ✓';b.classList.add('ok');setTimeout(function(){{b.textContent=t;b.classList.remove('ok');}},1800);}}
    if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(el.value).then(done,fallback);}}else{{fallback();}}
    function fallback(){{el.select();try{{document.execCommand('copy');done();}}catch(e){{}}}}
  }});
}});
</script>
</body></html>"""
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    print(f"Skrev {len(EMAILS)} e-poster til {out}")


if __name__ == "__main__":
    main()
