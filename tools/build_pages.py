"""Generate every CMTI page (index.html and the nine inner pages).

Run from the repository root:
    python3 tools/build_pages.py .

The wording comes from the original CMTI site; page structure follows the
"CMTI Website Inputs" brief. Edit text here, not in the generated .html files,
or the next run will overwrite your edits.
"""
import hashlib
import os
import re
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
    return "index.html?programme=" + quote(_html.unescape(programme)) + "#enquiry"

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
    ("Certified Courses", None, [("Advanced Construction Management Course (CACM)", "cacm.html"), ("Interior Design &amp; Management Course (IDM)", "idmti.html"),
                                ("Internships", "cacm.html#internship"),
                                ("Construction Software Courses", "cacm.html#construction-software"),
                                ("BIM Design Software", "cacm.html#bim-design")]),
    ("College MoUs", "colleges.html", None),
    ("E-Learning", None, [("Online Courses", "e-learning.html"), ("Webinars", "e-learning.html#webinars")]),
    ("Contact", "index.html#enquiry", None),
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
      <a class="btn btn-primary" href="index.html#enquiry">Make an enquiry</a>
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
    <div><h3>Certified Courses</h3><ul><li><a href="cacm.html">Advanced Construction Management Course (CACM)</a></li><li><a href="idmti.html">Interior Design &amp; Management Course (IDM)</a></li></ul></div>
    <div><h3>CMTI</h3><ul><li><a href="colleges.html">College MoUs</a></li><li><a href="testimonials.html">Google reviews</a></li><li><a href="index.html#enquiry">Contact us</a></li></ul></div>
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
  <a class="qc-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_ICON}<span class="qc-text"><span>WhatsApp</span><small>8884422480 / 8884422179</small></span></a>
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
    html = clean_links(html)
    open(f"{ROOT}/{name}", "w", encoding="utf-8").write(html)
    print("wrote", name)

def clean_links(html):
    """Link to /about rather than /about.html, and to ./ rather than index.html.
    GitHub Pages serves about.html for /about, so the address bar never shows .html."""
    def fix(m):
        page, rest = m.group(1), m.group(2) or ""
        return f'href="{"./" if page == "index" else page}{rest}"'
    return re.sub(r'href="([a-z0-9-]+)\.html([?#][^"]*)?"', fix, html)

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
    <div class="cta-actions"><a class="btn btn-white" href="index.html#enquiry">Make an enquiry</a><a class="btn btn-ghost-white" href="tel:+918884422179">Call 8884422179</a></div>
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from college_list import COLLEGE_STATES

def college_logo(slug):
    """File name of a college's logo in college-logos/, whatever its image type."""
    for ext in ("webp", "png", "svg", "jpg", "jpeg"):
        if os.path.exists(f"{ROOT}/college-logos/{slug}.{ext}"):
            return f"college-logos/{slug}.{ext}"
    raise SystemExit(f"college_list.py names the logo '{slug}', but college-logos/ has no such image")

def college_directory():
    """Every partner college, state by state: its logo where we have one, a cap mark where we don't."""
    cap = f'<span class="mark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{ICONS["cap"]}"/></svg></span>'
    def item(name, place, slug=None):
        mark = f'<img src="{college_logo(slug)}" alt="" width="44" height="44" loading="lazy">' if slug else cap
        return f'<li>{mark}<span><strong>{name}</strong>' + (f"<small>{place}</small>" if place else "") + "</span></li>"
    total = sum(len(rows) for _, rows in COLLEGE_STATES)
    out = ('<div class="section-head reveal"><p class="eyebrow">Partner colleges</p>'
           f'<h2 id="dir-title">{total} colleges across {len(COLLEGE_STATES)} states</h2>'
           "<p>Engineering colleges CMTI works with for training, internships and placements.</p></div>")
    out += ('<nav class="state-nav" aria-label="Jump to a state">' +
            "".join(f'<a href="#state-{s.lower().replace(" ", "-")}">{s} <span>{len(rows)}</span></a>' for s, rows in COLLEGE_STATES) + "</nav>")
    for state, rows in COLLEGE_STATES:
        sid = "state-" + state.lower().replace(" ", "-")
        out += (f'<h3 class="state-title" id="{sid}">{state} <span>{len(rows)} colleges</span></h3>'
                '<ul class="college-list">' + "".join(item(*r) for r in rows) + "</ul>")
    return out

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

def pillar(num, label, title, text, points, img, alt, cta, href, tone=""):
    pts = "".join(f"<li>{icon('check', 'tick')}<span>{pt}</span></li>" for pt in points)
    return f"""<article class="pillar {tone} reveal">
  <div class="pillar-img"><img src="{img}" alt="{alt}" loading="lazy" width="1600" height="1000"><span class="pillar-num">{num}</span></div>
  <div class="pillar-body">
    <p class="pillar-label">{label}</p>
    <h3>{title}</h3>
    <p class="pillar-text">{text}</p>
    <ul class="pillar-points">{pts}</ul>
    <a class="btn btn-primary" href="{href}">{cta}</a>
  </div>
</article>"""

ABOUT_CARDS = ('<div class="pillars">' +
    pillar("01", "For companies and institutions", "Corporate, Government and International Training",
        "CMTI is a technical training partner to real estate and engineering, procurement and construction (EPC) companies.",
        ["Capability development programmes delivered at project sites across India",
         "Training delivered for the Indian Space Research Organisation (ISRO)",
         "International programme for Towell Group in Manchester, UK"],
        "images/cmti/corporate-staff-training.webp", "A CMTI trainer leading a capability development session for corporate staff",
        "Explore corporate training", "corporate.html") +
    pillar("02", "For engineering colleges and students", "College Trainings and Placements",
        "On-campus and off-campus training, internship support and campus interviews for engineering students.",
        ["Partnerships with <strong>100+ engineering colleges</strong>",
         "<strong>5,000+ engineers</strong> placed in construction and interiors roles",
         "Hiring connections with <strong>300+ companies</strong> across construction, real estate, interiors and BIM"],
        "images/cmti/street-group.webp", "CMTI students in hard hats with their trainers on a street outside a site",
        "Explore college partnerships", "colleges.html", tone="alt") +
    "</div>")

