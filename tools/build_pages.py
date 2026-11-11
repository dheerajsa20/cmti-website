"""Generate every CMTI page (index.html and the nine inner pages).

Run from the repository root:
    python3 tools/build_pages.py .

The wording comes from the original CMTI site; page structure follows the
"CMTI Website Inputs" brief. Edit text here, not in the generated .html files,
or the next run will overwrite your edits.
"""
import hashlib
import sys
from urllib.parse import quote

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
def asset_version(path):
    """Short content hash, so browsers fetch a fresh copy whenever the file changes."""
    return hashlib.sha256(open(f"{ROOT}/{path}", "rb").read()).hexdigest()[:10]

CSS_V = asset_version("site.css")
JS_V = asset_version("site.js")
GOOGLE = "https://www.google.com/maps/search/?api=1&amp;query=Construction+Management+Training+Institute+Jayanagar+Bengaluru"
WA = "918884422179"

# ---------------------------------------------------------------- icons
ICONS = {
    "users": "M16 19v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM21 19v-1a4 4 0 0 0-3-3.9M16 4.1a3 3 0 0 1 0 5.8",
    "helmet": "M3 17h18M5 17v-3a7 7 0 0 1 14 0v3M10 7V5h4v2",
    "pin": "M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Zm0-8.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z",
    "tag": "M3 12V4h8l10 10-8 8L3 12ZM7.5 7.5h.01",
    "chart": "M4 20V10M10 20V4M16 20v-7M22 20H2",
    "briefcase": "M3 8h18v12H3zM8 8V5h8v3M3 13h18",
    "book": "M4 19V5a2 2 0 0 1 2-2h14v14H6a2 2 0 0 0-2 2Zm0 0a2 2 0 0 0 2 2h14",
    "award": "M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Zm-4 0-1 7 5-3 5 3-1-7",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-13v5l3 2",
    "laptop": "M4 5h16v11H4zM2 19h20",
    "cap": "M2 9l10-5 10 5-10 5L2 9Zm4 2v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5",
    "leaf": "M5 19c0-8 5-14 15-14 0 10-6 15-14 15M5 19l7-7",
    "doc": "M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14Zm5-2 5 5",
    "building": "M4 21V5l8-2v18M12 7l8 3v11M8 9h.01M8 13h.01M8 17h.01M16 13h.01M16 17h.01M2 21h20",
    "layers": "M12 3l9 5-9 5-9-5 9-5ZM3 12l9 5 9-5M3 16l9 5 9-5",
    "target": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-5a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z",
    "eye": "M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Zm10 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z",
    "check": "M5 12l4 4 10-10",
    "handshake": "M3 12l4-4 5 2 5-2 4 4M7 8l5 6 3-2M3 12l6 6 3-2 3 2 6-6",
    "ruler": "M3 17 17 3l4 4L7 21l-4-4ZM7 13l2 2M10 10l2 2M13 7l2 2",
    "chat": "M4 5h16v11H8l-4 4V5Z",
    "shield": "M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6l8-3Z",
    "bolt": "M13 2 4 14h7l-1 8 9-12h-7l1-8Z",
    "cpu": "M7 7h10v10H7zM10 2v3M14 2v3M10 19v3M14 19v3M2 10h3M2 14h3M19 10h3M19 14h3",
    "home": "M3 11l9-7 9 7v10h-6v-6H9v6H3V11Z",
    "rupee": "M7 4h10M7 9h10M7 4c6 0 6 10 0 10l8 6",
    "scale": "M12 3v18M5 7h14M5 7l-3 7a4 4 0 0 0 6 0L5 7Zm14 0-3 7a4 4 0 0 0 6 0l-3-7ZM8 21h8",
    "monitor": "M3 4h18v12H3zM8 20h8M12 16v4",
    "play": "M8 5v14l11-7z",
}

def icon(name, cls="icon"):
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg></span>'

def enquire(programme):
    import html as _html
    return "index.html?programme=" + quote(_html.unescape(programme)) + "#contact"

def arrow_link(text, href, attrs=""):
    return f'<a class="link-arrow" href="{href}"{attrs}>{text}</a>'

# ---------------------------------------------------------------- shared chrome
NAV = [
    ("Home", "index.html", None),
    ("About Us", None, [("About Us", "about.html"), ("Mission &amp; Vision", "vision-mission.html"), ("Our Clients", "about.html#clients"),
                        ("Professional Associations", "associations.html"), ("Awards &amp; Certificates", "awards.html"), ("Testimonials", "testimonials.html")]),
    ("For Corporates", None, [("Overview", "corporate.html"), ("Capability Development Programme for Staff", "corporate.html#training-participants"),
                              ("Capability Development Programme for Workmen", "corporate.html#workmen"),
                              ("Content Development", "corporate.html#content-development"),
                              ("Assessment of Employees", "corporate.html#assessment"), ("Hiring Support", "corporate.html#hiring")]),
    ("Certified Courses", None, [("Advanced Construction Management Course (CACM)", "finishing-school.html"), ("Interior Design &amp; Management Course (IDM)", "idmti.html"),
                                ("Internships", "finishing-school.html#internship"),
                                ("Construction Software Courses", "finishing-school.html#construction-software"),
                                ("BIM Design Software", "finishing-school.html#bim-design")]),
    ("College MoUs", "colleges.html", None),
    ("E-Learning", None, [("Online Courses", "e-learning.html"), ("Webinars", "e-learning.html#webinars")]),
    ("Contact", "index.html#contact", None),
]

def header(home=False):
    items = []
    for label, href, sub in NAV:
        if sub:
            links = "".join(f'<a href="{h}">{t}</a>' for t, h in sub)
            items.append(f'<li class="has-sub"><button type="button" aria-expanded="false">{label}</button><div class="sub">{links}</div></li>')
        else:
            items.append(f'<li><a href="{href}">{label}</a></li>')
    return f'''<div class="topbar">
  <div class="topbar-inner">
    <ul>
      <li class="tb-label tb-hide">Contact us</li>
      <li><a href="tel:+918884422480">8884422480</a> / <a href="tel:+918884422179">8884422179</a></li>
      <li class="tb-hide"><a href="mailto:cmtioffice@cmti.co.in">cmtioffice@cmti.co.in</a></li>
    </ul>
    <ul class="tb-right">
      <li class="tb-label tb-hide">Follow us</li>
      <li class="tb-hide"><a href="https://www.linkedin.com/company/cmtionline/">LinkedIn</a></li>
      <li class="tb-hide"><a href="https://linktr.ee/cmti">Social channels</a></li>
    </ul>
  </div>
</div>
<header class="masthead">
  <div class="masthead-inner">
    <a class="brand" href="index.html"><img src="cmti-logo.webp" alt="Construction Management Training Institute" width="900" height="529"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="menu-bars" aria-hidden="true"></span><span class="menu-label">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main navigation">
      <ul>{"".join(items)}</ul>
      <a class="btn btn-primary" href="index.html#contact">Make an enquiry</a>
    </nav>
  </div>
</header>'''

