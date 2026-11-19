"""Shared chrome for the redesigned pages (redesign-2026).

The redesign is built on the design-taste-frontend kit: its files are copied unedited into assets/
(system.css, system.js, ui/, motion/, layout/, moments/, icons/icon.css) and must stay byte-for-byte
the skill's copy. Page CSS lives in cmti.css and page JS in cmti.js. Lenis is vendored in vendor/.

Pages still on the old design keep using head()/header()/FOOTER in build_pages.py until they are
moved over; each redesigned page is written with write_v2().
"""
import hashlib
import os
import re

KIND = "service"

# The palette is CMTI's own (start.mjs brand), the type pairing the second one start.mjs dealt.
ROOT_TOKENS = """:root {
  --p-bg: #ffffff; --p-surface: #f3f5f8; --p-ink: #0a1f3a; --p-muted: #55657a;
  --p-accent: #195b9c; --p-accent-ink: #ffffff; --p-action: #195b9c; --p-action-ink: #ffffff;
  --p-inv-bg: #0a1f3a; --p-inv-surface: #192c47; --p-inv-ink: #ffffff; --p-inv-muted: #99a3b0;
  --p-inv-accent: #ffffff; --p-inv-accent-ink: #0a1f3a; --p-inv-action: #ffffff; --p-inv-action-ink: #0a1f3a;
  --font-display: "Source Serif 4", Georgia, serif;
  --font-text: "Libre Franklin", system-ui, sans-serif;
  --display-weight: 400;
  --display-tracking: -0.02em;
  --display-tracking-xl: -0.026em;
}"""

WA_NUMBER = "918884422179"
PHONES = '<a href="tel:+918884422480">8884422480</a> / <a href="tel:+918884422179">8884422179</a>'
EMAIL = '<a href="mailto:cmtioffice@cmti.co.in">cmtioffice@cmti.co.in</a>'
ADDRESS = "4th Floor, 177/1, 7th B Main Road<br>Above Menaka Cards, Near NMKRV Women’s College<br>Jayanagar 3rd Block, Bengaluru 560011, Karnataka"
OSM = "https://www.openstreetmap.org/search?query=7th%20B%20Main%20Road%20Jayanagar%203rd%20Block%20Bengaluru"
ELEARN = "https://elearn.cmti.co.in/"
ENQUIRY = "index.html#enquiry"


def _version(root, path):
    try:
        return hashlib.md5(open(os.path.join(root, path), "rb").read()).hexdigest()[:8]
    except OSError:
        return "0"


def _icon(root, name, label):
    """A real brand mark (assets/icons, see CREDITS.txt), inlined so it takes the text colour."""
    svg = open(os.path.join(root, "assets/icons", name + ".svg"), encoding="utf-8").read()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    svg = svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" fill="currentColor" ', 1).replace(' role="img"', "")
    return f'<span class="brand-ico" aria-hidden="true">{svg}</span>'


CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>'

