# CMTI redesign: plan

**Kind:** service (people are hired to train). `data-type="service"`, `site-kind="other"`.
**Deal:** hero `film` · nav `nav-mega` (redealt: `nav-split` is for places with four words, CMTI needs five groups) · footer `footer-visit` · close `close-photo` · rhythm `surface-pairs` · buttons `block` · mark: CMTI's own logo · moments `pinned-chapters` + `word-highlight`.
**Palette:** CMTI's own colours (brand, not dealt), because a client logo exists: white ground, cool grey surface `#f3f5f8`, navy ink `#0a1f3a`, Denim `#195b9c` for every action, Carrot Orange `#ffa434` only as one small accent per screen, WhatsApp green only on WhatsApp.
**Type:** dealt first: Nunito. Proposed: **Source Serif 4 headlines / Libre Franklin text** (the second dealt pairing). Nunito's own note says "cafes, kids and wellbeing"; L&D heads at EPC firms and ISRO are the first audience, and a sober serif reads as trusted and established. Headlines at weight 400, tight tracking, hero 72px desktop / 40px phone.

## Rules taken from the skill

- **Photographs:** real CMTI photographs only. The 8 AI images are deleted: home-banner, vision, mission, colleges-banner, associations-banner, testimonials-banner, e-learning-laptop, awards-banner.
- **Motion:**
  - The hero enters once on load. Each page gets one or two dealt moments.
  - Hover: linked cards lift 2px, photos zoom 1.02 inside their frame, buttons step on hover and press on click.
  - **Removed:** fade-ins on every card, count-up numbers, flip cards, the moving logo strips and the auto-advancing tabs.
- **Proof:** small exact objects rather than a big stat row. The hero carries one hard fact. Other figures sit inside the section they prove. Client logos appear as one still row in greyscale, coloured on hover.
- **Layout:** one section per screen, equal edges, and no captions under pictures.
- **Lenis:** loaded from a pinned version in `/vendor/`. Gentle smoothing on the mouse wheel, native touch scrolling, and fully off under reduced motion. Anchor links and Back to top go through `lenis.scrollTo` with an offset for the header; Skip to content still moves focus. `data-lenis-prevent` on the menu sheet and the video pop-up, and Lenis stops while a pop-up is open.

## Home, section by section (desktop screens)

| # | Section | One idea | Picture | Screens |
|---|---|---|---|---|
| 0 | Announcement strip | ISDA Infracon 2025 Best Skill Development Award → /awards (TODO: swap for the next CACM batch date) | none | n/a |
| 1 | Nav (mega) | Solutions · Programmes · Colleges · Learn · About; right side: "E-learning login" link + **Send an enquiry** | one photo card in the Programmes panel | n/a |
| 2 | Hero (film) | h1 "Site-ready training for construction teams"; lead with the hard fact "5,000+ engineers placed since 2018"; buttons **Train your team** / **Find a course**; "4.7 ★ from 2,362 Google reviews" | `rebar-inspection` as the film poster; play opens the CACM film (YouTube jxEoc8QkPOo) in the frame | 1 |
| 3 | Who we train | Organisations · engineering colleges · working professionals, one line and one link each | `corporate-staff-training` | 1 |
| 4 | **pinned-chapters**: how CMTI trains | 4 steps beside one frame: staff programmes → workmen skilling → certified courses (CACM, IDM) → e-learning | `corporate-staff-group`, `workmen-bar-bending`, `site-visit-group`, then a live HTML course card from `elearn_courses.json` (CMTI's own platform) | 2 |
| 5 | **word-highlight** statement | "Our 50+ trainers come from the site, most of them from L&T, and teach with real project examples." | type only (this is the statement moment) | 1 |
| 6 | Recognition (surface band) | ISDA award and Towell (Manchester, Nama Water) + one still row of 8 client logos | `isda-infracon-2025-award`, `towell-manchester-appreciation` | 1 |
| 7 | Hear from participants (surface band) | the 2 video testimonials side by side (DLF Gurugram, Bluewing) | the video frames (faces) | 1 |
| 8 | Colleges | 100+ partner colleges in 3 states, 300+ hiring companies; "Discuss a College MoU" | `street-group` | 1 |
| 9 | Keep learning | 76 self-paced courses (18 free) + free webinars on Saturdays at 7 PM IST | `showroom-visit` | 1 |
| 10 | Enquiry form | the WhatsApp form restyled, beside the address | none (form) | 1 |
| 11 | Close + footer (close-photo, footer-visit) | "Send an enquiry" beside a photo; the address set large; link columns; phones, email, GSTIN, CIN, Privacy | one photo not used above, or reuse rule: TODO pick at build | 1 |

## Other pages (after you approve Home)

- **For Corporates:** hero; solutions by need; the 5-step process as a horizontal timeline; career stages; 12 topics as an open grid with icons (flip cards removed); workmen trades; Content Development / Assessment / Hiring Support; client row; close.
- **CACM and IDM:** a key-facts strip (3 months · offline, online, hybrid · eligibility · next batch TODO); outcomes; syllabus accordion; video; FAQ built only from existing facts; a sticky Enquire / WhatsApp bar on phones.
- **About:** story, mentor, leadership, trainers. Each person listed once; initials monograms where there's no photo.
- **E-learning:** filters by topic and Free/Paid over the JSON.
- **The rest:** Colleges, Awards, Associations, Testimonials and Privacy get the new system. Real photos replace every AI banner.
- **URLs:** every URL keeps working, including the finishing-school redirect.

## Defaults I'm assuming (say if any are wrong)

1. **Course count:** "76 courses (18 free)", not "80+", because the data proves 76.
2. **Engineers:** "5,000+ engineers placed" everywhere (it's the main claim, used three times). The Corporate wording "trained" is changed to match. **TODO(CMTI):** confirm.
3. **Internships, Software and BIM:** one "Other programmes" group in the Programmes menu, each opening an enquiry with that programme preselected.
4. **Vision & Mission:** moved into About, and `/vision-mission` redirects there.
5. **E-learning:** a Free/Paid filter only, no prices shown.

## Where your brief and the skill still differ (my call; I'll change it on your word)

- **Architecture:** the skill loads its kit files unedited from `/assets/` (system, layout, motion and card CSS and JS), and its checker fails edited kit files. So the site becomes the kit files + one `site.css` + one `site.js` + Lenis, not strictly one CSS and one JS file. Still static, still the Python generator, no build step.
- **Hero layout:** the dealt hero puts the words in a navy box at the lower left of the photo frame, not centred.
- **Hero buttons:** split by audience (Train your team / Find a course), while the nav and close say **Send an enquiry**. The skill prefers one action repeated word for word everywhere.
- **No gradient band.** The deal gave flat grounds with one grey surface band.
- **Testimonials:** shown side by side, not as a carousel.
- **Contact details:** the skill's checker objects to full addresses, phone numbers, GSTIN and CIN, and allows only 5 waivers. To stay within that, the full set appears once in the footer and once in the enquiry block, and the waivers are logged.

## TODO(CMTI) placeholders

- Next CACM and IDM batch dates.
- Corporate brochure PDF.
- Photos of the leadership team and trainers.
- Which trainers are ex-L&T (for the badge).
- Case-study outcomes.
- The canonical domain and a share image.
- A photo for the closing section that isn't used higher up the page (CMTI has 9 real photos).