SOCIAL = [
    # Exactly the links on https://linktr.ee/cmti (except the CMTI Website link, which is this site), plus the WhatsApp channel.
    ("WhatsApp channel", "https://whatsapp.com/channel/0029Va4S47dEgGfOPitXTT2f", "M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.6-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3Z"),
    ("LinkedIn", "https://www.linkedin.com/company/cmtionline", "M6 9h3v10H6V9Zm1.5-4.5a1.75 1.75 0 1 1 0 3.5 1.75 1.75 0 0 1 0-3.5ZM11 9h2.9v1.4c.4-.8 1.5-1.6 3.1-1.6 3 0 3.5 2 3.5 4.6V19h-3v-4.9c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5V19H11V9Z"),
    ("Instagram", "https://www.instagram.com/cmtionline?r=nametag", "M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4Zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0ZM16.6 2.5H7.4a4.9 4.9 0 0 0-4.9 4.9v9.2a4.9 4.9 0 0 0 4.9 4.9h9.2a4.9 4.9 0 0 0 4.9-4.9V7.4a4.9 4.9 0 0 0-4.9-4.9Zm3.2 14.1a3.2 3.2 0 0 1-3.2 3.2H7.4a3.2 3.2 0 0 1-3.2-3.2V7.4a3.2 3.2 0 0 1 3.2-3.2h9.2a3.2 3.2 0 0 1 3.2 3.2Z"),
    ("Telegram", "https://t.me/joinchat/FNINrel7x3SKLBjd", "M20.7 3.8 2.9 10.7c-1.2.5-1.2 1.2-.2 1.5l4.6 1.4 1.8 5.4c.2.6.4.8.9.8.4 0 .6-.2.9-.4l2.2-2.1 4.6 3.4c.8.5 1.4.2 1.6-.8l3-14.2c.3-1.2-.5-1.8-1.6-1.3ZM9.8 14.3l-.4 3.8-1.4-4.6 10.3-6.5-8.5 7.3Z"),
    ("YouTube: CMTI Connect", "https://youtube.com/c/CMTIConnect", "M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4a2.5 2.5 0 0 0-1.8 1.8A26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8ZM10 15V9l5.2 3L10 15Z"),
    ("CMTI Android Application", "https://qrgo.page.link/SxLYw", "M7 9h10v8a1 1 0 0 1-1 1h-1v3h-2v-3h-2v3H9v-3H8a1 1 0 0 1-1-1V9Zm-3 0h2v6H4V9Zm14 0h2v6h-2V9ZM7 8a5 5 0 0 1 10 0H7Zm3-2.5a.7.7 0 1 0 0 1.4.7.7 0 0 0 0-1.4Zm4 0a.7.7 0 1 0 0 1.4.7.7 0 0 0 0-1.4ZM8.2 2.8l1.2 1.6M15.8 2.8l-1.2 1.6"),
    ("CMTI E Learning Website", "https://elearn.cmti.co.in/", "M2 9l10-5 10 5-10 5L2 9Zm4 2.2v4.3c0 1.6 2.7 3 6 3s6-1.4 6-3v-4.3l-6 3-6-3Z"),
]
SOCIAL_LINKS = "".join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg></a></li>' for n, u, p in SOCIAL)

FOOTER = f'''<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <img class="footer-logo" src="cmti-logo-dark.webp" alt="CMTI" width="900" height="529">
      <address>4th Floor, 177/1, 7th B Main Road<br>Above Menaka Cards, Near NMKRV Women’s College<br>Jayanagar 3rd Block, Bengaluru 560011, Karnataka</address>
      <p style="margin-top:14px"><a href="tel:+918884422480">8884422480</a> / <a href="tel:+918884422179">8884422179</a><br><a href="mailto:cmtioffice@cmti.co.in">cmtioffice@cmti.co.in</a></p>
    </div>
    <div><h3>About Us</h3><ul><li><a href="about.html">About Us</a></li><li><a href="vision-mission.html">Mission &amp; Vision</a></li><li><a href="about.html#clients">Our Clients</a></li><li><a href="associations.html">Professional Associations</a></li><li><a href="awards.html">Awards &amp; Certificates</a></li><li><a href="testimonials.html">Testimonials</a></li></ul></div>
    <div><h3>For Corporates</h3><ul><li><a href="corporate.html">Overview</a></li><li><a href="corporate.html#training-participants">Capability Development Programme for Staff</a></li><li><a href="corporate.html#workmen">Capability Development Programme for Workmen</a></li><li><a href="e-learning.html">E-Learning</a></li></ul></div>
    <div><h3>Certified Courses</h3><ul><li><a href="finishing-school.html">Advanced Construction Management Course (CACM)</a></li><li><a href="idmti.html">Interior Design &amp; Management Course (IDM)</a></li></ul></div>
    <div><h3>CMTI</h3><ul><li><a href="colleges.html">College MoUs</a></li><li><a href="testimonials.html">Google reviews</a></li><li><a href="index.html#contact">Contact us</a></li></ul></div>
  </div>
  <div class="footer-social">
    <p class="fs-title">Follow our social media for regular updates</p>
    <ul class="social-links">{SOCIAL_LINKS}</ul>
  </div>
  <div class="footer-base"><div class="fb-inner">
    <p class="fb-rights">© 2026 CMTi. All Rights Reserved.</p>
    <p class="fb-company"><strong>CMTI Construction Management Training Institute Pvt Limited</strong><span>GSTIN: 29AAJCC1709L1ZE</span><span>CIN: U74999KA2020PTC142113</span></p>
    <p class="fb-links"><a href="privacy-policy.html">Privacy Policy</a></p>
  </div></div>
</footer>'''

WA_ICON = '<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.6-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3Z"/></svg>'
QUICK = f'''<button class="to-top" type="button" aria-label="Back to top" title="Back to top" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<div class="quick-contact">
  <a class="qc-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>
  <a class="qc-call" href="tel:+918884422179" aria-label="Call CMTI"><svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg></a>
</div>'''

def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="site.css?v={CSS_V}">
<script>document.documentElement.classList.add("js")</script>
<script src="site.js?v={JS_V}" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def write(name, title, desc, body):
    footer = FOOTER.replace('<li><a href="testimonials.html">Google reviews</a></li>', '') if name == "index.html" else FOOTER
    html = head(title, desc) + header(name == "index.html") + '\n\n<main id="main">\n' + body + '\n</main>\n\n' + footer + "\n\n" + QUICK + "\n</body>\n</html>\n"
    open(f"{ROOT}/{name}", "w", encoding="utf-8").write(html)
    print("wrote", name)

# ---------------------------------------------------------------- building blocks
def page_hero(crumb_label, eyebrow, title, lede="", img="", tags_label="", tags=(), meta="", actions="", extra="", badge=""):
    crumbs = f'<ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{crumb_label}</li></ol>'
    tags_html = (f'<p class="tags-label">{tags_label}</p>' if tags_label else "") + (
        '<ul class="tags">' + "".join(f"<li>{t}</li>" for t in tags) + "</ul>" if tags else "")
    return f'''<section class="page-hero" aria-labelledby="page-title">
  {f'<div class="page-hero-bg"><img src="{img}" alt="" width="1400" height="934"></div>' if img else ''}
  <div class="page-hero-inner">
    {crumbs}
    <div class="copy hero-copy">
      {badge}
      <p class="eyebrow">{eyebrow}</p>
      <h1 id="page-title">{title}</h1>
      {f'<p class="lede">{lede}</p>' if lede else ''}
      {tags_html}
      {f'<p class="meta">{meta}</p>' if meta else ''}
      {f'<div class="hero-actions">{actions}</div>' if actions else ''}
      {extra}
    </div>
  </div>
</section>'''

def section(inner, cls="section", sid=None, label=None):
    a = (f' id="{sid}"' if sid else "") + (f' aria-labelledby="{label}"' if label else "")
    return f'<section class="{cls}"{a}>\n<div class="container">\n{inner}\n</div>\n</section>\n'

def shead(eyebrow, title, text="", hid=None):
    return (f'<div class="section-head reveal">' + (f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else "") +
            f'<h2{f" id=\"{hid}\"" if hid else ""}>{title}</h2>' + (f"<p>{text}</p>" if text else "") + "</div>")

def card(title, text, ic=None, label="", extra="", cid="", cred=""):
    return (f'<article class="card reveal"{f" id=\"{cid}\"" if cid else ""}>' + (icon(ic) if ic else "") +
            (f'<p class="label">{label}</p>' if label else "") + f"<h3>{title}</h3>" +
            (f'<p class="cred">{cred}</p>' if cred else "") + (f"<p>{text}</p>" if text else "") + extra + "</article>")

def video(vid, title, sub, yt):
    return f'''<div class="reveal"><button class="video" type="button" data-embed="{vid}" data-title="{title}">
  <span class="thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play" aria-hidden="true"></span></span>
  <span class="cap"><strong>{title}</strong><span>{sub}</span></span>
</button><p style="margin-top:12px">{arrow_link("Watch on YouTube", yt)}</p></div>'''

def cta():
    return f'''<section class="cta-band">
  <div class="cta-inner">
    <div><h2>Let’s discuss your training needs</h2><p>We reply within one working day.</p></div>
    <div class="cta-actions"><a class="btn btn-white" href="index.html#contact">Make an enquiry</a><a class="btn btn-ghost-white" href="tel:+918884422179">Call 8884422179</a></div>
  </div>
</section>'''