# Bar word, its page, its menu: columns of (label, [(link, grey line, href)]) and an optional photo card.
NAV = [
    ("Companies", "corporate.html", [
        ("Staff and workmen", [("Staff programmes", "Freshers to project heads", "corporate.html#training-participants"),
                               ("Workmen training", "Formwork, masonry, bar bending", "corporate.html#workmen")]),
        ("For L&amp;D teams", [("Content development", "SOPs and training material", "corporate.html#content-development"),
                               ("Employee assessment", "Skill gaps and priorities", "corporate.html#assessment"),
                               ("Hiring support", "Campus hiring, entry roles", "corporate.html#hiring")]),
    ], ("images/cmti/corporate-staff-group.webp", "Staff from a CMTI capability development programme outside their office", 1455, 1091,
        "Programmes at project sites", "Across India, online and hybrid", "corporate.html")),
    ("Courses", "cacm.html", [
        ("Certified courses", [("Construction management", "CACM, three months", "cacm.html"),
                               ("Interior design", "IDM, three months", "idmti.html")]),
        ("Other programmes", [("Internships", "Exposure on live projects", "cacm.html#internship"),
                              ("Construction software", "Drawings, estimates, planning", "cacm.html#construction-software"),
                              ("BIM design software", "Model-based design", "cacm.html#bim-design")]),
    ], ("images/cmti/site-visit-group.webp", "CACM students in hard hats on a construction site visit", 1600, 1200,
        "Courses with site visits", "Offline, online and hybrid", "cacm.html")),
    ("Colleges", "colleges.html", None, None),
    ("E-learning", "e-learning.html", [
        ("Learn online", [("Online courses", "76 self-paced courses", "e-learning.html"),
                          ("Webinars", "Saturdays at 7:00 PM IST", "e-learning.html#webinars")]),
    ], None),
    ("About", "about.html", [
        ("CMTI", [("About CMTI", "Story, mentor and team", "about.html"),
                  ("Mission and vision", "What guides CMTI", "vision-mission.html"),
                  ("Clients", "Firms we have trained", "about.html#clients")]),
        ("Recognition", [("Awards", "ISDA Infracon 2025", "awards.html"),
                         ("Associations", "ACCE, ICI, IPA, IGBC", "associations.html"),
                         ("Testimonials", "Participant videos", "testimonials.html")]),
    ], None),
]


def nav_v2(current=None):
    items = []
    for word, href, cols, card in NAV:
        cur = ' aria-current="page"' if current == href else ""
        if not cols:
            items.append(f'<div class="nav__item"><a class="nav__link" href="{href}"{cur}>{word}</a></div>')
            continue
        menu = "".join(
            f'<div class="menu-col span-3"><p class="t-label">{label}</p>' +
            "".join(f'<a href="{h}">{name}<span>{line}</span></a>' for name, line, h in links) + "</div>"
            for label, links in cols)
        if card:
            img, alt, iw, ih, title, line, chref = card
            start = " start-10" if len(cols) == 2 else ""
            menu += (f'<a class="menu-card span-3{start}" href="{chref}"><div class="panel"><img class="frame__img" src="{img}" alt="{alt}" width="{iw}" height="{ih}" loading="lazy" data-sizes="300px"></div>'
                     f'<span class="t-card">{title}</span><span class="t-small muted">{line}</span></a>')
        items.append(f'<div class="nav__item"><a class="nav__link" href="{href}"{cur}>{word} {CHEV}</a>'
                     f'<div class="nav__menu" data-lenis-prevent><div class="wrap grid">{menu}</div></div></div>')
    return f'''<header class="nav">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">Skip to content</a>
    <a class="nav__logo" href="index.html"><img src="cmti-logo-nav.webp" alt="CMTI, Construction Management Training Institute" width="368" height="216"></a>
    <nav class="nav__links" aria-label="Main" data-lenis-prevent>
      {"".join(items)}
    </nav>
    <div class="nav__actions">
      <a class="nav__link" href="{ELEARN}">E-learning login</a>
      <a class="btn btn--primary" href="{ENQUIRY}">Send an enquiry</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
  </div>
</header>'''


SOCIAL = [
    ("whatsapp", "CMTI on WhatsApp", "https://whatsapp.com/channel/0029Va4S47dEgGfOPitXTT2f"),
    ("linkedin", "CMTI on LinkedIn", "https://www.linkedin.com/company/cmtionline"),
    ("instagram", "CMTI on Instagram", "https://www.instagram.com/cmtionline?r=nametag"),
    ("telegram", "CMTI on Telegram", "https://t.me/joinchat/FNINrel7x3SKLBjd"),
    ("youtube", "CMTI Connect on YouTube", "https://youtube.com/c/CMTIConnect"),
]