PROGRAMME_GROUPS = [
    ("Certified Courses", ["Advanced Construction Management Course (CACM)", "Interior Design &amp; Management Course (IDM)", "Internships", "Construction Software Courses", "BIM Design Software"]),
    ("For Corporates", ["Capability Development Programme for Staff", "Capability Development Programme for Workmen", "Content Development", "Assessment of Employees", "Hiring Support", "Trainer Profiles"]),
    ("Other", ["College MoU", "E-Learning and Webinars", "Something else"]),
]

# ================================================================ HOME (redesign-2026, design-taste-frontend kit)
import json as _json_home
import chrome_v2 as v2

_COURSES = _json_home.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "elearn_courses.json"), encoding="utf-8"))["courses"]
_N_COURSES = len(_COURSES)
_N_FREE = sum(1 for c in _COURSES if not c["price"])
_N_COLLEGES = sum(len(cs) for _, cs in COLLEGE_STATES)
_FREE_PICKS = ["Non Destructive Testing Course", "Self Compacting Concrete Course", "Fire Safety in Highrise Construction",
               "Plant &amp; Machinery in Construction", "Drones in Construction"]

def _course_row(title):
    c = next(c for c in _COURSES if c["title"].replace("&", "&amp;") == title or c["title"] == title)
    return (f'<li><a class="lms__row" href="{c["url"]}"><span class="lms__title">{c["title"].replace("&", "&amp;")}</span>'
            f'<span class="lms__meta">{c["category"].replace("&", "&amp;")} · {c["lessons"]} lessons</span>'
            f'<span class="lms__chip">Free</span></a></li>')

_HOME_CLIENTS = [(1, "png", "DLF"), (4, "png", "ISRO"), (6, "png", "Larsen &amp; Toubro"), (2, "png", "Godrej Properties"),
                 (11, "png", "Tata Projects"), (8, "png", "Prestige Group"), (24, "png", "Shapoorji Pallonji"), (3, "png", "Hines")]

def _logo_size(n, e):
    from PIL import Image as _Img
    return _Img.open(os.path.join(ROOT, f"client-logos/h80/{n}.{e}")).size

_PLAY = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4.5 2.6v12.8c0 .8.9 1.3 1.6.9l10.3-6.4c.6-.4.6-1.3 0-1.7L6.1 1.7c-.7-.4-1.6.1-1.6.9Z" fill="currentColor"/></svg>'

def _video_card(vid, name, line):
    return f'''<article class="card card--open span-6">
  <h3>{name}</h3>
  <p>{line}</p>
  <div class="panel panel--video"><button class="yt" type="button" data-yt="{vid}" data-title="{name}: {line}">
    <img class="frame__img" src="images/youtube/{vid}.webp" alt="" width="480" height="360" loading="lazy">
    <span class="ly-play__disc">{_PLAY}</span><span class="sr-only">Play the video: {name}, {line}</span>
  </button></div>
</article>'''

_opts = "".join(f'<optgroup label="{g}">' + "".join(f"<option>{o}</option>" for o in opts) + "</optgroup>" for g, opts in PROGRAMME_GROUPS)