CLIENTS = [(1, "png", "DLF"), (2, "png", "Godrej Properties"), (3, "png", "Hines"), (4, "png", "ISRO"),
    (5, "jpeg", "L&amp;T Institute of Project Management"), (6, "png", "Larsen &amp; Toubro"), (7, "png", "M3M"),
    (8, "png", "Prestige Group"), (9, "jpeg", "Sattva Group"), (10, "jpeg", "Signature Global"), (11, "png", "Tata Projects"),
    (12, "jpeg", "Adarsh Group"), (13, "png", "Birla Estates"), (14, "jpeg", "Blue Wing Design and Construction"),
    (15, "png", "Cemindia"), (16, "png", "Century"), (17, "jpeg", "H.G. Infra Engineering"), (18, "png", "KEC International"),
    (19, "jpeg", "KNK"), (20, "png", "Piramal Realty"), (21, "jpeg", "Ramky Estates"), (22, "jpeg", "Ramky Infrastructure"),
    (23, "png", "Riviera Infraprojects"), (24, "png", "Shapoorji Pallonji"), (25, "png", "Sowparnika"),
    (26, "jpeg", "Spartan Builders"), (27, "jpeg", "Sumadhura"), (28, "png", "Uniqcore")]

def client_marquee():
    # Brief: scroll continuously in two lines, the first ten large companies on line one in upload order.
    def row(items, cls):
        return (f'<div class="marquee {cls}"><ul class="marquee-track">' +
                "".join(f'<li><img src="client-logos/{n}.{e}" alt="{a}" loading="lazy"></li>' for n, e, a in items) + "</ul></div>")
    return ('<div class="marquee-group reveal" data-marquee-group>' + row(CLIENTS[:10], "large") + row(CLIENTS[10:], "reverse") +
            '</div>')

COLLEGES = [("bmsit", "BMSIT"), ("presidency", "Presidency University"), ("sharnbasava", "Sharnbasava University"),
    ("kpriet", "KPRIET"), ("karunya", "Karunya"), ("sona", "Sona College"), ("rgm", "RGM Nandyal"),
    ("gndec", "Gurunanak Dev, Bidar"), ("bgsit", "BGSIT"), ("gprec", "G. Pulla Reddy Engineering College"),
    ("nitte", "Nitte Meenakshi Institute of Technology")]

def college_marquee():
    return ('<div class="marquee-group reveal" data-marquee-group><div class="marquee"><ul class="marquee-track">' +
            "".join(f'<li class="college"><img src="college-logos/{f}.jpeg" alt="" loading="lazy">{n}</li>' for f, n in COLLEGES) +
            '</ul></div></div>')

MOU = [("briefcase", "Placement support and campus interviews", "Employer coordination, résumé guidance, mock interviews and campus interviews."),
    ("helmet", "Internships", "Help students find and apply for relevant industry opportunities."),
    ("check", "Competitive exams", "Preparation guidance and practice assessments."),
    ("laptop", "Software training", "On-campus practice with CAD, BIM, planning and estimation tools."),
    ("book", "Free courses", "Selected technical and career-readiness courses for students."),
    ("doc", "Curriculum development", "Boards of Studies contributions and industry input on electives, labs and projects."),
    ("users", "Practical and faculty training", "Workshops, site visits, expert lectures and webinars."),
    ("leaf", "Campus Green Audits", "Support to assess campus environmental performance and identify improvements."),
    ("award", "NBA accreditation visits", "Industry partner inputs on internships, practical training and collaboration.")]

def mou_tiles():
    """MoU benefits split by who they help: students (light) and the college (navy)."""
    def items(rows):
        return "".join(f'<li>{icon(ic)}<div><h4>{t}</h4><p>{d}</p></div></li>' for ic, t, d in rows)
    return (f'<div class="mou-split reveal">'
            f'<div class="mou-col mou-students"><h3>For your students</h3><ul>{items(MOU[:5])}</ul></div>'
            f'<div class="mou-col mou-college"><h3>For your college</h3><ul>{items(MOU[5:])}</ul></div>'
            f'</div>')

TEAM = [
    ("AK", "Founder &amp; CEO", "Er. S. G. Ashok Kumar", "PMP, IGBC AP · 26 years in construction", "Founded CMTI and established IDMTI to develop interior design professionals. He leads the CMTI Finishing School, corporate training, industry readiness programmes and partnerships. His experience includes L&amp;T highway and airport projects. He serves on the IGBC Core Committee.", "https://www.linkedin.com/in/er-ashok-kumar-b645126b/"),
    ("SD", "Co-founder &amp; Head of Operations", "Er. S. K. Deepasree", "22 years of academic experience", "Oversees the CMTI and IDMTI Finishing Schools. She leads placements, coordinates with employers, guides students through recruitment and career decisions, and manages human resources.", "https://www.linkedin.com/in/s-k-deepasree/"),
    ("SA", "Partner for Corporate Training Initiatives", "Er. Sachin Amarnath", "10 years of experience", "A project management and learning and development professional. He assesses client needs, develops content, and designs and delivers capability development programmes for project teams.", "https://www.linkedin.com/in/sachin-amarnath/"),
    ("MD", "Collaboration Partner &amp; Quality Leader", "Mr. Manish Dave", "35+ years in construction", "Supports business development and client acquisition in Gujarat. He helps develop training programmes using his expertise in construction quality and site practices.", "https://www.linkedin.com/in/manish-dave-464081296/"),
]

def team_section(cls="section", sid="team"):
    cards = "".join(
        f'<article class="card reveal leader"><h3 class="leader-name">{name}</h3><p class="label leader-role">{role}</p>'
        f'<p class="cred">{cred}</p><p>{bio}</p>{arrow_link("View LinkedIn profile", li, f" aria-label=\"View {name.split(". ",1)[-1]} on LinkedIn\"")}</article>'
        for m, role, name, cred, bio, li in TEAM)
    return section(shead("Leadership", "The team behind CMTI", hid=f"{sid}-title") + f'<div class="grid" style="--cols:4">{cards}</div>', cls, sid, f"{sid}-title")

TRAINERS = [
    ("Er. S. G. Ashok Kumar", "PMP, IGBC AP. 26 years of construction industry experience, including highway and airport projects.", "https://www.linkedin.com/in/er-ashok-kumar-b645126b/", "Founder &amp; CEO"),
    ("Sachin Amarnath", "Sachin Specializes on Project Management, Digital Construction, Real Estate, Artificial Intelligence in Construction and Risk Management", "https://www.linkedin.com/in/sachin-amarnath/", ""),
    ("K B Natarajan", "Natarajan Specializes on Construction Management, having Vast Experience in Handling the Graduate Engineer Trainees / Diploma Engineer Trainees", "https://www.linkedin.com/in/kozunjavadi-balu-natarajan-193b8754/", ""),
    ("N Balaji", "N Balaji Specializes on Construction Management having vast experience in handling Real Estate and Industrial Construction Projects", "https://www.linkedin.com/in/balaji-nachiappan-362475214/", ""),
    ("Manish Dave", "Manish Dave carries experience on Project Management, executed complex projects and held leadership positions in leading Construction Companies", "https://www.linkedin.com/in/manish-dave-464081296/", ""),
    ("Nagareddayya Subbagari", "Nagareddayya Subbagari carries rich experience on Quality Management Systems, Construction Management", "https://www.linkedin.com/in/nagareddayya-subbagari-81309318/", ""),
    ("Madhukeshwar Jaglur", "Madhukeshwar Jaglur carries rich experience on Project Management, handled Large Complex projects", "https://www.linkedin.com/in/jaglur-m-188b1316/", ""),
]

def trainer(name, text, linkedin, label):
    return card(name, text, label=label, extra=arrow_link("View LinkedIn profile", linkedin, f' aria-label="View {name} on LinkedIn"'))

def trainers_section(cls="section dark on-dark", sid="trainers"):
    return section(f'''<div class="two-col">
  <div class="reveal">
    <p class="eyebrow">People behind the programmes</p>
    <h2 id="{sid}-title">Our trainer network</h2>
  </div>
  <div class="reveal">
    <p class="lead" style="color:#fff">CMTI works with <strong>50+ construction and real estate practitioners</strong>, most of whom are former L&amp;T professionals. They use real project examples to connect training with on-site practice.</p>
    <p>Trainers are based in Delhi NCR, Gujarat, Karnataka, Pune, Hyderabad and Chennai, and travel to project sites and training venues as required.</p>
    <p><a class="link-arrow" style="color:#fff" href="{enquire("Trainer Profiles")}">Request trainer profiles for your programme</a></p>
  </div>
</div>
<div class="grid trainer-grid" style="--cols:4;margin-top:48px">
  {"".join(trainer(*t) for t in TRAINERS)}
</div>''', cls, sid, f"{sid}-title")

