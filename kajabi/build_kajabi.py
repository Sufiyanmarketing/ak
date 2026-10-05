import re, base64, sys
S = sys.argv[1]  # folder with compressed hero.webp + coach.webp
html = open('index.html').read()
css = open('assets/css/styles.css').read()

def b64(p): return 'data:image/webp;base64,' + base64.b64encode(open(p,'rb').read()).decode()

# ---------- HTML ----------
body = html.split('<body>')[1].split('<script src="assets/js/main.js"')[0]
body = body.replace('<a class="skip" href="#main">Hopp til innhold</a>\n', '')
body = body.replace('<main id="main">', '').replace('</main>', '')
body = re.sub(r'<div class="hero-photo" aria-hidden="true">\s*<img[^>]*>\s*</div>',
              '<div class="hero-photo" aria-hidden="true"><div class="kob-img kob-img-hero"></div></div>', body)
def img_div(m):
    kind = 'hero' if 'hero-anne-karin' in m.group(1) else 'coach'
    alt = m.group(2)
    attrs = f' role="img" aria-label="{alt}"' if alt else ''
    return f'<div class="kob-img kob-img-{kind}"{attrs}></div>'
body = re.sub(r'<img src="assets/img/(hero-anne-karin|coaching)\.webp" alt="([^"]*)"[^>]*>', img_div, body)
assert 'assets/' not in body, re.findall(r'assets/[^"]+', body)
ld = re.findall(r'<script type="application/ld\+json">.*?</script>', html, re.S)

# ---------- CSS scoping ----------
def scope_sel(sel):
    sel = sel.strip()
    if sel.startswith('html'): return None
    if sel.startswith('.no-js') or sel.startswith('.site-header.is-scrolled') or sel == '.skip' or sel.startswith('.skip:'): return None
    if sel == ':root' or sel == 'body': return '.kob'
    if sel.startswith('*'): return '.kob ' + sel
    if sel.startswith('.nav-open'): return '.kob.nav-open' + sel[len('.nav-open'):]
    if sel.startswith('.reveal'): return '.kob.kob-js ' + sel
    return '.kob ' + sel

def scope_block(text):
    out, i = [], 0
    while i < len(text):
        j = text.find('{', i)
        if j < 0: out.append(text[i:]); break
        head = text[i:j]
        # find matching brace
        depth, k = 1, j + 1
        while depth:
            if text[k] == '{': depth += 1
            elif text[k] == '}': depth -= 1
            k += 1
        inner = text[j+1:k-1]
        h = head.strip()
        # keep comments preceding
        comments = re.findall(r'/\*.*?\*/', head, re.S)
        h = re.sub(r'/\*.*?\*/', '', h, flags=re.S).strip()
        if h.startswith('@media'):
            out.append('\n' + h + ' {' + scope_block(inner) + '}\n')
        else:
            sels = [scope_sel(s) for s in h.split(',')]
            sels = [s for s in sels if s]
            if sels:
                out.append('\n' + ', '.join(sels) + ' {' + inner + '}')
        i = k
    return ''.join(out)

css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
scoped = scope_block(css)
# header: absolute over hero instead of fixed
scoped = scoped.replace('position: fixed; inset: 0 0 auto; z-index: 50;', 'position: absolute; inset: 0 0 auto; z-index: 50;')
scoped = re.sub(r'(\.kob \.[\w-]+-photo) img\b', r'\1 .kob-img', scoped)

extra = """
/* Bilder – bytt url(...) med egne bilder lastet opp i Kajabi */
.kob { --img-hero: url(%s); --img-coach: url(%s); }
.kob .kob-img { background-repeat: no-repeat; background-size: cover; }
.kob .kob-img-hero { background-image: var(--img-hero); background-position: 50%% 15%%; }
.kob .kob-img-coach { background-image: var(--img-coach); background-position: 50%% 30%%; }
.kob .about-photo .kob-img { background-position: 50%% 10%%; }
.kob { position: relative; overflow-x: clip; }
.kob a { text-decoration: none; }
.kob .link-light, .kob .nav a:not(.btn) { text-decoration: none; }
.kob .link-light { text-decoration: underline; text-underline-offset: 5px; }
.kob ul, .kob ol { margin-top: 0; }
.kob figure { margin: 0; }
""" % (b64(S + '/hero.webp'), b64(S + '/coach.webp'))

js = """
(function () {
  var root = document.querySelector('.kob');
  if (!root) return;
  root.classList.add('kob-js');

  var sticky = root.querySelector('[data-sticky-cta]');
  var hero = root.querySelector('.hero');
  var finalCta = root.querySelector('.final-cta');
  function onScroll() {
    if (!sticky || !hero) return;
    var heroBottom = hero.getBoundingClientRect().bottom;
    var atEnd = finalCta && finalCta.getBoundingClientRect().top < window.innerHeight;
    sticky.classList.toggle('is-visible', heroBottom < 100 && !atEnd);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = root.querySelector('[data-nav-toggle]');
  var nav = root.querySelector('[data-nav]');
  function setNav(open) {
    root.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Lukk meny' : '\\u00c5pne meny');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setNav(!root.classList.contains('nav-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
  }

  var items = root.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  var faqs = root.querySelectorAll('.faq details');
  faqs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) faqs.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  var year = root.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
"""

out = f"""<!-- ==========================================================
  Kunsten å overbevise – Krystallklart budskap
  Lim inn hele denne koden i en «Custom Code»-blokk i Kajabi.
  Tips: skjul Kajabi-sidens egen header/footer, og sett blokkens
  padding til 0 og bredde til full bredde.
========================================================== -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">

<style>

{scoped}
{extra}
</style>

<div class="kob" lang="nb">
{body.strip()}
</div>

{chr(10).join(ld)}

<script>{js}</script>
"""
open('kajabi/kajabi-landing.html', 'w').write(out)
print(len(out))