home = f'''<section class="hero hero--film" data-enter aria-labelledby="hero-h">
  <div class="wrap"><div class="hero-text hero__in">
    <div class="hero__media hero__fill" data-film-host>
      <img src="images/cmti/rebar-inspection.webp" srcset="images/cmti/rebar-inspection-phone.webp 567w, images/cmti/rebar-inspection.webp 1600w" sizes="(max-width: 639px) 342px, 1280px" alt="CMTI course participants in hard hats inspecting reinforcement steel on a construction site" width="1600" height="1200" style="--ly-pos: 50% 45%; --ly-pos-phone: 50% 50%" fetchpriority="high">
      <div class="hero__over">
        <div>
          <p class="hero__kicker"><a href="awards.html">Best Skill Development Award, ISDA Infracon 2025</a></p>
          <h1 id="hero-h">Construction training for site teams</h1>
          <p class="hero__lead">Programmes for EPC and real estate staff and workmen at their sites, and three-month certified courses for engineers. 5,000+ engineers placed since 2018.</p>
          <div class="btn-row"><a class="btn btn--primary" href="corporate.html">See team training</a><a class="btn btn--secondary" href="#programmes">Find a course</a></div>
          <p class="hero__rating"><a href="testimonials.html">Rated 4.7 on Google from 2,362 reviews</a></p>
        </div>
        <a class="ly-play" href="https://www.youtube.com/watch?v=jxEoc8QkPOo" data-yt-film="jxEoc8QkPOo" data-title="Certificate Course on Advanced Construction Management">
          <span class="ly-play__disc">{_PLAY}</span>
          <span class="ly-play__label">Watch the CACM film<small>Certificate course overview</small></span>
        </a>
      </div>
    </div>
  </div></div>
</section>

<section class="section g2m" id="training" aria-labelledby="training-h">
  <div class="wrap grid">
    <div class="span-5">
      <div class="section-head">
        <h2 id="training-h">Training for companies, colleges and engineers</h2>
        <p>Each programme is planned with the client and delivered offline, online or hybrid.</p>
      </div>
      <ul class="rows">
        <li><span class="rows__name">Companies and government</span><span class="rows__value">ISRO, DLF, L&amp;T</span><p>Staff and workmen programmes at your sites, planned with your L&amp;D team.</p></li>
        <li><span class="rows__name">Engineering colleges</span><span class="rows__value">{_N_COLLEGES} colleges</span><p>MoUs for placements, internships and software training.</p></li>
        <li><span class="rows__name">Graduates and professionals</span><span class="rows__value">{_N_COURSES} courses online</span><p>Three-month certified courses and self-paced courses online.</p></li>
      </ul>
      <p class="rows-link"><a class="link" href="corporate.html#training-participants">See staff programmes</a></p>
    </div>
    <div class="frame frame--photo frame--split span-6 start-7">
      <img class="frame__img" src="images/cmti/corporate-staff-training.webp" srcset="images/cmti/corporate-staff-training-phone.webp 465w, images/cmti/corporate-staff-training.webp 1600w" sizes="(max-width: 639px) 342px, 1100px" alt="A CMTI trainer leading a workshop for corporate staff around a conference table" width="1600" height="952" loading="lazy">
    </div>
  </div>
</section>

<section class="section" id="programmes" style="--h: 2" data-moment="pinned-chapters" aria-labelledby="programmes-h">
  <div class="wrap mo-pc__grid">
    <div class="mo-pc__text">
      <h2 id="programmes-h">How the programmes run</h2>
      <ol class="mo-pc__steps">
        <li class="mo-pc__step">
          <h3>Staff programmes at your sites</h3>
          <p>We map skill gaps with your L&amp;D and operations teams, then train freshers, middle managers and project heads.</p>
          <figure class="mo-pc__visual"><img src="images/cmti/corporate-staff-group.webp" alt="Staff from a CMTI capability development programme outside their office" width="1455" height="1091" loading="lazy"></figure>
        </li>
        <li class="mo-pc__step">
          <h3>Trade training for workmen</h3>
          <p>Formwork, masonry, bar bending, plumbing, waterproofing and finishes, taught on site by trade trainers.</p>
          <figure class="mo-pc__visual"><img src="images/cmti/workmen-bar-bending.webp" alt="Workmen in hard hats learning to use a bar bending machine during CMTI on-site training" width="960" height="720" loading="lazy"></figure>
        </li>
        <li class="mo-pc__step">
          <h3>Construction management course (CACM)</h3>
          <p>Three months of drawings, BOQ, bar bending schedules, sequencing, quality and safety, with site visits.</p>
          <figure class="mo-pc__visual"><img src="images/cmti/site-visit-group.webp" alt="CACM students in hard hats lined up on a construction site visit" width="1600" height="1200" loading="lazy"></figure>
        </li>
        <li class="mo-pc__step">
          <h3>Interior design course (IDM)</h3>
          <p>Three months of layouts, materials, estimates and cut lists, with visits to modular factories and showrooms.</p>
          <figure class="mo-pc__visual"><img src="images/cmti/showroom-visit.webp" alt="IDM students listening to a guide during a showroom visit" width="1600" height="1117" loading="lazy"></figure>
        </li>
      </ol>
      <p class="pc-link"><a class="link" href="cacm.html">See the certified courses</a></p>
    </div>
    <div class="mo-pc__visuals frame"></div>
  </div>
</section>

<section class="section statement" id="trainers" data-moment="word-highlight" aria-label="Trainers">
  <div class="wrap">
    <p class="t-label">Trainers</p>
    <p class="mo-wh__text">CMTI works with 50+ construction and real estate practitioners, most of them <strong>former L&amp;T professionals</strong>. They teach with real project examples and travel to sites from Delhi NCR, Gujarat, Karnataka, Pune, Hyderabad and Chennai.</p>
  </div>
</section>

<section class="section ground-surface" id="recognition" aria-labelledby="recognition-h">
  <div class="wrap">
    <div class="section-head section-head--row">
      <div>
        <h2 id="recognition-h">Training awards and clients</h2>
        <p>Best Skill Development Award at the ISDA Infracon 2025 national awards in New Delhi, and an appreciation from the Towell Group chairman for a programme in Manchester.</p>
      </div>
      <a class="link" href="awards.html">See the awards</a>
    </div>
    <div class="grid">
      <div class="frame frame--photo span-6 pair"><img class="frame__img" src="images/awards/isda-infracon-2025-award.webp" alt="The CMTI team receiving the Best Skill Development Award on stage at ISDA Infracon 2025, New Delhi" width="1600" height="1200" loading="lazy"></div>
      <div class="frame frame--photo span-6 pair"><img class="frame__img" src="images/awards/towell-manchester-appreciation.webp" alt="CMTI receiving an appreciation certificate from the Towell Group chairman in Manchester" width="800" height="615" loading="lazy"></div>
    </div>
    <div class="clients">
      <p class="t-small muted">Clients include</p>
      <div class="logos">{"".join(f'<img src="client-logos/h80/{n}.{e}" alt="{a}" width="{_logo_size(n, e)[0]}" height="{_logo_size(n, e)[1]}" loading="lazy">' for n, e, a in _HOME_CLIENTS)}</div>
    </div>
  </div>
</section>

<section class="section ground-surface" id="feedback" aria-labelledby="feedback-h">
  <div class="wrap">
    <div class="section-head section-head--row">
      <div>
        <h2 id="feedback-h">Feedback from training participants</h2>
        <p>Participants from two client programmes on what the training covered.</p>
      </div>
      <a class="link" href="https://youtube.com/c/CMTIConnect">Watch more on YouTube</a>
    </div>
    <div class="grid">
      {_video_card("wjxFxRWlbUQ", "Muskan Singh", "DLF training by CMTI experts, Gurugram")}
      {_video_card("DmFHuy2J4ow", "Bluewing Design and Constructions", "Formwork training, employee feedback")}
    </div>
  </div>
</section>

<section class="section" id="colleges" aria-labelledby="colleges-h">
  <div class="wrap grid">
    <div class="span-5">
      <div class="section-head">
        <h2 id="colleges-h">College MoUs in 3 states</h2>
        <p>{_N_COLLEGES} engineering colleges in Karnataka, Tamil Nadu and Andhra Pradesh work with CMTI on training, internships and campus hiring.</p>
      </div>
      <ul class="facts">
        <li>300+ hiring companies across construction, real estate, interiors and BIM</li>
        <li>CAD, BIM, planning and estimation training on campus</li>
        <li>Industry partner inputs for NBA accreditation visits</li>
      </ul>
      <p><a class="link" href="colleges.html">See the partner colleges</a></p>
    </div>
    <div class="frame frame--photo frame--split span-6 start-7">
      <img class="frame__img" src="images/cmti/street-group.webp" alt="CMTI students in hard hats with their trainers on a street outside a site" width="1500" height="1125" loading="lazy">
    </div>
  </div>
</section>

<section class="section" id="learn" aria-labelledby="learn-h">
  <div class="wrap">
    <div class="section-head section-head--row">
      <div>
        <h2 id="learn-h">Self-paced courses online</h2>
        <p>{_N_COURSES} courses by construction practitioners on CMTI Civil Engg Connect, {_N_FREE} of them free. Free webinars run every Saturday at 7:00 PM IST.</p>
      </div>
      <a class="link" href="e-learning.html">See all {_N_COURSES} courses</a>
    </div>
    <div class="frame frame--lms">
      <div class="lms ui ui-lms" role="group" aria-label="Free courses on CMTI Civil Engg Connect">
        <div class="lms__bar"><span class="lms__name">CMTI Civil Engg Connect</span><span class="lms__tab">Free courses</span></div>
        <ul class="lms__list">{"".join(_course_row(t) for t in _FREE_PICKS)}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section g2m" id="enquiry" aria-labelledby="enquiry-h">
  <div class="wrap grid">
    <div class="span-5 stack-5">
      <div class="section-head">
        <h2 id="enquiry-h">Contact CMTI about training</h2>
        <p>Tell us who needs training, where and when. We reply within one working day.</p>
      </div>
      <dl class="contact-list">
        <div><dt>Call</dt><dd>{v2.PHONES}</dd></div>
        <div><dt>Email</dt><dd>{v2.EMAIL}</dd></div>
        <div><dt>WhatsApp</dt><dd><a class="wa-link" href="https://wa.me/{v2.WA_NUMBER}">{v2.wa_icon(ROOT)}Message CMTI on WhatsApp</a></dd></div>
      </dl>
    </div>
    <form class="form form--panel span-6 start-7" id="enquiry-form" action="https://wa.me/{v2.WA_NUMBER}" method="get" target="_blank" novalidate>
      <div class="field"><label for="f-name">Full name</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required maxlength="100" aria-describedby="f-name-err">
        <p class="field__error" id="f-name-err" hidden>Write your full name.</p></div>
      <div class="field"><label for="f-phone">Phone</label>
        <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="35" pattern="[\\d\\s\\+\\(\\)\\-]{{7,}}" aria-describedby="f-phone-err">
        <p class="field__error" id="f-phone-err" hidden>Write a phone number we can call, with at least seven digits.</p></div>
      <div class="field"><label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="150" aria-describedby="f-email-err">
        <p class="field__error" id="f-email-err" hidden>Write an email address with an @, like name@company.com.</p></div>
      <div class="field"><label for="f-org">Organisation (optional)</label>
        <input id="f-org" name="organisation" type="text" autocomplete="organization" maxlength="120"></div>
      <div class="field"><label for="programme">Programme</label>
        <select id="programme" name="programme" required aria-describedby="programme-err"><option value="">Choose a programme</option>{_opts}</select>
        <p class="field__error" id="programme-err" hidden>Choose the programme you are asking about.</p></div>
      <div class="field"><label for="f-message">Training needs (optional)</label>
        <textarea id="f-message" name="message" rows="2" maxlength="1000"></textarea></div>
      <div class="btn-row"><button class="btn btn--primary" type="submit">Send an enquiry</button></div>
      <p class="form__status" role="status" data-form-status></p>
      <p class="t-small">Opens WhatsApp with your enquiry written out, ready to send to CMTI.</p>
    </form>
  </div>
</section>
'''
open(f"{ROOT}/index.html", "w", encoding="utf-8").write(clean_links(v2.render_v2(
    ROOT, "CMTI: construction training for companies, colleges and engineers",
    "Construction training in Bengaluru and across India: staff and workmen programmes for EPC and real estate firms, CACM and IDM certified courses, and 76 online courses.",
    home, "Plan your team’s training", "We reply within one working day.",
    moments=("pinned-chapters", "word-highlight"), preload_img="images/cmti/rebar-inspection.webp",
    deal="type: service · deal: hero film, nav nav-mega (redealt from nav-split), close close-type (redealt from close-photo: no unused photograph), footer footer-visit, rhythm surface-pairs, buttons block, mark: CMTI logo · moments: pinned-chapters (#programmes), word-highlight (#trainers)")))
