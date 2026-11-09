"""Generate CMTI inner pages using the homepage's header, footer and quick-contact bar.

Run from the repository root after changing the header or footer in index.html:
    python3 tools/build_pages.py .
It rewrites about, vision-mission, associations, testimonials, e-learning,
finishing-school, idmti, colleges and corporate (.html). Edit page content here,
not in the generated files, or the next run will overwrite your edits.
"""
import re, sys
from urllib.parse import quote

ROOT = sys.argv[1]
index = open(f"{ROOT}/index.html", encoding="utf-8").read()

def between(start, end):
    i = index.index(start)
    return index[i:index.index(end, i) + len(end)]

HEADER = between('<header class="masthead">', '</header>').replace('href="#contact"', 'href="index.html#contact"')
FOOTER = between('<footer class="site-footer">', '</footer>').replace('href="#contact"', 'href="index.html#contact"')
QUICK = between('<div class="quick-contact">', '</a>\n</div>')
GOOGLE = "https://www.google.com/maps/search/?api=1&amp;query=Construction+Management+Training+Institute+Jayanagar+Bengaluru"

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
    "drop": "M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11Z",
    "target": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-5a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z",
    "eye": "M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Zm10 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z",
    "check": "M5 12l4 4 10-10",
    "handshake": "M3 12l4-4 5 2 5-2 4 4M7 8l5 6 3-2M3 12l6 6 3-2 3 2 6-6",
    "ruler": "M3 17 17 3l4 4L7 21l-4-4ZM7 13l2 2M10 10l2 2M13 7l2 2",
    "chat": "M4 5h16v11H8l-4 4V5Z",
}

def icon(name):
    return f'<span class="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg></span>'

def enquire(programme):
    return "index.html?programme=" + quote(programme) + "#contact"