NITI = '''<aside class="panel reveal">
  <h3>Construction skills for a developed India</h3>
  <p>NITI Aayog’s August 2026 skilling report emphasises flexible, lifelong learning aligned with industry needs. In construction, foundational skilling helps new entrants read drawings, measure work and follow site procedures. Reskilling helps experienced professionals move into roles that use BIM, digital quality tools and new construction methods. Upskilling helps project teams improve planning, safety, quality and resource efficiency as India builds towards Viksit Bharat 2047.</p>
  <p class="muted">Source inspiration: NITI Aayog, <cite>Reimagining Skilling for Viksit Bharat@2047</cite>, August 2026.</p>
</aside>'''

ABOUT_CARDS = ('<div class="grid" style="--cols:2;margin-top:40px">' +
    card("Corporate, Government and International Training", "CMTI is a technical training partner to real estate and engineering, procurement and construction (EPC) companies. It delivers capability development programmes at project sites across India, has trained the Indian Space Research Organisation (ISRO), and delivered an international programme for Towell Group in Manchester, UK.", "building", extra=arrow_link("Explore corporate training", "corporate.html")) +
    card("College Trainings and Placements", "On-campus and off-campus training, internship support and campus interviews for engineering students. CMTI partners with <strong>100+ engineering colleges</strong>, has placed <strong>5,000+ engineers</strong> in construction and interiors roles, and works with <strong>300+ companies</strong> across construction, real estate, interiors and BIM.", "cap", extra=arrow_link("Explore college partnerships", "colleges.html")) +
    "</div>")

PROGRAMME_GROUPS = [
    ("Certified Courses", ["Advanced Construction Management Course (CACM)", "Interior Design &amp; Management Course (IDM)", "Internships", "Construction Software Courses", "BIM Design Software"]),
    ("For Corporates", ["Capability Development Programme for Staff", "Capability Development Programme for Workmen", "Content Development", "Assessment of Employees", "Hiring Support", "Trainer Profiles"]),
    ("Other", ["College MoU", "E-Learning and Webinars", "Something else"]),
]

# ================================================================ HOME
home = f'''<section class="hero" aria-labelledby="hero-title">
  <div class="hero-bg"><img src="images/cmti/site-visit-group.webp" alt="CMTI students in hard hats on a construction site visit" width="1600" height="1200" fetchpriority="high"></div>
  <div class="hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">Construction education and skilling · Pan India</p>
      <h1 id="hero-title">Build the skills construction demands.</h1>
      <p class="lede">Practical training for engineers, interior professionals, project teams and skilled workmen, led by industry practitioners.</p>
      <div class="hero-actions"><a class="btn btn-white" href="finishing-school.html">Explore programmes</a><a class="btn btn-ghost-white" href="#contact">Make an enquiry</a></div>
    </div>
  </div>
</section>
<div class="stat-strip">
  <div class="container">
    <dl>
      <div><dt>Established</dt><dd>2018</dd></div>
      <div><dt>engineering college partners</dt><dd data-count="100">100+</dd></div>
      <div><dt>engineers placed</dt><dd data-count="5000">5,000+</dd></div>
      <div><dt>companies across construction, real estate, interiors and BIM</dt><dd data-count="300">300+</dd></div>
    </dl>
  </div>
</div>
'''
home += section(f'''<div class="two-col">
  <div class="prose reveal">
    <p class="eyebrow">About CMTI · Established 2018</p>
    <h2 id="about-title">Preparing professionals for construction careers</h2>
    <p class="lead">CMTI is one of India’s leading construction edtech institutes, delivering industry-led skilling across India.</p>
    <p>Er. S. G. Ashok Kumar, PMP, founded the Construction Management Training Institute in 2018. With guidance from Er. V. Suresh, a senior industry leader in building and construction standards, CMTI has expanded its training and placement activities across India.</p>
    {arrow_link("About Us", "about.html")}
  </div>
  {NITI}
</div>
{ABOUT_CARDS}''', sid="about", label="about-title")
home += section(shead("Delivery formats", "Learn in the format that fits", hid="formats-title") + '''<div class="cols-rule reveal">
  <article>''' + icon("building") + '''<h3>Offline</h3><p>Classroom workshops, site visits and hands-on trade demonstrations.</p></article>
  <article>''' + icon("laptop") + '''<h3>Online</h3><p>Live sessions and self-paced learning through CMTI Civil Engg Connect.</p>''' + arrow_link("Explore CMTI e-learning", "e-learning.html") + '''</article>
  <article>''' + icon("layers") + '''<h3>Hybrid</h3><p>Online instruction combined with in-person workshops or site-based practice.</p></article>
</div>''', sid="formats", label="formats-title")
home += section('<div class="section-head reveal"><h2 id="clients-title">Trusted By Leading Organizations</h2></div>' + client_marquee(), "section alt", "clients", "clients-title")
home += team_section("section alt")
home += trainers_section()
home += section(f'''<div class="webinar-strip reveal">
  {icon("monitor")}
  <div class="ws-text">
    <p class="ws-label">CMTI Webinars</p>
    <h2 id="webinars-title">Free webinars led by industry practitioners</h2>
    <p class="ws-when">Saturdays at 7:00 PM IST · Certificate of participation</p>
  </div>
  <a class="btn btn-primary" href="e-learning.html#webinars">Explore CMTI webinars</a>
</div>''', "section webinar-section", "webinars", "webinars-title")
options = "".join(f'<optgroup label="{g}">' + "".join(f"<option>{o}</option>" for o in opts) + "</optgroup>" for g, opts in PROGRAMME_GROUPS)
home += section(f'''<div class="contact-wrap">
  <div class="contact-info reveal">
    <p class="eyebrow">Contact us</p>
    <h2 id="contact-title">Let’s discuss your training needs</h2>
    <p class="promise">We reply within one working day.</p>
    <h3>Office address</h3>
    <address>4th Floor, 177/1, 7th B Main Road<br>Above Menaka Cards, Near NMKRV Women’s College<br>Jayanagar 3rd Block, Bengaluru 560011, Karnataka</address>
    <h3>Call or email CMTI</h3>
    <p><a href="tel:+918884422480">8884422480</a> / <a href="tel:+918884422179">8884422179</a><br><a href="mailto:cmtioffice@cmti.co.in">cmtioffice@cmti.co.in</a></p>
    <p>{arrow_link("Student testimonials", "testimonials.html")}</p>
  </div>
  <form id="enquiry" class="form-panel reveal" novalidate>
    <h3>Training enquiry</h3>
    <p class="help">Complete the form to open a draft in WhatsApp. Review and send it there.</p>
    <div class="fields">
      <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required maxlength="100" aria-describedby="e-name"><p class="field-error" id="e-name"></p></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="150" aria-describedby="e-email"><p class="field-error" id="e-email"></p></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="35" aria-describedby="e-phone"><p class="field-error" id="e-phone"></p></div>
      <div class="field"><label for="f-org">Organisation (optional)</label><input id="f-org" name="organisation" autocomplete="organization" maxlength="120"><p class="field-error"></p></div>
      <div class="field"><label for="programme">Programme</label><select id="programme" name="programme" required aria-describedby="e-programme"><option value="">Select a programme</option>{options}</select><p class="field-error" id="e-programme"></p></div>
      <div class="field"><label for="f-format">Preferred format</label><select id="f-format" name="format"><option>Flexible</option><option>Offline</option><option>Online</option><option>Hybrid</option></select><p class="field-error"></p></div>
      <div class="field field-wide"><label for="f-message">Training requirements (optional)</label><textarea id="f-message" name="message" maxlength="1000"></textarea><p class="field-error"></p></div>
    </div>
    <button class="btn btn-wa" type="submit">{WA_ICON}Open WhatsApp draft</button>
    <p class="form-status" id="form-status" role="status"></p>
  </form>
</div>''', "section alt", "contact", "contact-title")
write("index.html", "CMTI | Construction Management Training Institute",
      "Explore CMTI construction, interiors, corporate and trade skills programmes in offline, online and hybrid formats.", home)