print("wrote index.html (redesign)")

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
  <div class="vm-img"><img src="images/cmti/rebar-inspection.webp" alt="CMTI course participants in hard hats inspecting reinforcement steel on a construction site" loading="lazy" width="1600" height="1200"></div>
  <div class="vm-text">{icon("eye")}<h2 id="vision-title">Vision</h2><p>Our objective is to help construction based professionals be prepared and ready once they enter the industry by providing an extensive module of necessary training that gives them the fundamental skills and paramount level of preparedness to perform tasks and tackle any challenge that lies ahead of them once they enter the building and construction industry.</p></div>
</div>
<div class="vm-block flip reveal">
  <div class="vm-img"><img src="images/cmti/site-visit-group.webp" alt="CACM students in hard hats lined up on a construction site visit" loading="lazy" width="1600" height="1200"></div>
  <div class="vm-text">{icon("target")}<h2>Mission</h2><p>Our services are designed to help individuals improve their chances of building their careers in the construction industry in two different ways. Firstly by providing the required training to be eligible for employment. Secondly by offering placements and opportunities to professionals through our list of excellent, renowned clients and contacts in the construction industry.</p></div>
</div>''', label="vision-title")
vm += cta()
write("vision-mission.html", "Vision &amp; Mission | CMTI", "CMTI’s vision and mission for preparing construction professionals.", vm)

# ================================================================ ASSOCIATIONS
def assoc(logo, abbr, name, text):
    return f'<article class="card reveal"><img class="logo" src="association-logos/{logo}" alt="{abbr} logo" loading="lazy"><p class="label">{abbr}</p><h3>{name}</h3><p>{text}</p></article>'
asc = page_hero("Professional Associations", "Professional network", "Professional associations",
    "CMTI experts regularly participate in conferences, exhibitions and webinars to keep up with emerging industry requirements.",
    "images/cmti/corporate-staff-training.webp", "Areas of professional exchange", ["Civil engineering", "Concrete practice", "Plumbing systems", "Green buildings"])
asc += section('<div class="grid" style="--cols:4">' +
    assoc("acce.jpeg", "ACCE", "Association of Consulting Civil Engineers", "A forum for civil engineers to exchange practical knowledge on design, construction and professional practice.") +
    assoc("ici.jpeg", "ICI", "Indian Concrete Institute", "Promotes knowledge of concrete technology, from materials and mix design to site execution, testing and durability.") +
    assoc("ipa.png", "IPA", "Indian Plumbing Association", "Promotes good practice in plumbing, water supply and sanitation, including efficient use of water in buildings.") +
    assoc("igbc.jpeg", "IGBC", "Indian Green Building Council", "Promotes green building practices, including energy efficiency, water conservation and responsible material use.") +
    "</div>", sid="associations")
asc += cta()
write("associations.html", "Associations | CMTI", "CMTI’s professional associations: ACCE, Indian Concrete Institute, Indian Plumbing Association and Indian Green Building Council.", asc)

# ================================================================ TESTIMONIALS
def story(vid, name, sub):
    yt = f"https://www.youtube.com/watch?v={vid}"
    return f'''<article class="story reveal">
  <button class="video" type="button" data-embed="{vid}" data-title="{name}">
    <span class="thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play" aria-hidden="true"></span></span>
  </button>
  <div class="story-body">
    <span class="story-mark" aria-hidden="true">&ldquo;</span>
    <div><h3>{name}</h3><p>{sub}</p></div>
    {arrow_link("Watch on YouTube", yt)}
  </div>