FOOT_COLS = [
    ("Companies", [("Staff programmes", "corporate.html#training-participants"), ("Workmen training", "corporate.html#workmen"),
                   ("Content development", "corporate.html#content-development"), ("Employee assessment", "corporate.html#assessment"),
                   ("Hiring support", "corporate.html#hiring")]),
    ("Courses", [("Construction management (CACM)", "cacm.html"), ("Interior design (IDM)", "idmti.html"),
                 ("Internships", "cacm.html#internship"), ("Construction software", "cacm.html#construction-software"),
                 ("BIM design software", "cacm.html#bim-design")]),
    ("Learn", [("College MoUs", "colleges.html"), ("Online courses", "e-learning.html"), ("Webinars", "e-learning.html#webinars"),
               ("CMTI Android app", "https://qrgo.page.link/SxLYw")]),
    ("About", [("About CMTI", "about.html"), ("Mission and vision", "vision-mission.html"), ("Clients", "about.html#clients"),
               ("Awards", "awards.html"), ("Associations", "associations.html"), ("Testimonials", "testimonials.html")]),
]


def footer_v2(root, close_h2, close_line):
    cols = "".join(f'<div class="span-3 footer__col"><h3>{t}</h3><ul>' +
                   "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in links) + "</ul></div>" for t, links in FOOT_COLS)
    socials = "".join(f'<a href="{u}" aria-label="{n}">{_icon(root, i, n)}</a>' for i, n, u in SOCIAL)
    return f'''<footer class="footer closing footer--visit g2" id="contact" aria-labelledby="close-h">
  <div class="wrap">
    <div class="closing__cta close--type">
      <div class="section-head">
        <h2 id="close-h">{close_h2}</h2>
        <p>{close_line}</p>
      </div>
      <a class="btn btn--primary btn--xl btn--wide" href="{ENQUIRY}">Send an enquiry{ARROW}</a>
    </div>
    <div class="closing__links">
      <div class="grid">
        <div class="span-6 stack-4">
          <address class="footer__address">{ADDRESS}</address>
          <p><a class="link" href="{OSM}">Get directions</a></p>
        </div>
        <div class="span-6 start-7 stack-4">
          <h3>Call or write</h3>
          <p>{PHONES}<br>{EMAIL}</p>
          <div class="socials">{socials}</div>
        </div>
      </div>
      <div class="grid footer__cols">{cols}</div>
      <div class="footer__legal">
        <span>&copy; 2026 CMTI Construction Management Training Institute Pvt Limited &nbsp; GSTIN: 29AAJCC1709L1ZE &nbsp; CIN: U74999KA2020PTC142113 &nbsp; <a href="privacy-policy.html">Privacy Policy</a></span>
        <span class="credits">Icons via Simple Icons and SVG Logos. Product names and logos are trademarks of their owners.</span>
      </div>
    </div>
  </div>
</footer>'''




def actionbar(root):
    return f'''<nav class="actionbar" aria-label="Quick actions">
  <a class="btn btn--primary" href="{ENQUIRY}">Send an enquiry</a>
</nav>'''


def wa_icon(root):
    return _icon(root, "whatsapp", "WhatsApp")


def add_srcset(root, html):
    """Give each photograph that has an 800px copy (name-800.webp) a srcset, so a phone loads the small file."""
    def fix(m):
        tag, src = m.group(0), m.group(1)
        small = src[:-5] + "-800.webp"
        if "srcset=" in tag or "data-full" in tag or 'fetchpriority="high"' in tag or not os.path.exists(os.path.join(root, small)):
            return tag
        given = re.search(r' data-sizes="([^"]+)"', tag)
        if given:
            tag = tag.replace(given.group(0), "")
        w = re.search(r'width="(\d+)"', tag)
        sizes = given.group(1) if given else "(max-width: 1023px) 100vw, 50vw"
        tiny = src[:-5] + "-400.webp"
        set_ = (f"{tiny} 400w, " if os.path.exists(os.path.join(root, tiny)) else "") + f"{small} 800w, {src} {w.group(1) if w else 1600}w"
        return tag.replace(f'src="{src}"', f'src="{src}" srcset="{set_}" sizes="{sizes}"', 1)
    return re.sub(r'<img [^>]*?src="(images/[a-z0-9/-]+\.webp)"[^>]*>', fix, html)


def head_v2(root, title, desc, moments=(), preload_img=None, diagrams=False, preload_set=None):
    mo = ""
    if moments:
        mo = ("<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>\n"
              '<link rel="modulepreload" href="assets/moments/moments.js"><link rel="modulepreload" href="assets/moments/lib.js">\n' +
              "".join(f'<link rel="modulepreload" href="assets/moments/{m}/moment.js">' for m in moments) + "\n")
    pre = ""
    if preload_img:
        small = preload_img[:-5] + "-800.webp"
        phone, small = preload_img[:-5] + "-phone.webp", preload_img[:-5] + "-800.webp"
        if preload_set:
            ss = f' imagesrcset="{preload_set[0]}" imagesizes="{preload_set[1]}"'
        elif os.path.exists(os.path.join(root, phone)):
            ss = f' imagesrcset="{phone} 567w, {preload_img} 1600w" imagesizes="(max-width: 639px) 342px, 1280px"'
        elif os.path.exists(os.path.join(root, small)):
            ss = f' imagesrcset="{small} 800w, {preload_img} 1600w" imagesizes="100vw"'
        else:
            ss = ""
        pre = f'<link rel="preload" as="image" href="{preload_img}"{ss} fetchpriority="high">\n'
    return f'''<!doctype html>
<html lang="en" data-type="{KIND}" data-radius="soft" data-buttons="block" data-motion>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="images/cmti/rebar-inspection.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="cmti-logo.webp" type="image/webp">
<meta name="theme-color" content="#ffffff">
<!-- TODO(CMTI): <link rel="canonical" href="https://[CMTI's domain]/"> once the domain is confirmed; og:image then becomes a 1200x630 share.jpg -->
<meta name="site-kind" content="other">
<meta name="page-type" content="{KIND}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400..700&family=Libre+Franklin:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/system.css?v={_version(root, 'assets/system.css')}">
<link rel="stylesheet" href="assets/ui/cards.css">
<link rel="stylesheet" href="assets/motion/motion.css">
<link rel="stylesheet" href="assets/layout/layout.css">
<link rel="stylesheet" href="assets/icons/icon.css">
{'<link rel="stylesheet" href="assets/diagrams/diagram.css">' + chr(10) if diagrams else ""}<link rel="stylesheet" href="vendor/lenis-1.3.27/lenis.css">
<style>
{ROOT_TOKENS}
</style>
<link rel="stylesheet" href="cmti.css?v={_version(root, 'cmti.css')}">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
{mo}</head>
<body>
'''


TAIL = '''<script src="vendor/lenis-1.3.27/lenis.min.js" defer></script>
<script type="module" src="assets/system.js"></script>
<script type="module" src="assets/motion/motion.js"></script>
<script type="module" src="assets/layout/layout.js"></script>
<script src="cmti.js?v={v}" defer></script>
</body>
</html>
'''


def page_v2(root, title, desc, body, close_h2, close_line, current=None, moments=(), preload_img=None, deal="", bar=False, diagrams=False, preload_set=None):
    tail = TAIL.replace("{v}", _version(root, "cmti.js"))
    if diagrams:
        tail = tail.replace('<script src="cmti.js', '<script type="module" src="assets/diagrams/mount.js"></script>\n<script src="cmti.js')
    return (head_v2(root, title, desc, moments, preload_img, diagrams, preload_set) +
            (f"<!-- {deal} -->\n" if deal else "") +
            nav_v2(current) + '\n\n<main id="top">\n' + body + "\n</main>\n\n" +
            footer_v2(root, close_h2, close_line) + "\n\n" + (actionbar(root) + "\n" if bar else "") +
            tail)


def render_v2(root, *args, **kw):
    return add_srcset(root, page_v2(root, *args, **kw))