# ================================================================ ABOUT
about = page_hero("About Us", "About CMTI · Established 2018", "Preparing professionals for construction careers",
    "CMTI is one of India’s leading construction edtech institutes, delivering industry-led skilling across India.",
    "images/cmti/street-group.webp", "How CMTI connects learning to project work",
    ["Technical foundations", "Practitioner-led training", "Project applications"])
about += section(f'''<div class="two-col">
  <div class="prose reveal">
    <p class="eyebrow">About CMTI</p>
    <h2 id="story-title">Construction skills for a developed India</h2>
    <p class="lead">Er. S. G. Ashok Kumar, PMP, founded the Construction Management Training Institute in 2018. With guidance from Er. V. Suresh, a senior industry leader in building and construction standards, CMTI has expanded its training and placement activities across India.</p>
  </div>
  {NITI.replace("<h3>Construction skills for a developed India</h3>", "")}
</div>
{ABOUT_CARDS}''', label="story-title")
import os as _os
MENTOR_PHOTO = "images/team/v-suresh.webp"
mentor_visual = (f'<img class="mentor-photo" src="{MENTOR_PHOTO}" alt="Er. V. Suresh" width="400" height="400">'
                 if _os.path.exists(f"{ROOT}/{MENTOR_PHOTO}") else '<span class="monogram" aria-hidden="true">VS</span>')
about += section(f'''<div class="mentor reveal">
  {mentor_visual}
  <div>
    <p class="eyebrow">CMTI Mentor</p>
    <h2 id="mentor-title">Er. V. Suresh</h2>
    <p class="role">Former Chairman &amp; Managing Director, HUDCO</p>
    <p>Er. V. Suresh is a senior civil engineer whose work spans housing, infrastructure and urban development. He has contributed to national building standards and the National Building Code, bringing decades of experience in the built environment.</p>
    <p>As CMTI’s mentor, he encourages construction education, practical skilling and knowledge sharing. His guidance inspires CMTI’s efforts to prepare industry-ready professionals and promote green building awareness.</p>
    <a class="link-arrow" href="https://www.linkedin.com/in/suresh-vasudevan-349253157/">Connect with Er. V. Suresh on LinkedIn</a>
  </div>
</div>''', "section dark on-dark", "mentor", "mentor-title")
about += team_section()
about += trainers_section("section alt", "trainers").replace('style="color:#fff"', "")
about += section('<div class="section-head reveal"><p class="eyebrow">Our Clients</p><h2 id="about-clients">Trusted By Leading Organizations</h2></div>' + client_marquee(), "section", "clients", "about-clients")
about += cta()
write("about.html", "About CMTI | CMTI", "About the Construction Management Training Institute: our story, mentor, leadership team, trainer network and clients.", about)

# ================================================================ VISION & MISSION
vm = page_hero("Mission &amp; Vision", "What guides CMTI", "Vision &amp; Mission", img="images/cmti/site-visit-group.webp")
vm += section(f'''<div class="vm-block reveal">
  <div class="vm-img"><img src="images/cmti/rebar-inspection.webp" alt="A CMTI trainer explaining slab reinforcement to students on site" loading="lazy" width="1600" height="1200"></div>
  <div class="vm-text">{icon("eye")}<h2 id="vision-title">Vision</h2><p>Our objective is to help construction based professionals be prepared and ready once they enter the industry by providing an extensive module of necessary training that gives them the fundamental skills and paramount level of preparedness to perform tasks and tackle any challenge that lies ahead of them once they enter the building and construction industry.</p></div>
</div>
<div class="vm-block flip reveal">
  <div class="vm-img"><img src="images/cmti/street-group.webp" alt="CMTI students and trainer on a site visit" loading="lazy" width="1500" height="1125"></div>
  <div class="vm-text">{icon("target")}<h2>Mission</h2><p>Our services are designed to help individuals improve their chances of building their careers in the construction industry in two different ways. Firstly by providing the required training to be eligible for employment. Secondly by offering placements and opportunities to professionals through our list of excellent, renowned clients and contacts in the construction industry.</p></div>
</div>''', label="vision-title")
vm += cta()
write("vision-mission.html", "Vision &amp; Mission | CMTI", "CMTI’s vision and mission for preparing construction professionals.", vm)

# ================================================================ ASSOCIATIONS
def assoc(logo, abbr, name, text):
    return f'<article class="card reveal"><img class="logo" src="association-logos/{logo}" alt="{abbr} logo" loading="lazy"><p class="label">{abbr}</p><h3>{name}</h3><p>{text}</p></article>'
asc = page_hero("Professional Associations", "Professional network", "Professional associations",
    "CMTI experts regularly participate in conferences, exhibitions and webinars to keep up with emerging industry requirements.",
    "images/cmti/rebar-inspection.webp", "Areas of professional exchange", ["Civil engineering", "Concrete practice", "Plumbing systems", "Green buildings"])
asc += section('<div class="grid" style="--cols:4">' +
    assoc("acce.jpeg", "ACCE", "Association of Consulting Civil Engineers", "A forum for civil engineers to exchange practical knowledge on design, construction and professional practice.") +
    assoc("ici.jpeg", "ICI", "Indian Concrete Institute", "Promotes knowledge of concrete technology, from materials and mix design to site execution, testing and durability.") +
    assoc("ipa.png", "IPA", "Indian Plumbing Association", "Promotes good practice in plumbing, water supply and sanitation, including efficient use of water in buildings.") +
    assoc("igbc.jpeg", "IGBC", "Indian Green Building Council", "Promotes green building practices, including energy efficiency, water conservation and responsible material use.") +
    "</div>", sid="associations")
asc += cta()
write("associations.html", "Associations | CMTI", "CMTI’s professional associations: ACCE, Indian Concrete Institute, Indian Plumbing Association and Indian Green Building Council.", asc)

# ================================================================ TESTIMONIALS
tst = page_hero("Testimonials", "CMTI Finishing School · Student testimonials", "From training to your first job",
    "Hear students share what they learnt, how they prepared for placements, and what it felt like to take their first step into the industry.",
    "images/cmti/site-visit-group.webp",
    extra=f'<a class="rating-box" href="{GOOGLE}" target="_blank" rel="noopener" style="margin-top:28px"><span class="score">4.7</span><span><span class="stars" style="--rating:4.7" role="img" aria-label="Rated 4.7 out of 5"></span><strong>2,362</strong> Google reviews</span></a>')
tst += section(shead("", "Hear from CMTI students", hid="students-title") + '<div class="grid" style="--cols:2">' +
    video("gd1zW_J2vXc", "Keerthana", "CMTI Finishing School", "https://www.youtube.com/watch?v=gd1zW_J2vXc") +
    video("vd9OFFVTzVo", "Amrita Bhat", "CMTI Finishing School", "https://www.youtube.com/watch?v=vd9OFFVTzVo") +
    f'</div><p style="margin-top:28px">{arrow_link("Explore CMTI testimonials on YouTube", "https://www.youtube.com/@CMTICivil/playlists")}</p>',
    label="students-title")
tst += cta()
write("testimonials.html", "Testimonials and Reviews | CMTI", "Student testimonials from the CMTI Finishing School and CMTI’s Google reviews.", tst)

# ================================================================ E-LEARNING
el = page_hero("E-Learning", "CMTI Civil Engg Connect", "Learn construction skills at your pace",
    "Explore 80+ affordable, self-paced courses delivered by construction industry experts. Designed for civil engineering students, fresh graduates and working professionals.",
    "images/cmti/street-group.webp",
    actions='<a class="btn btn-white" href="https://play.google.com/store/apps/details?id=com.learn.cmti">Download the Android app</a><a class="btn btn-ghost-white" href="https://elearn.cmti.co.in/">Open the e-learning platform</a>')