</article>'''

tst = page_hero("Testimonials", "CMTI testimonials", "Hear from the people we train",
    "Feedback from participants of CMTI training programmes, from on-site corporate training to our certified courses.",
    "images/cmti/site-visit-group.webp",
    actions='<a class="btn btn-white" href="#stories">Watch training feedback</a>',
    extra='<div class="rating-box" style="margin-top:28px"><span class="score">4.7</span><span><span class="stars" style="--rating:4.7" role="img" aria-label="Rated 4.7 out of 5"></span><strong>2,362</strong> Google reviews</span></div>')
tst += section(shead("Training feedback", "In their own words",
    "Participants share their experience of CMTI training delivered for DLF and Bluewing Design and Constructions.", hid="students-title") +
    '<div class="story-grid">' +
    story("wjxFxRWlbUQ", "Muskan Singh", "DLF training by CMTI experts, Gurugram") +
    story("DmFHuy2J4ow", "Bluewing Design and Constructions", "Formwork training · Employee feedback") +
    f'</div><p style="margin-top:28px">{arrow_link("Explore CMTI testimonials on YouTube", "https://www.youtube.com/@CMTICivil/playlists")}</p>', sid="stories", label="students-title")
tst += section(shead("The journey", "From training to your first job", hid="journey-title") +
    '''<ol class="journey reveal">
  <li><span class="j-num">01</span><h3>Learn on real sites</h3><p>Classroom workshops, site visits and hands-on trade demonstrations led by construction industry experts.</p></li>
  <li><span class="j-num">02</span><h3>Prepare for placements</h3><p>Interview preparation and career guidance as students get ready for recruitment.</p></li>
  <li><span class="j-num">03</span><h3>Start your career</h3><p>CMTI coordinates with employers across construction, real estate, interiors and BIM to help students take their first step.</p></li>