def crumbs(*items):
    li = ['<li><a href="index.html">Home</a></li>']
    for label, href in items:
        li.append(f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>')
    return '<ol class="crumbs" aria-label="Breadcrumb">' + "".join(li) + "</ol>"

def page_hero(crumb, kicker, title, lede, chips="", actions="", media="", extra="", amber=False):
    chips_html = ""
    if chips:
        chips_html = f'<ul class="chips{" amber" if amber else ""}">' + "".join(f"<li>{c}</li>" for c in chips) + "</ul>"
    cls = "page-hero" + ("" if media else " no-media")
    return f'''<section class="{cls}" aria-labelledby="page-title">
  <div class="page-hero-inner">
    <div class="page-hero-copy hero-copy">
      {crumb}
      <p class="kicker">{kicker}</p>
      <h1 id="page-title">{title}</h1>
      <p class="lede">{lede}</p>
      {chips_html}
      {f'<div class="hero-actions">{actions}</div>' if actions else ''}
      {extra}
    </div>
    {f'<div class="page-hero-media">{media}</div>' if media else ''}
  </div>
</section>'''

def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{desc}">
<title>{title} | CMTI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="site.css">
<script>document.documentElement.classList.add("js")</script>
<script src="site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def cta(title="Ready to talk about training?", text="Tell us who needs training and what they need to learn.", programme="Something else", button="Send an enquiry"):
    return f'''<section class="section page-end">
  <div class="container">
    <div class="cta-band reveal">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
        <p class="promise"><span class="promise-dot" aria-hidden="true"></span>We reply within one working day.</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-light" href="{enquire(programme)}">{button}</a>
        <a class="btn btn-outline-light" href="tel:+918884422179">Call +91 88844 22179</a>
      </div>
    </div>
  </div>
</section>'''

DIALOG = '''<dialog class="video-dialog" aria-label="Video">
  <div class="video-frame"></div>
  <button class="video-close" type="button">Close video</button>
</dialog>'''

def video_card(vid, name, sub):
    return f'''<button class="story-card reveal" type="button" data-video="{vid}" data-title="{name}">
  <span class="story-thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="play" aria-hidden="true"></span></span>
  <span class="story-meta"><strong>{name}</strong><span>{sub}</span></span>
  <span class="sr-only">Play video</span>
</button>'''

def card(ic, title, text, extra="", label="", cid=""):
    idattr = f' id="{cid}"' if cid else ""
    lab = f'<p class="card-label">{label}</p>' if label else ""
    return f'<article class="card reveal"{idattr}>{icon(ic) if ic else ""}{lab}<h3>{title}</h3><p>{text}</p>{extra}</article>'

def section(inner, cls="section", label=None, sid=None):
    attrs = f' id="{sid}"' if sid else ""
    attrs += f' aria-labelledby="{label}"' if label else ""
    return f'<section class="{cls}"{attrs}>\n  <div class="container">\n{inner}\n  </div>\n</section>'

def head_block(kicker, title, text="", hid=None):
    hid_attr = f' id="{hid}"' if hid else ""
    return f'<div class="section-head reveal">{f"<p class=\"kicker\">{kicker}</p>" if kicker else ""}<h2{hid_attr}>{title}</h2>{f"<p>{text}</p>" if text else ""}</div>'

def write(name, title, desc, body, video=False):
    html = head(title, desc) + "\n" + HEADER + "\n\n<main id=\"main\">\n" + body + "\n</main>\n\n" + (DIALOG + "\n\n" if video else "") + FOOTER + "\n\n" + QUICK + "\n</body>\n</html>\n"
    open(f"{ROOT}/{name}", "w", encoding="utf-8").write(html)
    print("wrote", name, len(html))

CLIENTS = [(1, "png", "DLF"), (2, "png", "Godrej Properties"), (3, "png", "Hines"), (4, "png", "ISRO"),
    (5, "jpeg", "L&amp;T Institute of Project Management"), (6, "png", "Larsen &amp; Toubro"), (7, "png", "M3M"),
    (8, "png", "Prestige Group"), (9, "jpeg", "Sattva Group"), (10, "jpeg", "Signature Global"), (11, "png", "Tata Projects"),
    (12, "jpeg", "Adarsh Group"), (13, "png", "Birla Estates"), (14, "jpeg", "Blue Wing Design and Construction"),
    (15, "png", "Cemindia"), (16, "png", "Century"), (17, "jpeg", "H.G. Infra Engineering"), (18, "png", "KEC International"),
    (19, "jpeg", "KNK"), (20, "png", "Piramal Realty"), (21, "jpeg", "Ramky Estates"), (22, "jpeg", "Ramky Infrastructure"),
    (23, "png", "Riviera Infraprojects"), (24, "png", "Shapoorji Pallonji"), (25, "png", "Sowparnika"),
    (26, "jpeg", "Spartan Builders"), (27, "jpeg", "Sumadhura"), (28, "png", "Uniqcore")]
LOGO_WALL = '<ul class="logo-wall reveal">' + "".join(
    f'<li><img src="client-logos/{n}.{ext}" alt="{alt}" loading="lazy"></li>' for n, ext, alt in CLIENTS) + "</ul>"

COLLEGES = [("bmsit", "BMSIT"), ("presidency", "Presidency University"), ("sharnbasava", "Sharnbasava University"),
    ("kpriet", "KPRIET"), ("karunya", "Karunya"), ("sona", "Sona College"), ("rgm", "RGM Nandyal"),
    ("gndec", "Guru Nanak Dev, Bidar"), ("bgsit", "BGSIT"), ("gprec", "G. Pulla Reddy Engineering College"),
    ("nitte", "Nitte Meenakshi Institute of Technology")]

def team_cards():
    people = [
        ("AK", "Er. S. G. Ashok Kumar", "Founder and CEO", "PMP, IGBC AP, 26 years in construction", "Founded CMTI and established IDMTI to develop interior design professionals. He leads the CMTI Finishing School, corporate training, industry readiness programmes and partnerships. His experience includes L&amp;T highway and airport projects, and he serves on the IGBC Core Committee.", "https://www.linkedin.com/in/er-ashok-kumar-b645126b/"),
        ("SD", "Er. S. K. Deepasree", "Co-founder and Head of Operations", "22 years of academic experience", "Oversees the CMTI and IDMTI finishing schools. She leads placements, coordinates with employers, guides students through recruitment and career decisions, and manages human resources.", "https://www.linkedin.com/in/s-k-deepasree/"),
        ("SA", "Er. Sachin Amarnath", "Partner, corporate training initiatives", "10 years of experience", "A project management and learning and development professional. He assesses client needs, develops content, and designs and delivers capability development programmes for project teams.", "https://www.linkedin.com/in/sachin-amarnath/"),
        ("MD", "Mr. Manish Dave", "Collaboration partner and quality leader", "35+ years in construction", "Supports business development and client acquisition in Gujarat, and helps develop training programmes using his expertise in construction quality and site practices.", "https://www.linkedin.com/in/manish-dave-464081296/"),
    ]
    out = []
    for ini, name, role, exp, text, li in people:
        out.append(f'''<article class="person reveal">
  <span class="avatar" aria-hidden="true">{ini}</span>
  <h3>{name}</h3>
  <p class="role">{role}</p>
  <p><strong>{exp}</strong></p>
  <p>{text}</p>
  <a class="text-link" href="{li}">LinkedIn<span class="sr-only"> profile of {name}</span></a>
</article>''')
    return '<div class="team-grid">' + "".join(out) + "</div>"

# ======================= ABOUT =======================
about = page_hero(
    crumbs(("About CMTI", None)), "About CMTI",
    "Preparing professionals for construction careers since 2018",
    "CMTI is one of India's leading construction edtech institutes, delivering industry-led skilling across India.",
    chips=["Technical foundations", "Practitioner-led training", "Project applications"],
    actions=f'<a class="btn btn-primary" href="index.html#courses">Explore programmes</a><a class="btn btn-ghost" href="#team">Meet the team</a>',
    media='<img src="images/photos/site-team.webp" alt="Engineers in safety vests reviewing a construction site" width="1400" height="934">',
    extra='<dl class="hero-stats"><div><dt>Founded</dt><dd>2018</dd></div><div><dt>Engineers placed</dt><dd data-count="5000">5,000+</dd></div><div><dt>Partner colleges</dt><dd data-count="100">100+</dd></div><div><dt>Hiring companies</dt><dd data-count="300">300+</dd></div></dl>',
)
about += section(f'''<div class="split-2">
  <div class="prose reveal">
    <p class="kicker">Our story</p>
    <h2 id="story-title">From one founder's site experience to a pan-India institute</h2>
    <p class="lead-text">Er. S. G. Ashok Kumar, PMP, founded the Construction Management Training Institute in 2018. With guidance from Er. V. Suresh, a senior industry leader in building and construction standards, CMTI has expanded its training and placement activities across India.</p>
  </div>
  <div class="card-grid" style="--cols:1">
    {card("cap", "College training and placements", "On-campus and off-campus training, internship support and campus interviews for engineering students. CMTI partners with <strong>100+ engineering colleges</strong>, has placed <strong>5,000+ engineers</strong> in construction and interiors roles, and works with <strong>300+ companies</strong> across construction, real estate, interiors and BIM.", '<a class="text-link" href="colleges.html">Explore college partnerships</a>')}
    {card("building", "Corporate, government and international training", "CMTI is a technical training partner to real estate and engineering, procurement and construction (EPC) companies. It delivers capability development programmes at project sites across India, has trained the Indian Space Research Organisation (ISRO), and delivered an international programme for Towell Group in Manchester, UK.", '<a class="text-link" href="corporate.html">Explore corporate training</a>')}
  </div>
</div>''', label="story-title")
about += section(f'''<div class="callout reveal">
  {icon("chart")}
  <div>
    <h2 id="skills-title">Construction skills for a developed India</h2>
    <p>NITI Aayog's August 2026 skilling report emphasises flexible, lifelong learning aligned with industry needs. In construction, foundational skilling helps new entrants read drawings, measure work and follow site procedures. Reskilling helps experienced professionals move into roles that use BIM, digital quality tools and new construction methods. Upskilling helps project teams improve planning, safety, quality and resource efficiency as India builds towards Viksit Bharat 2047.</p>
    <p class="source">Source inspiration: NITI Aayog, <cite>Reimagining Skilling for Viksit Bharat@2047</cite>, August 2026.</p>
  </div>
</div>''', label="skills-title")
about += section('''<div class="mentor reveal">
  <span class="avatar" aria-hidden="true">VS</span>
  <div>
    <p class="kicker">CMTI mentor</p>
    <h2 id="mentor-title">Er. V. Suresh</h2>
    <p class="role">Former Chairman &amp; Managing Director, HUDCO</p>
    <p>Er. V. Suresh is a senior civil engineer whose work spans housing, infrastructure and urban development. He has contributed to national building standards and the National Building Code, bringing decades of experience in the built environment.</p>
    <p>As CMTI's mentor, he encourages construction education, practical skilling and knowledge sharing. His guidance inspires CMTI's efforts to prepare industry-ready professionals and promote green building awareness.</p>
    <a href="https://www.linkedin.com/in/suresh-vasudevan-349253157/">Connect with Er. V. Suresh on LinkedIn</a>
  </div>
</div>''', label="mentor-title", sid="mentor")
about += section(head_block("Leadership", "The team behind CMTI", hid="team-title") + team_cards(), label="team-title", sid="team")
about += section(head_block("People behind the programmes", "Our trainer network",
    "CMTI works with <strong>50+ construction and real estate practitioners</strong>, most of whom are former L&amp;T professionals. They use real project examples to connect training with on-site practice.", hid="trainers-title") +
    '<ul class="chips reveal"><li>Delhi NCR</li><li>Gujarat</li><li>Karnataka</li><li>Pune</li><li>Hyderabad</li><li>Chennai</li></ul>'
    '<p class="reveal" style="max-width:68ch;color:var(--muted)">Trainers are based across these regions and travel to project sites and training venues as required.</p>'
    '<div class="card-grid" style="--cols:3">' +
    card("helmet", "Er. S. G. Ashok Kumar", "PMP, IGBC AP. 26 years of construction industry experience, including highway and airport projects.", label="Founder and CEO") +
    card("chart", "Vijay Gupta", "PMP-certified project management instructor.", label="Project management") +
    card("chat", "Madhukeshwar Jaglur", "Senior project management professional and CMTI webinar speaker on cost priorities and AI prompt engineering.", label="Visiting speaker") +
    '</div><p style="margin-top:24px"><a class="text-link" href="' + enquire("Corporate Training") + '">Request trainer profiles for your programme</a></p>',
    cls="section tint", label="trainers-title", sid="trainers")
about += section(head_block("Clients", "Companies we have trained teams for", "Real estate developers, EPC contractors and public organisations across India.", hid="clients-title") + LOGO_WALL, label="clients-title", sid="clients")
about += cta()
write("about.html", "About CMTI", "CMTI has trained construction professionals since 2018: our story, mentor, leadership team, trainer network and clients.", about)

# ======================= VISION & MISSION =======================
vm = page_hero(crumbs(("About", "about.html"), ("Vision and mission", None)), "What guides CMTI", "Vision and mission",
    "Why CMTI exists and how we help people build careers in construction.",
    chips=["Technical foundations", "Practitioner-led training", "Project applications"])
vm += section(f'''<div class="split-2">
  <article class="statement reveal">{icon("eye")}<h2 id="vision-title">Vision</h2><p>Our objective is to help construction based professionals be prepared and ready once they enter the industry by providing an extensive module of necessary training that gives them the fundamental skills and paramount level of preparedness to perform tasks and tackle any challenge that lies ahead of them once they enter the building and construction industry.</p></article>
  <article class="statement reveal">{icon("target")}<h2>Mission</h2><p>Our services are designed to help individuals improve their chances of building their careers in the construction industry in two different ways. Firstly by providing the required training to be eligible for employment. Secondly by offering placements and opportunities to professionals through our list of excellent, renowned clients and contacts in the construction industry.</p></article>
</div>''', label="vision-title")
vm += section(head_block("In practice", "How the mission shows up in our programmes", hid="practice-title") + '<div class="card-grid" style="--cols:3">' +
    card("book", "Training for employment", "Three-month certificate courses in construction management and interior design build the skills employers ask for.", '<a class="text-link" href="finishing-school.html">See the courses</a>') +
    card("briefcase", "Placements and opportunities", "Résumé guidance, mock interviews and campus interviews with CMTI's network of 300+ hiring companies.", '<a class="text-link" href="colleges.html">How placements work</a>') +
    card("helmet", "Practitioner-led", "50+ trainers, most of them former L&amp;T professionals, connect every lesson to real site practice.", '<a class="text-link" href="about.html#trainers">Meet the trainers</a>') +
    "</div>", cls="section", label="practice-title")
vm += cta()
write("vision-mission.html", "Vision and mission", "CMTI's vision and mission: preparing construction professionals for the industry through training and placements.", vm)

# ======================= ASSOCIATIONS =======================
assoc = page_hero(crumbs(("About", "about.html"), ("Professional associations", None)), "Professional network", "Professional associations",
    "CMTI experts regularly participate in conferences, exhibitions and webinars to keep up with emerging industry requirements.",
    chips=["Civil engineering", "Concrete practice", "Plumbing systems", "Green buildings"])
def assoc_card(logo, abbr, name, text):
    return f'<article class="card reveal"><img class="card-logo" src="association-logos/{logo}" alt="" loading="lazy"><p class="card-label">{abbr}</p><h3>{name}</h3><p>{text}</p></article>'
assoc += section(head_block("Our associations", "Where CMTI's experts exchange knowledge", hid="assoc-title") + '<div class="card-grid" style="--cols:4">' +
    assoc_card("acce.jpeg", "ACCE", "Association of Consulting Civil Engineers", "A forum for civil engineers to exchange practical knowledge on design, construction and professional practice.") +
    assoc_card("ici.jpeg", "ICI", "Indian Concrete Institute", "Promotes knowledge of concrete technology, from materials and mix design to site execution, testing and durability.") +
    assoc_card("ipa.png", "IPA", "Indian Plumbing Association", "Promotes good practice in plumbing, water supply and sanitation, including efficient use of water in buildings.") +
    assoc_card("igbc.jpeg", "IGBC", "Indian Green Building Council", "Promotes green building practices, including energy efficiency, water conservation and responsible material use.") +
    "</div>", label="assoc-title")
assoc += cta()
write("associations.html", "Professional associations", "CMTI's professional associations: ACCE, Indian Concrete Institute, Indian Plumbing Association and IGBC.", assoc)

# ======================= TESTIMONIALS =======================
test = page_hero(crumbs(("Student stories", None)), "CMTI Finishing School", "From training to your first job",
    "Hear students share what they learnt, how they prepared for placements, and what it felt like to take their first step into the industry.",
    extra=f'''<a class="review-summary" href="{GOOGLE}" target="_blank" rel="noopener" style="margin:8px 0 0">
      <span class="review-score">4.7</span>
      <span class="review-detail"><span class="stars stars-lg" style="--rating:4.7" role="img" aria-label="Rated 4.7 out of 5"></span><span>Rated by <strong>2,362</strong> students and professionals on Google</span></span>
      <span class="review-cta">Read the reviews</span>
    </a>''')
test += section(head_block("Videos", "Hear from CMTI students", hid="videos-title") + '<div class="story-grid">' +
    video_card("gd1zW_J2vXc", "Keerthana", "Finishing School student") +
    video_card("vd9OFFVTzVo", "Amrita Bhat", "Finishing School student") +
    video_card("jxEoc8QkPOo", "Inside the CACM course", "Construction management") +
    '</div><p class="stories-more"><a class="text-link" href="https://www.youtube.com/@CMTICivil/playlists">Explore CMTI testimonials on YouTube</a></p>',
    label="videos-title")
test += section(f'''<div class="callout reveal">
  {icon("chat")}
  <div>
    <h2 id="share-title">Share your first-job story</h2>
    <p>Recently placed or started your first job? Tell us about your new role, what helped you prepare, and what you'd like the next batch to know. You can include a link to your video and let us know if we may feature it.</p>
    <p style="margin-top:18px"><a class="btn btn-primary" href="mailto:cmtioffice@cmti.co.in?subject=My%20CMTI%20first-job%20story">Share your story by email</a></p>
  </div>
</div>''', label="share-title")
test += cta("Start your own story", "Join the next batch of the construction management or interior design course.", "CMTI Finishing School (CACM)", "Enquire about a course")
write("testimonials.html", "Student stories", "Student testimonials from the CMTI Finishing School, plus CMTI's 4.7 Google rating from 2,362 reviews.", test, video=True)

# ======================= E-LEARNING =======================
el = page_hero(crumbs(("E-learning", None)), "CMTI Civil Engg Connect", "Learn construction skills at your pace",
    "Explore 80+ affordable, self-paced courses delivered by construction industry experts. Designed for civil engineering students, fresh graduates and working professionals.",
    chips=["80+ courses", "Mock tests", "E-certificates"], amber=True,
    actions='<a class="btn btn-primary" href="https://play.google.com/store/apps/details?id=com.learn.cmti">Download the Android app</a><a class="btn btn-ghost" href="https://elearn.cmti.co.in/">Open the e-learning platform</a>',
    media='<img src="images/app-preview.png" alt="CMTI Civil Engg Connect app preview from Google Play" class="app-shot" style="aspect-ratio:auto;object-fit:contain">')
el += section(head_block("How it works", "Learn, practise and earn a certificate", hid="how-title") + '<div class="card-grid" style="--cols:3">' +
    card("clock", "Learn anytime", "Fit lessons around work or study and revisit them when you need a refresher.") +
    card("check", "Practise with mock tests", "Check your understanding and identify topics to review.") +
    card("award", "Earn an e-certificate", "Complete the course requirements to earn your certificate.") +
    "</div>", label="how-title")
el += section('''<div class="webinar-band reveal">
  <div>
    <p class="kicker">CMTI webinars</p>
    <h2 id="webinars-title">Free webinars led by industry practitioners</h2>
    <p>CMTI regularly hosts free webinars and provides a certificate of participation. Follow our WhatsApp channel and LinkedIn page for upcoming topics, dates and registration details.</p>
    <ul class="chips"><li>Free expert-led session</li><li>Topic updates via WhatsApp and LinkedIn</li><li>Certificate of participation</li></ul>
    <div class="cta-actions"><a class="btn btn-light" href="https://whatsapp.com/channel/0029Va4S47dEgGfOPitXTT2f">Follow on WhatsApp</a><a class="btn btn-outline-light" href="https://www.linkedin.com/company/cmtionline/">Follow on LinkedIn</a></div>
    <p style="margin:18px 0 0"><a href="https://linktr.ee/cmti" style="color:#fff;font-weight:700">Find CMTI on YouTube, Instagram and Telegram</a></p>
  </div>
  <div class="webinar-time">
    <strong>Saturdays at 7:00 PM IST</strong>
    <p>Construction, quality, digital construction, interiors and trending industry topics.</p>
  </div>
</div>''', label="webinars-title", sid="webinars")
el += cta("Prefer a classroom course?", "Our three-month certificate courses add site visits and placement support.", "E-learning and webinars", "Ask about courses")
write("e-learning.html", "E-learning and webinars", "CMTI Civil Engg Connect: 80+ self-paced construction courses with mock tests and e-certificates, plus free Saturday webinars.", el)

# ======================= FINISHING SCHOOL (CACM) =======================
P_CACM = "CMTI Finishing School (CACM)"
fs = page_hero(crumbs(("Courses", "index.html#courses"), ("Construction management", None)), "CMTI Finishing School",
    "Certificate Course on Advanced Construction Management",
    "A three-month course with hands-on exercises and construction site visits that prepares you for day-to-day site responsibilities.",
    chips=["3 months", "Offline, online and hybrid", "Site visits"], amber=True,
    actions=f'<a class="btn btn-primary" href="{enquire(P_CACM)}">Enquire about the course</a><button class="btn btn-ghost" type="button" data-video="jxEoc8QkPOo" data-title="CACM course video">Watch the course video</button>',
    media='<img src="images/photos/site-rebar.webp" alt="Workers fixing reinforcement on a building site" width="900" height="655">'
          '<div class="float-card fc-2"><span class="fc-icon fc-amber" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3 2 8l10 5 8-4v6h2V8L12 3Zm-6 9v4c0 1.7 2.7 3 6 3s6-1.3 6-3v-4l-6 3-6-3Z"/></svg></span><span><strong>5,000+</strong> engineers placed</span></div>')
fs += section(head_block("Skills you practise", "Drawings, BOQ and BBS, construction sequencing, and site quality and safety", hid="apply-title") +
    '<div class="card-grid" style="--cols:3">' +
    card("users", "Eligibility", "Diploma holders, graduates and postgraduates, including freshers and young professionals with one to two years of experience.", label="Who should apply") +
    card("target", "Target audience", "Aspiring construction professionals who want practical skills in site execution, quantity estimation, quality and safety. The course also supports those preparing for job interviews or exploring construction entrepreneurship.", label="Who it's for") +
    '<div class="video-card">' + video_card("jxEoc8QkPOo", "Watch: the CACM course", "Construction management") + '</div>' +
    "</div>", label="apply-title")
fs += section(f'''<div class="callout reveal">{icon("ruler")}<div><h2 id="objective-title">Programme objective</h2><p>Prepare participants for day-to-day site responsibilities by building their ability to interpret drawings and specifications, understand construction materials, perform calculations, estimate quantities and costs, and sequence construction activities.</p></div></div>''', label="objective-title")
fs += section(head_block("Learning outcomes", "What you will be able to do", hid="outcomes-title") + '<ul class="tick-list reveal">' + "".join(f"<li>{x}</li>" for x in [
    "Interpret drawings and specifications, convert units, and take site measurements.",
    "Identify cement, aggregates, reinforcement steel and masonry units, and explain their properties, uses and basic quality checks.",
    "Calculate area, volume, material quantities and reinforcement weight.",
    "Prepare Bills of Quantities (BOQs), Bar Bending Schedules (BBS) and rate analyses.",
    "Sequence construction activities and explain where formwork, construction methods and site execution procedures fit.",
    "Identify quality checks and safety practices and relate them to activities observed during site visits.",
    "Use AutoCAD, SketchUp and BIM tools in construction workflows.",
    "Prepare for job interviews and identify the first steps towards starting a construction business."]) + "</ul>",
    cls="section tint", label="outcomes-title")
fs += section(head_block("More from the Finishing School", "Internships, software and BIM", hid="more-title") + '<div class="card-grid" style="--cols:3">' +
    card("briefcase", "Internships", "Explore practical exposure to construction projects and enquire about current internship opportunities.", f'<a class="text-link" href="{enquire(P_CACM)}">Enquire</a>', cid="internship") +
    card("laptop", "Construction software courses", "Build software skills for construction drawings, quantity estimation and project planning.", f'<a class="text-link" href="{enquire(P_CACM)}">Enquire</a>', cid="construction-software") +
    card("layers", "BIM design software", "Explore model-based design and coordination for construction and interiors.", f'<a class="text-link" href="{enquire(P_CACM)}">Enquire</a>', cid="bim-design") +
    "</div>", label="more-title")
fs += cta("Join the next CACM batch", "Tell us about your background and we'll help you choose the right format.", P_CACM, "Enquire about the course")
write("finishing-school.html", "Construction management course (CACM)", "Three-month Certificate Course on Advanced Construction Management with site visits, software training and placement support.", fs, video=True)

# ======================= IDMTI =======================
P_IDM = "IDMTI Interior Design (IDM)"
idm = page_hero(crumbs(("Courses", "index.html#courses"), ("Interior design", None)), "Interior Design &amp; Management Training Institute",
    "Certificate Course on Interior Design &amp; Management",
    "Founded by Er. S. G. Ashok Kumar, IDMTI prepares aspiring professionals for residential and commercial interiors.",
    chips=["3 months", "Offline, online and hybrid", "Factory and site visits"], amber=True,
    actions=f'<a class="btn btn-primary" href="{enquire(P_IDM)}">Enquire about the course</a><button class="btn btn-ghost" type="button" data-video="5kdH5vo8Wio" data-title="IDM course video">Watch the course video</button>',
    media='<img src="images/photos/plans-desk.webp" alt="Designer marking up drawings at a desk" width="900" height="600">',
    extra='<p style="margin:24px 0 0;color:var(--muted)"><strong style="color:var(--navy)">Alumni have worked with</strong> HomeLane, DesignCafe, Bonito Designs and Purva Streaks.</p>')
idm += section(head_block("How an interior fit-out comes together", "Design and layouts, modular production and site installation", hid="idm-apply") + '<div class="card-grid" style="--cols:4">' +
    card("users", "Eligibility", "Diploma holders, graduates and postgraduates, including freshers and young professionals with one to two years of experience.", label="Who should apply") +
    card("target", "Target audience", "Aspiring interior design professionals and early-career professionals interested in large-scale interior projects.", label="Who it's for") +
    card("ruler", "Programme objective", "Learn to gather client requirements, prepare drawings and estimates, select materials and hardware, and understand how designs move from factory production to site installation.", label="What you'll learn") +
    '<div class="video-card">' + video_card("5kdH5vo8Wio", "Watch: the IDM course", "Interior design") + '</div>' +
    "</div>", label="idm-apply")
idm += section(head_block("Syllabus", "What the course covers", "Hands-on exercises, software training and field visits to modular factories, showrooms and interior project sites.", hid="syllabus-title") + '<div class="card-grid" style="--cols:3">' +
    card("doc", "Standards and drawings", "Interior design standards, drawings and specifications.") +
    card("layers", "Materials and hardware", "Materials and hardware selection for interior and modular works.") +
    card("laptop", "Software", "AutoCAD, SketchUp and an introduction to BIM.") +
    card("chart", "Estimation", "Quantity estimation, basic costing and modular cut lists.") +
    card("chat", "Working with clients", "Client requirements, design presentations and feedback.") +
    card("building", "Factory to site", "Factory production, showroom design and material selection, and site installation.") +
    "</div>", label="syllabus-title")
idm += section(head_block("Learning outcomes", "What you will be able to do", hid="idm-outcomes") + '<ul class="tick-list reveal">' + "".join(f"<li>{x}</li>" for x in [
    "Prepare basic AutoCAD layouts and SketchUp 3D models.",
    "Interpret specifications and select materials and hardware.",
    "Calculate quantities and prepare estimates and cut lists.",
    "Explain how drawings guide manufacturing and installation.",
    "Document client requirements, present options and respond to feedback."]) + "</ul>", cls="section tint", label="idm-outcomes")
idm += cta("Join the next IDM batch", "Tell us about your background and we'll help you choose the right format.", P_IDM, "Enquire about the course")
write("idmti.html", "Interior design course (IDM)", "Three-month Certificate Course on Interior Design & Management at IDMTI: AutoCAD, SketchUp, materials, estimation and factory-to-site installation.", idm, video=True)

# ======================= COLLEGES =======================
col = page_hero(crumbs(("For colleges", None)), "College partnerships", "What a CMTI MoU offers your college",
    "Campus-to-career support for engineering students: software and workshops, internship exposure and interview preparation.",
    chips=["Software and workshops", "Internship exposure", "Interview preparation"],
    actions=f'<a class="btn btn-primary" href="{enquire("College MoU")}">Discuss a college MoU</a>',
    extra='<dl class="hero-stats" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div><dt>Engineering college partners</dt><dd data-count="100">100+</dd></div><div><dt>Engineers placed</dt><dd data-count="5000">5,000+</dd></div><div><dt>Companies across construction, real estate, interiors and BIM</dt><dd data-count="300">300+</dd></div></dl>')
col += section(head_block("What's included", "Nine ways CMTI supports your students and faculty", hid="mou-title") + '<div class="card-grid" style="--cols:3">' +
    card("briefcase", "Placement support and campus interviews", "Employer coordination, résumé guidance, mock interviews and campus interviews.") +
    card("helmet", "Internships", "Help students find and apply for relevant industry opportunities.") +
    card("check", "Competitive exams", "Preparation guidance and practice assessments.") +
    card("laptop", "Software training", "On-campus practice with CAD, BIM, planning and estimation tools.") +
    card("book", "Free courses", "Selected technical and career-readiness courses for students.") +
    card("doc", "Curriculum development", "Boards of Studies contributions and industry input on electives, labs and projects.") +
    card("users", "Practical and faculty training", "Workshops, site visits, expert lectures and webinars.") +
    card("leaf", "Campus green audits", "Support to assess campus environmental performance and identify improvements.") +
    card("award", "NBA accreditation visits", "Industry partner inputs on internships, practical training and collaboration.") +
    "</div>", label="mou-title")
col += section(head_block("College network", "Selected partner institutions", hid="network-title") +
    '<ul class="college-logos reveal" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">' +
    "".join(f'<li><img src="college-logos/{f}.jpeg" alt="" loading="lazy"><span>{n}</span></li>' for f, n in COLLEGES) + "</ul>",
    cls="section tint", label="network-title")
col += cta("Bring CMTI to your campus", "Tell us about your college and the support your students need.", "College MoU", "Discuss a college MoU")
write("colleges.html", "For colleges", "A CMTI MoU gives engineering colleges placement support, internships, software training, curriculum input, faculty training and more.", col)

# ======================= CORPORATE =======================
P_CORP = "Corporate Training"
corp = page_hero(crumbs(("For companies", None)), "For companies", "Technical capability development for your teams",
    "Customised construction training for your teams, project needs and industry standards.",
    chips=["Pan-India delivery", "50+ practitioner trainers", "Online and hybrid options"],
    actions=f'<a class="btn btn-primary" href="{enquire(P_CORP)}">Discuss your training needs</a><a class="btn btn-ghost" href="#training-topics">Browse topics</a>',
    media='<img src="images/photos/classroom.webp" alt="Professionals attending a training session" width="900" height="600">')
corp += section(head_block("Why CMTI", "Top 5 reasons companies choose CMTI as their technical capability partner", hid="why-title") + '<div class="card-grid" style="--cols:3">' +
    card("target", "Customised programmes", "We work with Learning &amp; Development and Operations teams to align training with participant roles, project needs and industry standards.") +
    card("helmet", "Experienced industry practitioners", "Our network of 50+ trainers brings hands-on construction and real estate experience. Most are former Larsen &amp; Toubro professionals.") +
    card("pin", "Pan-India delivery", "We deliver training at project sites and corporate offices across India, with online and hybrid options.") +
    card("tag", "Affordable pricing", "We align the scope, duration and delivery format with your training priorities and budget.") +
    card("chart", "Proven track record and strong NPS", "We deliver programmes for real estate, EPC and government organisations, track participant feedback using Net Promoter Score, and assess learning against agreed objectives.") +
    f'<article class="card card-feature reveal"><h3>Plan a programme with us</h3><p>Share your project, roles and timelines, and we will propose a session plan.</p><a class="btn btn-light" href="{enquire(P_CORP)}" style="margin-top:auto;align-self:flex-start">Discuss your needs</a></article>' +
    "</div>", label="why-title")
corp += section(head_block("Our process", "How we customise each programme", hid="process-title") + '<ol class="steps reveal">' + "".join(f"<li>{s}</li>" for s in [
    "Discuss needs with L&amp;D and Operations", "Identify skill gaps and map competencies", "Refine and agree the session plan",
    "Develop tailored training content", "Deliver and assess learning"]) + "</ol>", cls="section tint", label="process-title")
corp += section(f'''<div class="split-2">
  <div class="prose reveal">
    <p class="kicker">Corporate training</p>
    <h2 id="staff-title">Capability development for staff</h2>
    <p class="lead-text">When skilled hires are hard to find, upskilling helps existing staff take on more responsibility in their current roles, while reskilling prepares them for new roles. CMTI works with L&amp;D and Operations to identify skill gaps and design training around the work participants will do.</p>
  </div>
  <div class="card-grid" style="--cols:1">
    {card("cap", "Freshers", "Diploma Engineer Trainee (DET) and Graduate Engineer Trainee (GET) programmes. We tailor the duration and topics to business needs. CMTI has delivered GET programmes for nine years, with programme details available on request.", label="Training by career stage")}
    {card("users", "Middle management", "We recommend a two-day workshop on construction topics selected with your team.", label="3–15 years of experience")}
    {card("briefcase", "Construction and project managers", "Workshops tailored to senior project responsibilities and organisational priorities.", label="15+ years of experience")}
  </div>
</div>''', label="staff-title", sid="training-participants")
topics = [("Construction Management", "Core and shell, formwork, finishes and handover protocols."),
    ("Project Management", "Project planning, project controls and software tools."),
    ("Quality Management", "Quality planning, inspections and corrective actions."),
    ("Safety Management", "Site hazard identification, risk controls and safe work practices."),
    ("MEPF", "Mechanical, electrical, plumbing and firefighting systems."),
    ("AI in Construction", "Applying artificial intelligence across construction functions."),
    ("Real Estate", "Real estate fundamentals for professionals outside the sector."),
    ("Finance", "Finance fundamentals for non-finance professionals."),
    ("Customer Relationship Management", "Customer communication, issue resolution and handover coordination."),
    ("RERA and National Building Code", "An overview of real estate regulation and building code requirements."),
    ("Green Buildings, Sustainability and ESG", "Resource efficiency, sustainable construction and ESG practices.")]
corp += section(head_block("Topics", "Explore training topics", "Select a topic to see what it covers.", hid="topics-title") +
    '<div class="accordion reveal">' + "".join(f"<details><summary>{t}</summary><p>{d}</p></details>" for t, d in topics) + "</div>" +
    f'<p style="margin-top:24px"><a class="text-link" href="{enquire(P_CORP)}">Discuss a programme for your team</a></p>',
    cls="section tint", label="topics-title", sid="training-topics")
corp += section(f'''<div class="split-2 center">
  <div class="page-hero-media reveal"><img src="images/photos/workman.webp" alt="Tradesperson in a hard hat working on site" width="900" height="601" loading="lazy"></div>
  <div class="prose reveal">
    <p class="kicker">Site crews</p>
    <h2 id="workmen-title">Capability development for workmen</h2>
    <ul class="chips amber"><li>Formwork &amp; scaffolding</li><li>Masonry</li><li>Bar bending</li><li>Plumbing</li><li>Waterproofing</li><li>Finishing works</li></ul>
    <p class="lead-text">Experienced trade trainers customise practical programmes around project requirements and the work crews perform on site.</p>
    <p>Formwork and scaffolding certification is available as part of the trade training offering.</p>
    <a class="btn btn-primary" href="{enquire("CMTI Workmen Skills")}">Enquire about workmen training</a>
  </div>
</div>''', label="workmen-title", sid="workmen")
def service(sid, ic, title, steps, text):
    return (f'<article class="card reveal" id="{sid}">{icon(ic)}<h3>{title}</h3><ol class="steps mini" style="margin:6px 0 18px">' +
            "".join(f"<li>{s}</li>" for s in steps) + f'</ol><p>{text}</p><a class="text-link" href="{enquire(P_CORP)}">Enquire with CMTI</a></article>')
corp += section(head_block("More services", "Content, assessment and hiring support", hid="services-title") + '<div class="card-grid" style="--cols:3">' +
    service("content-development", "doc", "Content development", ["Understand project workflows", "Develop SOPs and learning materials", "Review with your team"],
        "CMTI develops standard operating procedures and training content for in-house learning systems. We tailor materials to project workflows, roles and site requirements.") +
    service("assessment", "search", "Assessment of employees", ["Identify role competencies", "Assess skills and knowledge", "Report gaps and training priorities"],
        "CMTI helps L&amp;D teams assess employees periodically using suitable internationally used assessment tools. We report competency gaps and priorities for follow-up training. CMTI has delivered assessments for multiple clients.") +
    service("hiring", "handshake", "Hiring support", ["Share your hiring needs", "Connect with campuses", "Interview potential hires"],
        "CMTI has trained 5,000+ engineers through its Finishing School and works with 100+ engineering colleges. We can help employers coordinate campus hiring for entry-level engineering roles.") +
    "</div>", cls="section tint", label="services-title")
corp += section(head_block("Clients", "Companies we have trained teams for", hid="corp-clients") + LOGO_WALL, label="corp-clients", sid="client-logos")
corp += cta("Plan training for your team", "Share your project, roles and timelines, and we will propose a session plan.", P_CORP, "Discuss your training needs")
write("corporate.html", "Corporate training", "Customised construction training for staff and workmen, content development, employee assessment and hiring support across India.", corp)