el += section(f'''<div class="two-col center">
  <div class="reveal">
    <p class="eyebrow">Learn, practise and earn a certificate</p>
    <h2 id="app-title">Self-paced lessons · Mock tests · Course e-certificate</h2>
    <div class="grid" style="--cols:1;margin-top:32px">
      {card("Learn anytime", "Fit lessons around work or study and revisit them when you need a refresher.", "clock")}
      {card("Practise with mock tests", "Check your understanding and identify topics to review.", "check")}
      {card("Earn an e-certificate", "Complete the course requirements to earn your certificate.", "award")}
    </div>
  </div>
  <figure class="reveal" style="margin:0">
    <div class="app-frame"><img src="images/app-preview.png" alt="CMTI Civil Engg Connect app preview from Google Play" loading="lazy"></div>
    <figcaption class="app-cap" style="color:var(--muted)">App preview from Google Play</figcaption>
  </figure>
</div>''', label="app-title")
el += section(f'''<div class="two-col center">
  <div class="reveal">
    <p class="eyebrow">CMTI Webinars</p>
    <h2 id="webinars-title">Free webinars led by industry practitioners</h2>
    <p>CMTI regularly hosts free webinars and provides a certificate of participation. Follow our WhatsApp channel and LinkedIn page for upcoming topics, dates and registration details.</p>
    <p class="tags-label">What to expect from a CMTI webinar</p>
    <ul class="tags"><li>Free expert-led session</li><li>Topic updates via WhatsApp and LinkedIn</li><li>Certificate of participation</li></ul>
    <div class="cta-actions"><a class="btn btn-white" href="https://whatsapp.com/channel/0029Va4S47dEgGfOPitXTT2f">Follow CMTI on WhatsApp</a><a class="btn btn-ghost-white" href="https://www.linkedin.com/company/cmtionline/">Follow CMTI on LinkedIn</a></div>
    <p style="margin-top:20px"><a class="link-arrow" style="color:#fff" href="https://linktr.ee/cmti">Find CMTI on YouTube, Instagram and Telegram</a></p>
  </div>
  <div class="card reveal" style="background:var(--navy-2)">{icon("monitor")}<p class="label">Every week</p><h3 style="font-size:2rem">Saturdays at 7:00 PM IST</h3><p>Construction, Quality, Digital Construction, Interiors and trending industry topics.</p></div>
</div>''', "section dark on-dark", "webinars", "webinars-title")
el += cta()
write("e-learning.html", "CMTI E-Learning | CMTI", "CMTI Civil Engg Connect: 80+ affordable, self-paced construction courses, plus free CMTI webinars.", el)

# ================================================================ FINISHING SCHOOL (CACM)
P = "Advanced Construction Management Course (CACM)"
fs = page_hero("Advanced Construction Management Course (CACM)", "CMTI Finishing School", "Certificate Course on Advanced Construction Management",
    img="images/cmti/rebar-inspection.webp", tags_label="Skills practised in the CACM course",
    tags=["Drawings, BOQ and BBS", "Construction sequencing", "Site quality and safety"],
    meta="3 months · Offline, online and hybrid · Hands-on exercises and construction site visits",
    actions=f'<a class="btn btn-white" href="{enquire(P)}">Enquire about the course</a>')
fs += section(f'''<div class="two-col">
  <div class="reveal">
    <h2 id="apply-title" style="margin-bottom:28px">Who should apply?</h2>
    <div class="grid" style="--cols:1">
      {card("Eligibility", "Diploma holders, graduates and postgraduates, including freshers and young professionals with one to two years of experience.", "users")}
      {card("Target audience", "Aspiring construction professionals who want practical skills in site execution, quantity estimation, quality and safety. The course also supports those preparing for job interviews or exploring construction entrepreneurship.", "target")}
    </div>
  </div>
  {video("jxEoc8QkPOo", "Certificate Course on Advanced Construction Management", "CMTI Finishing School", "https://youtu.be/jxEoc8QkPOo?si=nEbcd9MJnwgl8fzC")}
</div>''', "section alt", label="apply-title")
fs += section('''<div class="panel reveal">
  <h2 id="objective-title">Programme objective</h2>
  <p style="margin:0">Prepare participants for day-to-day site responsibilities by building their ability to interpret drawings and specifications, understand construction materials, perform calculations, estimate quantities and costs, and sequence construction activities.</p>
</div>''', label="objective-title")
fs += section(shead("", "Learning outcomes", hid="outcomes-title") + '<ul class="tick-list reveal">' + "".join(f"<li>{x}</li>" for x in [
    "Interpret drawings and specifications, convert units, and take site measurements.",
    "Identify cement, aggregates, reinforcement steel and masonry units, and explain their properties, uses and basic quality checks.",
    "Calculate area, volume, material quantities and reinforcement weight.",
    "Prepare Bills of Quantities (BOQs), Bar Bending Schedules (BBS) and rate analyses.",
    "Sequence construction activities and explain where formwork, construction methods and site execution procedures fit.",
    "Identify quality checks and safety practices and relate them to activities observed during site visits.",
    "Use AutoCAD, SketchUp and BIM tools in construction workflows.",
    "Prepare for job interviews and identify the first steps towards starting a construction business."]) + "</ul>",
    label="outcomes-title")
fs += section(shead("CMTI / IDMTI Finishing School", "More Finishing School programmes", hid="more-title") + '<div class="grid" style="--cols:4">' +
    card("Interior Design &amp; Management Course (IDM)", "Certificate Course on Interior Design &amp; Management", None, extra='<img class="card-brand" src="idmti-logo.webp" alt="IDMTI, Interior Design &amp; Management Training Institute" width="600" height="321" loading="lazy">' + arrow_link("Explore the three-month interior design course", "idmti.html")) +
    card("Internships", "Explore practical exposure to construction projects and enquire about current internship opportunities.", "briefcase", cid="internship", extra=arrow_link("Enquire", enquire("Internships"))) +
    card("Construction Software Courses", "Build software skills for construction drawings, quantity estimation and project planning.", "laptop", cid="construction-software", extra=arrow_link("Enquire", enquire("Construction Software Courses"))) +
    card("BIM Design Software", "Explore model-based design and coordination for construction and interiors.", "cpu", cid="bim-design", extra=arrow_link("Enquire", enquire("BIM Design Software"))) +
    "</div>", "section alt", label="more-title")
fs += cta()
write("finishing-school.html", "Advanced Construction Management Course (CACM) | CMTI", "Certificate Course on Advanced Construction Management: 3 months, offline, online and hybrid, with hands-on exercises and construction site visits.", fs)

# ================================================================ IDMTI
PI = "Interior Design &amp; Management Course (IDM)"
idm = page_hero("Interior Design &amp; Management Course (IDM)", "Interior Design &amp; Management Training Institute", "Certificate Course on Interior Design &amp; Management",
    "Founded by Er. S. G. Ashok Kumar, IDMTI prepares aspiring professionals for residential and commercial interiors. Alumni have worked with firms including HomeLane, DesignCafe, Bonito Designs and Purva Streaks.",
    "images/cmti/showroom-visit.webp", "How an interior fit-out comes together", ["Design and layouts", "Modular production", "Site installation"],
    meta="3 months · Offline, online and hybrid", actions=f'<a class="btn btn-white" href="{enquire(PI)}">Enquire about the course</a>',
    badge='<img class="hero-badge" src="idmti-logo-dark.webp" alt="IDMTI, Interior Design &amp; Management Training Institute" width="600" height="321">')
idm += '''<div class="stat-strip"><div class="container"><dl style="grid-template-columns:repeat(3,minmax(0,1fr))">
  <div><dt>Certificate course duration</dt><dd>3 months</dd></div>
  <div><dt>interior firms hiring IDMTI alumni over the past 8 years</dt><dd data-count="200">200+</dd></div>
  <div><dt>Offline, online and hybrid</dt><dd>3 modes</dd></div>
</dl></div></div>'''
idm += section(f'''<div class="two-col">
  <div class="reveal">
    <h2 id="idm-apply" style="margin-bottom:28px">Who should apply?</h2>
    <div class="grid" style="--cols:1">
      {card("Eligibility", "Diploma holders, graduates and postgraduates, including freshers and young professionals with one to two years of experience.", "users")}
      {card("Target audience", "Aspiring interior design professionals and early-career professionals interested in large-scale interior projects.", "target")}
      {card("Programme objective", "Learn to gather client requirements, prepare drawings and estimates, select materials and hardware, and understand how designs move from factory production to site installation.", "ruler")}
    </div>
  </div>
  {video("5kdH5vo8Wio", "Certificate Course on Interior Design &amp; Management", "IDMTI", "https://youtu.be/5kdH5vo8Wio?si=3yrPcKyu891crYqX")}
</div>''', label="idm-apply")
SYL = [("doc", "Interior design standards, drawings and specifications"), ("layers", "Materials and hardware selection for interior and modular works"),
    ("laptop", "AutoCAD, SketchUp and an introduction to BIM"), ("chart", "Quantity estimation, basic costing and modular cut lists"),
    ("chat", "Client requirements, design presentations and feedback"), ("building", "Factory production, showroom design and material selection, and site installation")]