</ol>''' + f'<p style="margin-top:36px">{arrow_link("Explore our certified courses", "cacm.html")}</p>',
    cls="section alt", sid="journey", label="journey-title")
tst += cta()
write("testimonials.html", "Testimonials and Reviews | CMTI", "Training feedback from CMTI programmes and CMTI’s Google reviews.", tst)

# ================================================================ E-LEARNING
el = page_hero("E-Learning", "CMTI Civil Engg Connect", "Learn construction skills at your pace",
    "Explore 80+ affordable, self-paced courses delivered by construction industry experts. Designed for civil engineering students, fresh graduates and working professionals.",
    "images/cmti/showroom-visit.webp",
    actions='<a class="btn btn-white" href="https://play.google.com/store/apps/details?id=com.learn.cmti">Download the Android app</a><a class="btn btn-ghost-white" href="https://elearn.cmti.co.in/">Open the e-learning platform</a>')
# Courses offered: data comes from tools/elearn_courses.json (taken from elearn.cmti.co.in)
import json as _json
from html import escape as _esc
ELEARN = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "elearn_courses.json"), encoding="utf-8"))["courses"]
COURSE_CATS = ["Concrete & materials", "Quality, safety & standards", "Quantity surveying & billing",
               "Site & project management", "Software & BIM", "Interiors", "Careers"]

TOPIC_ICONS = {"Concrete & materials": "layers", "Quality, safety & standards": "shield", "Quantity surveying & billing": "rupee",
               "Site & project management": "helmet", "Software & BIM": "monitor", "Interiors": "home", "Careers": "briefcase"}

def topic_block(cat):
    names = [c["title"] for c in ELEARN if c["category"] == cat]
    items = "".join(f"<li>{_esc(n, quote=False)}</li>" for n in names)
    return f"""<article class="topic-block reveal">
  <div class="tb-head">{icon(TOPIC_ICONS[cat])}<h3>{_esc(cat, quote=False)}</h3><span class="tb-count">{len(names)} courses</span></div>
  <ul class="tb-list">{items}</ul>
</article>"""

n_free = sum(1 for c in ELEARN if not c["price"])
el += section(shead("Courses offered", "We offer courses on these topics",
    f"{len(ELEARN)} self-paced construction courses by industry practitioners, including {n_free} free courses, on CMTI Civil Engg Connect.",
    hid="courses-title") +
    '<div class="topic-grid">' + "".join(topic_block(k) for k in COURSE_CATS) + "</div>" +
    '<p class="course-more"><a class="btn btn-primary" href="https://elearn.cmti.co.in/learn/view-all?show=courses&amp;type=1" target="_blank" rel="noopener">Browse all courses</a></p>',
    "section alt", "courses", "courses-title")
el += section(shead("Learn, practise and earn a certificate", "Self-paced lessons · Mock tests · Course e-certificate", hid="app-title") +
    f'''<div class="grid" style="--cols:3">
      {card("Learn anytime", "Fit lessons around work or study and revisit them when you need a refresher.", "clock")}
      {card("Practise with mock tests", "Check your understanding and identify topics to review.", "check")}
      {card("Earn an e-certificate", "Complete the course requirements to earn your certificate.", "award")}
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
fs = page_hero("Advanced Construction Management Course (CACM)", "Certified Courses", "Certificate Course on Advanced Construction Management",
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
  {video("jxEoc8QkPOo", "Certificate Course on Advanced Construction Management", "Certified Courses", "https://youtu.be/jxEoc8QkPOo?si=nEbcd9MJnwgl8fzC")}
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
fs += section(shead("Certified Courses", "More certified courses", hid="more-title") + '<div class="grid" style="--cols:4">' +
    card("Interior Design &amp; Management Course (IDM)", "Certificate Course on Interior Design &amp; Management", None, extra='<img class="card-brand" src="idmti-logo.webp" alt="IDMTI, Interior Design &amp; Management Training Institute" width="600" height="321" loading="lazy">' + arrow_link("Explore the three-month interior design course", "idmti.html")) +
    card("Internships", "Explore practical exposure to construction projects and enquire about current internship opportunities.", "briefcase", cid="internship", extra=arrow_link("Enquire", enquire("Internships"))) +
    card("Construction Software Courses", "Build software skills for construction drawings, quantity estimation and project planning.", "laptop", cid="construction-software", extra=arrow_link("Enquire", enquire("Construction Software Courses"))) +
    card("BIM Design Software", "Explore model-based design and coordination for construction and interiors.", "cpu", cid="bim-design", extra=arrow_link("Enquire", enquire("BIM Design Software"))) +
    "</div>", "section alt", label="more-title")
fs += cta()
write("cacm.html", "Advanced Construction Management Course (CACM) | CMTI", "Certificate Course on Advanced Construction Management: 3 months, offline, online and hybrid, with hands-on exercises and construction site visits.", fs)

# Old address: the CACM page used to live at /finishing-school. Send visitors on, keeping any #section.
REDIRECT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Advanced Construction Management Course (CACM) | CMTI</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="cacm">
<meta http-equiv="refresh" content="0; url=cacm">
<script>location.replace('cacm' + location.search + location.hash)</script>
</head>
<body><p>This page has moved to <a href="cacm">the CACM course page</a>.</p></body>
</html>
"""
open(f"{ROOT}/finishing-school.html", "w", encoding="utf-8").write(REDIRECT)
print("wrote finishing-school.html (redirect)")

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
col = page_hero("College MoUs", "College partnerships", "What a CMTI MoU offers your college", img="images/cmti/street-group.webp",
    tags_label="Campus-to-career support", tags=["Software and workshops", "Internship exposure", "Interview preparation"],
    actions=f'<a class="btn btn-white" href="{enquire("College MoU")}">Discuss a College MoU</a>')
col += '''<div class="stat-strip"><div class="container"><dl style="grid-template-columns:repeat(3,minmax(0,1fr))">
  <div><dt>engineering college partners</dt><dd data-count="100">100+</dd></div>
  <div><dt>engineers placed</dt><dd data-count="5000">5,000+</dd></div>
  <div><dt>companies across construction, real estate, interiors and BIM</dt><dd data-count="300">300+</dd></div>
</dl></div></div>'''
col += section(shead("College partnerships", "Benefits for Colleges Signing an MoU with CMTI", hid="mou-title") + mou_tiles(), label="mou-title")
col += section(college_directory(), label="dir-title")
col += cta()
write("colleges.html", "College MoUs | CMTI", "What a CMTI MoU offers engineering colleges: placements, internships, software training, curriculum development and more.", col)

# ================================================================ CORPORATE (redesign-2026, design-taste-frontend kit)
PC = "Capability Development Programme for Staff"
_CORP_STEPS = {
    "layout": "timeline", "orient": "v", "ground": "none", "motion": {"pulse": "none"},
    "alt": "CMTI builds a programme in five steps: needs discussed with L&D and operations, skill gaps mapped, the session plan agreed, content developed, then training delivered and learning assessed.",
    "steps": [
        {"label": "Needs discussed", "sub": "With L&D and operations", "icon": "ui:messages-square"},
        {"label": "Skill gaps mapped", "sub": "Roles and competencies", "icon": "ui:target"},
        {"label": "Session plan agreed", "sub": "Refined with your team", "icon": "ui:clipboard-check"},
        {"label": "Content developed", "sub": "Tailored to your projects", "icon": "ui:file-pen"},
        {"label": "Learning assessed", "sub": "Delivered and measured", "icon": "ui:graduation-cap"},
    ]}
_TOPICS_V2 = [("Construction management", "Core and shell, formwork, finishes and handover."),
    ("Project management", "Planning, project controls and software tools."),
    ("Quality management", "Quality planning, inspections and corrective actions."),
    ("Safety management", "Hazard identification, risk controls and safe work."),
    ("MEPF", "Mechanical, electrical, plumbing and firefighting systems."),
    ("AI in construction", "Applying AI across construction functions."),
    ("Real estate", "Real estate basics for people outside the sector."),
    ("Finance", "Finance basics for non-finance professionals."),
    ("Customer relationship management", "Customer communication, issues and handover."),
    ("RERA and National Building Code", "Real estate regulation and building code requirements."),
    ("Green buildings, sustainability and ESG", "Resource efficiency and sustainable construction."),
    ("Quality management systems (QMS)", "ISO 9001:2026, audits and third-party certification.")]

def _lucide(name):
    svg = open(os.path.join(ROOT, f"assets/icons/ui-{name}.svg"), encoding="utf-8").read()
    return svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)

def _rows(items):
    return "".join(f'<li><span class="rows__name">{n}</span><p>{t}</p></li>' for n, t in items)

corp = f'''<section class="hero hero--photo" data-enter data-calm="left" aria-labelledby="hero-h">
  <img class="hero__bg" src="images/cmti/corporate-staff-training.webp" srcset="images/cmti/corporate-staff-training-hero-phone.webp 1049w, images/cmti/corporate-staff-training.webp 1600w" sizes="(max-width: 639px) 390px, 100vw" alt="A CMTI trainer leading a workshop for corporate staff around a conference table" width="1600" height="952" style="--ly-pos: 72% 50%; --ly-pos-phone: 50% 50%" fetchpriority="high">
  <div class="wrap"><div class="hero-text">
    <div class="hero__text">
      <h1 id="hero-h">Construction team training</h1>
      <p class="hero__lead">Staff and workmen training for EPC and real estate teams, by 50+ trainers.</p>
      <div class="btn-row"><a class="btn btn--primary" href="{enquire(PC)}">Send an enquiry</a><a class="btn btn--secondary" href="#training-topics">See the training topics</a></div>
    </div>
  </div></div>
</section>

<section class="section" id="process" aria-labelledby="process-h">
  <div class="wrap grid">
    <div class="span-5">
      <div class="section-head">
        <h2 id="process-h">How CMTI builds a training programme</h2>
        <p>Five steps with your L&amp;D and operations teams, led by CMTI’s 50+ practitioner trainers. Scope, duration and format are set to your priorities and budget.</p>
      </div>
      <p><a class="link" href="{enquire(PC)}">Request a training plan</a></p>
    </div>
    <div class="steps-pic frame span-6 start-7" role="img" aria-label="{_CORP_STEPS['alt']}">
      <ol class="steps-pic__list" aria-hidden="true">{"".join(f'<li><span class="steps-pic__ic">{_lucide(st["icon"][3:])}</span><span class="steps-pic__l">{st["label"]}</span><span class="steps-pic__s">{st["sub"]}</span></li>' for st in _CORP_STEPS["steps"])}</ol>
    </div>
  </div>
</section>

<section class="section" id="where" data-moment="photo-chapters" aria-labelledby="where-h">
  <div class="wrap mo-ph">
    <div class="mo-ph__head"><h2 id="where-h">Where the training happens</h2><p>At your offices and on live sites across India, with online and hybrid options.</p></div>
    <ol class="mo-ph__list">
      <li class="mo-ph__ch" id="training-participants">
        <figure class="mo-ph__pic"><img src="images/cmti/corporate-staff-group.webp" alt="Staff from a CMTI capability development programme outside their office" width="1455" height="1091" srcset="images/cmti/corporate-staff-group-phone.webp 666w, images/cmti/corporate-staff-group.webp 1455w" sizes="(max-width: 639px) 360px, 1440px" loading="lazy"></figure>
        <h3>Staff programmes at offices and sites</h3>
        <p>Upskilling for current roles and reskilling for new ones, designed around the work participants do.</p>
      </li>
      <li class="mo-ph__ch">
        <figure class="mo-ph__pic"><img src="images/cmti/rebar-inspection.webp" alt="Trainees in hard hats inspecting reinforcement steel on a construction site" width="1600" height="1200" srcset="images/cmti/rebar-inspection-phone.webp 567w, images/cmti/rebar-inspection.webp 1600w" sizes="(max-width: 639px) 360px, 1440px" loading="lazy"></figure>
        <h3>Practice on live sites</h3>
        <p>Hybrid programmes add site-based practice to online sessions and in-person workshops.</p>
      </li>
      <li class="mo-ph__ch">
        <figure class="mo-ph__pic"><img src="images/cmti/site-visit-group.webp" alt="Trainee engineers in hard hats lined up on a construction site visit" width="1600" height="1200" srcset="images/cmti/site-visit-group-phone.webp 732w, images/cmti/site-visit-group.webp 1600w" sizes="(max-width: 639px) 360px, 1440px" loading="lazy"></figure>
        <h3>Trainee engineer programmes</h3>
        <p>DET and GET programmes with the duration and topics set to your needs, run by CMTI for nine years.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section" id="workmen" aria-labelledby="workmen-h">
  <div class="wrap grid">
    <div class="span-5">
      <div class="section-head">
        <h2 id="workmen-h">Trade training for workmen</h2>
        <p>Experienced trade trainers build practical programmes around your project and the work your crews do on site.</p>
      </div>
      <ul class="rows rows--trades"><li><span class="rows__name">Formwork and scaffolding</span><span class="rows__value">Certification available</span></li>{"".join(f'<li><span class="rows__name">{t}</span></li>' for t in ("Masonry", "Bar bending", "Plumbing", "Waterproofing", "Finishing works"))}</ul>
    </div>
    <figure class="develop span-6 start-7" data-moment="picture-develops"><img src="images/cmti/workmen-bar-bending.webp" alt="Workmen in hard hats learning to use a bar bending machine during CMTI on-site training" width="960" height="720" loading="lazy" data-full></figure>
  </div>
</section>

<section class="section" id="training-topics" aria-labelledby="topics-h">
  <div class="wrap">
    <div class="section-head section-head--row">
      <div>
        <h2 id="topics-h">12 training topics</h2>
        <p>Middle managers with 3 to 15 years of experience take a two-day workshop on topics chosen with your team; project heads with 15+ years take workshops built around senior responsibilities.</p>
      </div>
      <a class="link" href="{enquire(PC)}">Ask about a topic</a>
    </div>
    <div class="grid">
      <ul class="rows span-4">{_rows(_TOPICS_V2[0:4])}</ul>
      <ul class="rows span-4">{_rows(_TOPICS_V2[4:8])}</ul>
      <ul class="rows span-4">{_rows(_TOPICS_V2[8:12])}</ul>
    </div>
  </div>
</section>

<section class="section" id="services" aria-labelledby="services-h">
  <div class="wrap grid">
    <div class="span-5">
      <div class="section-head">
        <h2 id="services-h">Support services for L&amp;D teams</h2>
        <p>Beyond training, CMTI helps L&amp;D teams write material, measure skills and hire engineers.</p>
      </div>
      <ul class="rows">
        <li id="content-development"><span class="rows__name">Content development</span><span class="rows__value">SOPs</span><p>SOPs and training material for your in-house learning system, written around your workflows.</p></li>
        <li id="assessment"><span class="rows__name">Employee assessment</span><span class="rows__value">Skill gaps</span><p>Periodic assessments with internationally used tools, reporting gaps and training priorities.</p></li>
        <li id="hiring"><span class="rows__name">Hiring support</span><span class="rows__value">100+ colleges</span><p>Campus hiring for entry-level engineering roles through CMTI's partner colleges.</p></li>
      </ul>
    </div>
    <div class="frame frame--photo frame--split span-6 start-7">
      <img class="frame__img" src="images/cmti/street-group.webp" alt="Engineering trainees in hard hats with their CMTI trainers outside a site" width="1500" height="1125" loading="lazy">
    </div>
  </div>
</section>

<section class="section ground-surface" id="client-logos" aria-labelledby="clients-h">
  <div class="wrap">
    <div class="section-head section-head--row">
      <div>
        <h2 id="clients-h">Clients and training awards</h2>
        <p>Programmes for real estate, EPC and government clients including ISRO, and for the Towell Group in Manchester. Participant feedback is tracked by Net Promoter Score.</p>
      </div>
      <a class="link" href="awards.html">See the awards</a>
    </div>
    <div class="grid">
      <div class="frame frame--photo span-6 pair"><img class="frame__img" src="images/awards/isda-infracon-2025-award.webp" alt="The CMTI team receiving the Best Skill Development Award on stage at ISDA Infracon 2025, New Delhi" width="1600" height="1200" loading="lazy"></div>
      <div class="frame frame--photo span-6 pair"><img class="frame__img" src="images/awards/towell-manchester-appreciation.webp" alt="CMTI receiving an appreciation certificate from the Towell Group chairman in Manchester" width="800" height="615" loading="lazy"></div>
    </div>
    <div class="clients">
      <p class="t-small muted">Clients include</p>
      <div class="logos">{"".join(f'<img src="client-logos/h80/{n}.{e}" alt="{a}" width="{_logo_size(n, e)[0]}" height="{_logo_size(n, e)[1]}" loading="lazy">' for n, e, a in _HOME_CLIENTS)}</div>
    </div>
  </div>
</section>
'''
open(f"{ROOT}/corporate.html", "w", encoding="utf-8").write(clean_links(v2.render_v2(
    ROOT, "CMTI for companies: construction training for staff and workmen",
    "Construction training for EPC, real estate and government teams across India: staff and workmen programmes, 12 training topics, content development, employee assessment and hiring support.",
    corp, "Plan your team’s training", "We reply within one working day.", current="corporate.html",
    moments=("photo-chapters", "picture-develops"), preload_img="images/cmti/corporate-staff-training.webp",
    preload_set=("images/cmti/corporate-staff-training-hero-phone.webp 1049w, images/cmti/corporate-staff-training.webp 1600w", "(max-width: 639px) 390px, 100vw"),
    deal="type: service · deal: hero photo (data-calm left), nav nav-mega, close close-type, footer footer-visit, rhythm surface-pairs, buttons block · moments: photo-chapters (#where), picture-develops (#workmen) · a still illustration of the five steps (#process)")))
print("wrote corporate.html (redesign)")

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
        slides = [pic(img, alt, w, h, title), pic(*extra, title + " (certificate)")]
        pics = (f'<div class="award-slider" data-slider aria-roledescription="carousel" aria-label="{title} photos">'
                f'<div class="slider-track" tabindex="0">' + "".join(f'<div class="slide" role="group" aria-roledescription="slide" aria-label="{i + 1} of {len(slides)}">{s}</div>' for i, s in enumerate(slides)) + '</div>'
                '<button class="slider-btn prev" type="button" aria-label="Previous photo"></button>'
                '<button class="slider-btn next" type="button" aria-label="Next photo"></button>'
                '<div class="slider-dots">' + "".join(f'<button type="button" aria-label="Show photo {i + 1}"></button>' for i in range(len(slides))) + '</div></div>')
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
          "For conducting a two-week programme for Omani officials at Manchester, UK.</p><p>Presented to CMTI in recognition of the successful design and delivery of the 5-day Executive Programme in Infrastructure Leadership &amp; Project Excellence for Nama Water Services, organised by Towell Infrastructure Projects LLC, for senior engineers, managers and support staff.",
          extra=("images/awards/towell-programme-certificate.webp", "The certificate presented to CMTI by Towell Infrastructure Projects LLC", 1308, 887)) +
    '</div>', label=None)
aw += cta()
write("awards.html", "Awards &amp; Certificates | CMTI", "Awards and certificates received by CMTI, including the Best Skill Development Award at the ISDA Infracon 2025 National Level Awards, New Delhi.", aw)