idm += section(shead("", "Syllabus", "Hands-on exercises, software training and field visits to modular factories, showrooms and interior project sites.", hid="syl-title") +
    '<div class="info-grid reveal" style="--cols:3">' + "".join(f'<div class="info-tile"><span class="n">{i:02d}</span>{icon(ic)}<div><h3>{t}</h3></div></div>' for i, (ic, t) in enumerate(SYL, 1)) + "</div>",
    "section alt", label="syl-title")
idm += section(shead("", "Learning outcomes", hid="idm-out") + '<ul class="tick-list reveal">' + "".join(f"<li>{x}</li>" for x in [
    "Prepare basic AutoCAD layouts and SketchUp 3D models.", "Interpret specifications and select materials and hardware.",
    "Calculate quantities and prepare estimates and cut lists.", "Explain how drawings guide manufacturing and installation.",
    "Document client requirements, present options and respond to feedback."]) + "</ul>", label="idm-out")
idm += cta()
write("idmti.html", "Interior Design &amp; Management Course (IDM) | CMTI", "Certificate Course on Interior Design & Management from IDMTI: 3 months, offline, online and hybrid.", idm)

# ================================================================ COLLEGES
col = page_hero("College MoUs", "College partnerships", "What a CMTI MoU offers your college", img="images/cmti/site-visit-group.webp",
    tags_label="Campus-to-career support", tags=["Software and workshops", "Internship exposure", "Interview preparation"],
    actions=f'<a class="btn btn-white" href="{enquire("College MoU")}">Discuss a College MoU</a>')
col += '''<div class="stat-strip"><div class="container"><dl style="grid-template-columns:repeat(3,minmax(0,1fr))">
  <div><dt>engineering college partners</dt><dd data-count="100">100+</dd></div>
  <div><dt>engineers placed</dt><dd data-count="5000">5,000+</dd></div>
  <div><dt>companies across construction, real estate, interiors and BIM</dt><dd data-count="300">300+</dd></div>
</dl></div></div>'''
col += section(shead("College partnerships", "Benefits for Colleges Signing an MoU with CMTI", hid="mou-title") + mou_tiles(), label="mou-title")
col += section('<div class="section-head reveal"><p class="eyebrow">College network</p><h2 id="net-title">Selected institutions</h2></div>' + college_marquee() +
    f'<p style="margin-top:32px"><a class="btn btn-primary" href="{enquire("College MoU")}">Discuss a College MoU</a></p>', "section alt", label="net-title")
col += cta()
write("colleges.html", "College MoUs | CMTI", "What a CMTI MoU offers engineering colleges: placements, internships, software training, curriculum development and more.", col)

# ================================================================ CORPORATE
def stage(title, text, big, small, tone):
    """Solid colour block: a large experience figure on the left, title and text on the right."""
    return (f'<article class="stage-block tone-{tone}"><p class="sb-figure">{big}<small>{small}</small></p>'
            f'<div><h4>{title}</h4><p>{text}</p></div></article>')

PC = "Capability Development Programme for Staff"
corp = page_hero("For Corporates", "For Corporates", "Technical capability development",
    "Customised construction training for your teams, project needs and industry standards.", "images/cmti/showroom-visit.webp",
    actions=f'<a class="btn btn-white" href="{enquire(PC)}">Discuss your training needs</a>')
REASONS = [("target", "Customised programmes", "We work with Learning &amp; Development and Operations teams to align training with participant roles, project needs and industry standards."),
    ("helmet", "Experienced industry practitioners", "Our network of 50+ trainers brings hands-on construction and real estate experience. Most are former Larsen &amp; Toubro professionals."),
    ("pin", "Pan-India delivery", "We deliver training at project sites and corporate offices across India, with online and hybrid options."),
    ("tag", "Affordable pricing", "We align the scope, duration and delivery format with your training priorities and budget."),
    ("chart", "Proven track record and strong NPS", "We deliver programmes for real estate, EPC and government organisations, track participant feedback using Net Promoter Score, and assess learning against agreed objectives.")]
reason_items = "".join(
    f'<li class="reason{" is-open" if i == 1 else ""}"><button type="button" class="reason-head" aria-expanded="{"true" if i == 1 else "false"}" aria-controls="reason-{i}">'
    f'<span class="reason-num">{i:02d}</span>{icon(ic)}<span class="reason-title">{t}</span><span class="reason-x" aria-hidden="true"></span></button>'
    f'<div class="reason-body" id="reason-{i}"{"" if i == 1 else " hidden"}><p>{d}</p></div></li>'
    for i, (ic, t, d) in enumerate(REASONS, 1))
corp += section(f'''<div class="reasons-panel reveal">
  <div class="reasons-lead">
    <h2 id="why-title">Top 5 reasons corporates choose CMTI as their technical capability development partner</h2>
    <p>Customised construction training for your teams, project needs and industry standards.</p>
    <a class="btn btn-primary" href="{enquire(PC)}">Make an enquiry</a>
  </div>
  <ol class="reasons-list" data-reasons>{reason_items}</ol>
</div>''', label="why-title")
corp += section(shead("", "How we customise each programme", hid="steps-title") + '<ol class="steps reveal" aria-label="Programme customisation steps">' + "".join(f"<li>{s}</li>" for s in [
    "Discuss needs with L&amp;D and Operations", "Identify skill gaps and map competencies", "Refine and agree the session plan",
    "Develop tailored training content", "Deliver and assess learning"]) + "</ol>", "section dark on-dark", label="steps-title")
corp += section(f'''<div class="two-col">
  <div class="prose reveal">
    <p class="eyebrow">Corporate training</p>
    <h2 id="staff-title">Capability Development Programme for Staff</h2>
    <p class="lead">When skilled hires are hard to find, upskilling helps existing staff take on more responsibility in their current roles, while reskilling prepares them for new roles. CMTI works with L&amp;D and Operations to identify skill gaps and design training around the work participants will do.</p>
    <div class="photo" style="margin-top:32px"><img src="images/cmti/site-visit-group.webp" alt="CMTI students in hard hats on a construction site visit" loading="lazy" width="1600" height="1200"></div>
  </div>
  <div class="reveal">
    <h3 style="margin-bottom:20px">Training by career stage</h3>
    <div class="stage-blocks">
      {stage("Freshers", "Diploma Engineer Trainee (DET) and Graduate Engineer Trainee (GET) programmes. We tailor the duration and topics to business needs. CMTI has delivered GET programmes for nine years, with programme details available on request.", "DET / GET", "programmes", 1)}
      {stage("Middle management", "We recommend a two-day workshop on construction topics selected with your team.", "3–15", "years of experience", 2)}
      {stage("Construction and project managers", "Workshops tailored to senior project responsibilities and organisational priorities.", "15+", "years of experience", 3)}
    </div>
  </div>
</div>''', "section alt", "training-participants", "staff-title")
TOPICS = [("building", "Construction Management", "Core and shell, formwork, finishes and handover protocols."),
    ("chart", "Project Management", "Project planning, project controls and software tools."),
    ("check", "Quality Management", "Quality planning, inspections and corrective actions."),
    ("shield", "Safety Management", "Site hazard identification, risk controls and safe work practices."),
    ("bolt", "MEPF", "Mechanical, electrical, plumbing and firefighting systems."),
    ("cpu", "AI in Construction", "Applying artificial intelligence across construction functions."),
    ("home", "Real Estate", "Real estate fundamentals for professionals outside the sector."),
    ("rupee", "Finance", "Finance fundamentals for non-finance professionals."),
    ("handshake", "Customer Relationship Management", "Customer communication, issue resolution and handover coordination."),
    ("scale", "RERA and National Building Code", "An overview of real estate regulation and building code requirements."),
    ("leaf", "Green Buildings, Sustainability and ESG", "Resource efficiency, sustainable construction and ESG practices."),
    ("award", "Quality Management Systems (QMS)", "ISO 9001:2026 requirements, audit planning, auditing principles, audit reporting and the third-party certification process.")]
# Topic flip cards: hover (or tap / Enter) flips a card to show what the topic covers.
flips = "".join(
    f'<article class="flip-card" data-flip>'
    f'<div class="flip-inner">'
    f'<button class="flip-face flip-front" type="button" aria-expanded="false">{icon(ic)}<h3>{t}</h3>'
    f'<span class="flip-hint" aria-hidden="true">Flip for details</span><span class="sr-only">: show what this topic covers</span></button>'
    f'<div class="flip-face flip-back"><p class="flip-num">Topic {i:02d}</p><h3>{t}</h3><p>{d}</p>'
    f'<div class="flip-actions"><a class="link-arrow" href="{enquire(PC)}">Enquire with CMTI</a>'
    f'<button class="flip-return" type="button">Back</button></div></div>'
    f'</div></article>'
    for i, (ic, t, d) in enumerate(TOPICS, 1))
corp += section(shead("", "Explore training topics", "Select a topic to see what it covers.", hid="topics-title") +
    f'<div class="flip-grid reveal">{flips}</div>', sid="training-topics", label="topics-title")
corp += section(f'''<div class="two-col center">
  <div class="photo reveal"><img src="images/cmti/rebar-inspection.webp" alt="A CMTI trainer explaining slab reinforcement to students on site" loading="lazy" width="1600" height="1200"></div>
  <div class="reveal">
    <h2 id="workmen-title">Capability Development Programme for Workmen</h2>
    <ul class="tags light" style="padding:0">{"".join(f'<li style="border:1px solid var(--line);color:var(--ink)">{t}</li>' for t in ["Formwork &amp; scaffolding", "Masonry", "Bar bending", "Plumbing", "Waterproofing", "Finishing works"])}</ul>
    <p class="lead">Experienced trade trainers customise practical programmes around project requirements and the work crews perform on site.</p>
    <p>Formwork and scaffolding certification is available as part of the trade training offering.</p>
    <a class="btn btn-primary" href="{enquire("Capability Development Programme for Workmen")}">Enquire with CMTI</a>
  </div>
</div>''', "section alt", "workmen", "workmen-title")
def service(sid, ic, title, steps, text):
    prog = title
    return (f'<article class="service reveal" id="{sid}"><div class="service-head">{icon(ic)}<h3>{title}</h3></div>'
            f'<div class="service-body"><p class="service-label">How it works</p><ol class="service-steps">' + "".join(f"<li>{s}</li>" for s in steps) +
            f'</ol><p class="service-text">{text}</p><a class="btn btn-primary service-cta" href="{enquire(prog)}">Enquire with CMTI</a></div></article>')
corp += section('<div class="service-grid">' +
    service("content-development", "doc", "Content Development", ["Understand project workflows", "Develop SOPs and learning materials", "Review with your team"],
            "CMTI develops standard operating procedures and training content for in-house learning systems. We tailor materials to project workflows, roles and site requirements.") +
    service("assessment", "search", "Assessment of Employees", ["Identify role competencies", "Assess skills and knowledge", "Report gaps and training priorities"],
            "CMTI helps L&amp;D teams assess employees periodically using suitable internationally used assessment tools. We report competency gaps and priorities for follow-up training. CMTI has delivered assessments for multiple clients.") +
    service("hiring", "handshake", "Hiring Support", ["Share your hiring needs", "Connect with campuses", "Interview potential hires"],
            "CMTI has trained 5,000+ engineers through its Finishing School and works with 100+ engineering colleges. We can help employers coordinate campus hiring for entry-level engineering roles.") +
    "</div>")
corp += section('<div class="section-head reveal"><h2 id="corp-clients">Trusted By Leading Organizations</h2></div>' + client_marquee(), "section alt", "client-logos", "corp-clients")
corp += cta()
write("corporate.html", "For Corporates | CMTI", "Customised construction training for staff and workmen, content development, employee assessment and hiring support across India.", corp)

# ================================================================ PRIVACY POLICY (text from cmti.co.in)
def legal_page(blocks):
    """blocks: list of (heading, [paragraph or list-of-bullets, ...])."""
    out = []
    for heading, parts in blocks:
        out.append(f"<h2>{heading}</h2>")
        for part in parts:
            if isinstance(part, list):
                out.append("<ul>" + "".join(f"<li>{x}</li>" for x in part) + "</ul>")
            else:
                out.append(f"<p>{part}</p>")
    return '<article class="legal-text reveal">' + "".join(out) + "</article>"

privacy = page_hero("Privacy Policy", "CMTi", "CMTi Privacy Policy", img="images/cmti/street-group.webp")
privacy += section(legal_page([
    ("Information that is gathered from visitors", [[
        "In common with other websites, log files are stored on the web server saving details such as the visitor's IP address, browser type, referring page and time of visit.",
        "Cookies may be used to remember visitor preferences when interacting with the website.",
        "Where registration is required, the visitor's email and a username will be stored on the server."]]),
    ("How the Information is used?", [[
        "The information is used to enhance the vistor's experience when using the website to display personalised content and possibly advertising.",
        "E-mail addresses &amp; Mobile numbers will not be sold, rented or leased to 3rd parties.",
        "E-mails and SMSes may be sent to inform you of news of our services or offers by us or our affiliates."]]),
    ("Visitor Options", [[
        "If you have subscribed to one of our services, you may unsubscribe by following the instructions which are included in e-mail that you receive.",
        "You may be able to block cookies via your browser settings but this may prevent you from access to certain features of the website."]]),
    ("Cookies", [
        "Cookies are small digital signature files that are stored by your web browser that allow your preferences to be recorded when visiting the website. Also they may be used to track your return visits to the website. 3rd party advertising companies may also use cookies for tracking purposes."]),
    ("Google Ads", [[
        "Google, as a third party vendor, uses cookies to serve ads.",
        "Google's use of the DART cookie enables it to serve ads to visitors based on their visit to sites they visit on the Internet.",
        "Website visitors may opt out of the use of the DART cookie by visiting the Google ad and content network privacy policy."]]),
]), label=None)
privacy += cta()
write("privacy-policy.html", "Privacy Policy | CMTi", "CMTi privacy policy: information gathered from visitors, how it is used, visitor options, cookies and Google Ads.", privacy)

# ================================================================ AWARDS & CERTIFICATES
def award(img, alt, w, h, kind, title, meta, text="", extra=None):
    def pic(src, a, iw, ih, label):
        return (f'<a class="award-img" href="{src}" target="_blank" rel="noopener" aria-label="Open full-size image: {label}">'
                f'<img src="{src}" alt="{a}" width="{iw}" height="{ih}" loading="lazy"><span class="award-zoom" aria-hidden="true">View full size</span></a>')
    pics = pic(img, alt, w, h, title)
    if extra:
        pics = f'<div class="award-pics">{pics}{pic(*extra, title + " (certificate)")}</div>'
    return (f'<article class="award reveal">{pics}'
            f'<div class="award-body"><p class="award-kind">{kind}</p><h2>{title}</h2><p class="award-meta">{meta}</p>{f"<p>{text}</p>" if text else ""}</div></article>')

aw = page_hero("Awards &amp; Certificates", "About CMTI", "Awards &amp; Certificates",
    "Recognition for CMTI's work in construction skilling and corporate training.", "images/awards/isda-infracon-2025-award.webp")
aw += section('<div class="award-list">' +
    award("images/awards/isda-infracon-2025-award.webp", "CMTI receiving the Best Skill Development Award on stage at the ISDA Infracon National Awards 2025", 1600, 1200,
          "Award", "Best Skill Development Award for CMTI",
          "ISDA Infracon 2025 National Level Awards at New Delhi") +
    award("images/awards/towell-manchester-appreciation.webp", "CMTI receiving the appreciation certificate from Towell Group in Manchester, UK", 800, 615,
          "Certificate", "Appreciation Certificate",
          "Issued by Towell Group Chairman",
          "For conducting a two-week programme for Omani officials at Manchester, UK.",
          extra=("images/awards/towell-programme-certificate.webp", "The certificate presented to CMTI by Towell Infrastructure Projects LLC", 1308, 887)) +
    '</div>', label=None)
aw += cta()
write("awards.html", "Awards &amp; Certificates | CMTI", "Awards and certificates received by CMTI, including the Best Skill Development Award at the ISDA Infracon 2025 National Level Awards, New Delhi.", aw)

