# -*- coding: utf-8 -*-
"""
Builds the "Publications & Academic Works" section of drnidhi.great-site.net
from publications/catalog.py.

Outputs
  publications/index.html            landing page + search/filter
  publications/<slug>.html           one page per work
  publications/library.json          machine-readable catalog
  publications/print/<slug>.html     print templates (PDF source)
  publications/files/                the original documents + generated PDFs
"""
import os, re, json, shutil, html, subprocess, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from catalog import WORKS, AUTHOR

ROOT = r"C:\Users\nidhi\harshal\DrNidhi_portfolio"
NEW = os.path.join(ROOT, "newdata")
PUB = os.path.join(ROOT, "publications")
FILES = os.path.join(PUB, "files")
PRINT = os.path.join(PUB, "print")
SITE = "https://drnidhi.great-site.net"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TODAY = datetime.date.today().isoformat()

for d in (PUB, FILES, PRINT):
    os.makedirs(d, exist_ok=True)


def esc(s):
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    return html.escape(s, quote=True)


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def clean_inline(s):
    """Plain text safe for embedding in a single HTML line."""
    s = re.sub(r"\s+", " ", s or "").strip()
    return s


# ---------------------------------------------------------------- citations
def cite_apa(w):
    authors = [AUTHOR["name"]] + list(w.get("coauthors", []))
    auth = ", ".join(authors)
    year = w.get("year", "n.d.")
    if w["type"] == "Thesis":
        return (f"{auth} ({year}). {w['title']} [Unpublished master\u2019s dissertation]. "
                f"{w.get('venue', '')}. {w.get('institution', '')}.")
    if w["type"] == "Article":
        return (f"{auth} ({year}). {w['title']}. {w.get('venue', '')}.")
    if w["type"] == "Abstract":
        return (f"{auth} ({year}). {w['title']} [Conference abstract]. {w.get('venue', '')}.")
    return (f"{auth} ({year}). {w['title']} [Seminar presentation]. {w.get('venue', '')}.")


def cite_vancouver(w):
    authors = [AUTHOR["name"]] + list(w.get("coauthors", []))
    numbered = "; ".join(f"{i+1}. {a}" for i, a in enumerate(authors))
    year = w.get("year", "n.d.")
    if w["type"] == "Thesis":
        return f"{numbered}. {w['title']} [dissertation]. {w.get('venue','')}; {year}."
    if w["type"] == "Article":
        return f"{numbered}. {w['title']}. {w.get('venue','')}; {year}."
    if w["type"] == "Abstract":
        return f"{numbered}. {w['title']} [abstract]. {w.get('venue','')}; {year}."
    return f"{numbered}. {w['title']} [seminar presentation]; {year}; {w.get('venue','')}."


def cite_bibtex(w):
    key = slugify(w["title"])[:40]
    auth = " and ".join([AUTHOR["name"]] + list(w.get("coauthors", [])))
    if w["type"] == "Thesis":
        etype, school = "phdthesis", w.get("venue", "")
    elif w["type"] == "Article":
        etype, school = "article", w.get("venue", "")
    else:
        etype, school = "misc", w.get("venue", "")
    kw = ", ".join(w.get("keywords", [])[:5])
    return (f"@{etype}{{{key},\n  author = {{{auth}}},\n  title = {{{w['title']}}},\n"
            f"  year = {{{w.get('year','')}}},\n  school = {{{school}}},\n"
            f"  keywords = {{{kw}}}\n}}")


# ---------------------------------------------------------------- json-ld
def scholarly_jsonld(w):
    url = f"{SITE}/publications/{w['slug']}.html"
    authors = [{"@type": "Person", "name": AUTHOR["name"],
                "affiliation": {"@type": "Organization", "name": AUTHOR["affiliation"]}}]
    for c in w.get("coauthors", []):
        authors.append({"@type": "Person", "name": c})
    data = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "@id": url + "#article",
        "headline": w["title"],
        "name": w["title"],
        "description": clean_inline(w["abstract"])[:300],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": str(w.get("year", "")),
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "author": authors,
        "keywords": ", ".join(w.get("keywords", [])),
        "articleSection": w.get("type_label", w["type"]),
        "genre": w.get("type", ""),
        "publisher": {"@type": "Organization", "name": "Dr. Nidhi Patel"},
        "about": [{"@type": "MedicalEntity", "name": k} for k in w.get("keywords", [])[:5]],
    }
    if w.get("venue"):
        data["publisher"] = {"@type": "Organization", "name": w["venue"]}
        data["isPartOf"] = {"@type": "PublicationIssue", "name": w["venue"]}
    if w.get("guide"):
        data["editor"] = {"@type": "Person", "name": w["guide"]}
    if w.get("reg_no"):
        data["identifier"] = w["reg_no"]
    if w.get("degree"):
        data["educationalLevel"] = w["degree"]
    if w.get("institution"):
        data["publisher"] = {"@type": "Organization", "name": w["institution"]}
    # citation_* fields — the classic Google Scholar / Scholar-compatible markup
    data["citation_title"] = w["title"]
    data["citation_author"] = [AUTHOR["name"]] + list(w.get("coauthors", []))
    data["citation_publication_date"] = str(w.get("year", ""))
    if w.get("venue"):
        data["citation_journal_title"] = w["venue"]
        data["citation_conference_title"] = w["venue"]
    data["citation_pdf_url"] = f"{SITE}/publications/files/{w['slug']}.pdf"
    data["citation_abstract"] = clean_inline(w["abstract"])
    data["citation_keywords"] = "; ".join(w.get("keywords", []))
    return json.dumps(data, indent=2, ensure_ascii=False)


def breadcrumb_jsonld(w):
    url = f"{SITE}/publications/{w['slug']}.html"
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Publications", "item": SITE + "/publications/"},
            {"@type": "ListItem", "position": 3, "name": w["title"], "item": url},
        ]
    }, indent=2, ensure_ascii=False)


def collection_jsonld():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Publications & Academic Works — Dr. Nidhi Patel (M.S.) Ayurveda",
        "url": SITE + "/publications/",
        "description": "Peer-reviewed articles, conference abstracts, seminar presentations and the M.S. (Ayurveda) dissertation of Dr. Nidhi Sanjay Patel in Prasuti Tantra & Stree Roga.",
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": "Dr. Nidhi Patel (M.S.) — Ayurvedic Women's Wellness",
                     "url": SITE + "/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(WORKS),
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/publications/{w['slug']}.html",
                 "name": w["title"]}
                for i, w in enumerate(sorted(WORKS, key=lambda x: (x.get("year", 0), x["title"]), reverse=True))
            ]
        }
    }, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------- shared html
HEAD_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Dr. Nidhi Sanjay Patel">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="Dr. Nidhi Patel (M.S.) Ayurveda">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/dr-nidhi-patel-profile.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/dr-nidhi-patel-profile.jpg">
<link rel="icon" type="image/png" href="{SITE}/1.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Sacramento&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{jsonld}
</head>
<body>
<nav class="pub-nav">
  <div class="wrap">
    <a class="pub-brand" href="{SITE}/">Dr. Nidhi <span>Patel</span></a>
    <ul>
      <li><a href="{SITE}/">Home</a></li>
      <li><a href="{SITE}/#about">About</a></li>
      <li><a href="{SITE}/#services">Services</a></li>
      <li><a href="{SITE}/#professional-journey">Journey</a></li>
      <li><a href="{SITE}/publications/" aria-current="page">Publications</a></li>
      <li><a href="{SITE}/#contact">Contact</a></li>
    </ul>
  </div>
</nav>
"""

FOOT_TPL = """
<footer class="pub-footer">
  <div class="wrap footer-grid">
    <div>
      <p><strong>Dr. Nidhi Sanjay Patel</strong> — B.A.M.S., M.S. (Ayurveda), Prasuti Tantra &amp; Stree Roga.<br>
      Assistant Professor, Department of Prasuti Tantra &amp; Stree Roga, Uka Tarsadia University, Bardoli, Gujarat.</p>
      <p><a href="mailto:{email}">{email}</a> &middot; <a href="tel:{phone}">{phone}</a></p>
    </div>
    <div>
      <p><a href="{SITE}/publications/">All publications</a> &middot; <a href="{SITE}/publications/library.json">Catalog JSON</a> &middot; <a href="{SITE}/rss.xml">RSS feed</a></p>
      <p>All works on this page are published by the author for open access and are free to read and share.<br>
      &copy; {year} Dr. Nidhi Patel. Content licensed CC BY 4.0 unless otherwise noted.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def page_head(title, desc, canonical, ogtype="article", css="assets/pub.css", jsonld=""):
    blocks = jsonld if isinstance(jsonld, (list, tuple)) else ([jsonld] if jsonld else [])
    jl = "".join(f'\n    <script type="application/ld+json">\n{b}\n    </script>' for b in blocks)
    return HEAD_TPL.format(title=esc(title), desc=esc(desc), canonical=canonical,
                           ogtype=ogtype, ogtitle=esc(title), css=css, jsonld=jl, SITE=SITE)


# ---------------------------------------------------------------- related works
def related_for(w, limit=4):
    kw = set(k.lower() for k in w.get("keywords", []))
    scored = []
    for o in WORKS:
        if o["slug"] == w["slug"]:
            continue
        ok = set(k.lower() for k in o.get("keywords", []))
        score = len(kw & ok)
        if score:
            scored.append((score, o))
    scored.sort(key=lambda x: (-x[0], x[1]["title"]))
    return [o for _, o in scored[:limit]]


# ---------------------------------------------------------------- work page
def render_work_page(w):
    url = f"{SITE}/publications/{w['slug']}.html"
    desc = clean_inline(w["abstract"])[:300]
    keywords = "".join(f'<a href="{SITE}/publications/?q={k.replace(" ", "+")}">{esc(k)}</a>' for k in w.get("keywords", []))
    coauthor_rows = ""
    if w.get("coauthors"):
        coauthor_rows = f"<tr><th>Co-author(s)</th><td>{esc('; '.join(w['coauthors']))}</td></tr>"
    guide_row = f"<tr><th>Guide / Supervisor</th><td>{esc(w['guide'])}</td></tr>" if w.get("guide") else ""
    deg_row = f"<tr><th>Degree</th><td>{esc(w['degree'])}</td></tr>" if w.get("degree") else ""
    inst_row = f"<tr><th>Institution</th><td>{esc(w['institution'])}</td></tr>" if w.get("institution") else ""
    reg_row = f"<tr><th>Registration no.</th><td>{esc(w['reg_no'])}</td></tr>" if w.get("reg_no") else ""

    rel = related_for(w)
    rel_html = ""
    if rel:
        items = "".join(
            f'<li><a href="{SITE}/publications/{r["slug"]}.html">{esc(r["title"])}</a> '
            f'<span style="color:var(--text-soft)"> — {esc(r.get("type_label", r["type"]))}, {r.get("year","")}</span></li>'
            for r in rel)
        rel_html = f'<section class="related"><h2>Related reading</h2><ul class="related-list">{items}</ul></section>'

    body = f"""
<main class="pub-article">
  <div class="wrap narrow">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="{SITE}/">Home</a><span>/</span>
      <a href="{SITE}/publications/">Publications</a><span>/</span>
      <span>{esc(w.get('type_label', w['type']))}</span>
    </nav>

    <article>
      <header class="work-head">
        <span class="work-type">{esc(w.get('type_label', w['type']))}</span>
        <h1>{esc(w['title'])}</h1>
        {f'<p class="work-sub">{esc(w["subtitle"])}</p>' if w.get("subtitle") else ''}
        <p class="hook-line">{esc(w['hook'])}</p>
      </header>

      <div class="action-row">
        <a class="btn primary" href="files/{w['slug']}.pdf" download>Download the full text (PDF)</a>
        <a class="btn" href="files/{w['slug']}-source.{esc(w['source_ext'])}" download>Original file ({esc(w['source_ext'].upper())})</a>
        <a class="btn ghost" href="#cite">Cite this work</a>
      </div>

      <table class="meta-table">
        <tbody>
          <tr><th>Author</th><td>{esc(AUTHOR['name'])}, {esc(AUTHOR['degrees'])}</td></tr>
          {coauthor_rows}
          {guide_row}
          {deg_row}
          {inst_row}
          <tr><th>Year</th><td>{esc(w.get('year',''))}</td></tr>
          {f'<tr><th>Venue</th><td>{esc(w["venue"])}</td></tr>' if w.get('venue') else ''}
          {reg_row}
        </tbody>
      </table>

      <section class="abstract-box">
        <h2>Abstract</h2>
        <p>{esc(w['abstract'])}</p>
        <div class="keyword-row">{keywords}</div>
      </section>

      <div class="note">
        <strong>How to read this.</strong> This work is published here in full and free for clinicians, postgraduate
        students, researchers and patients. If it is useful to you, please cite it using the format below — every
        citation strengthens the reach of this research. Questions about the work can be sent directly to
        <a href="mailto:{AUTHOR['email']}">{AUTHOR['email']}</a>.
      </div>

      <section class="cite-box" id="cite">
        <h2>Cite this work</h2>
        <div class="cite-label">APA 7th</div>
        <p class="cite-text">{esc(cite_apa(w))}</p>
        <div class="cite-label">Vancouver</div>
        <p class="cite-text">{esc(cite_vancouver(w))}</p>
        <div class="cite-label">BibTeX</div>
        <p class="cite-text">{esc(cite_bibtex(w))}</p>
      </section>

      {rel_html}
    </article>
  </div>
</main>
"""
    foot = FOOT_TPL.format(SITE=SITE, email=AUTHOR["email"], phone=AUTHOR["phone"], year=TODAY[:4])
    head = page_head(
        f"{w['title']} — {w.get('type_label', w['type'])} | Dr. Nidhi Patel (M.S.) Ayurveda",
        desc, url, ogtype="article", css="assets/pub.css",
        jsonld=[scholarly_jsonld(w), breadcrumb_jsonld(w)])
    return head + body + foot


# ---------------------------------------------------------------- print page
def render_print_page(w, body_html="", full_text=False):
    """Clean, print-optimised sheet. With body_html the full source text follows the cover."""
    kw = "".join(f'<span class="kw">{esc(k)}</span>' for k in w.get("keywords", []))
    authors = esc(AUTHOR["name"]) + "".join(f"<br><span class='co'>{esc(c)}</span>" for c in w.get("coauthors", []))
    details = []
    if w.get("guide"):
        details.append(f"<div><b>Guide / Supervisor</b><br>{esc(w['guide'])}</div>")
    if w.get("degree"):
        details.append(f"<div><b>Degree</b><br>{esc(w['degree'])}</div>")
    if w.get("institution"):
        details.append(f"<div><b>Institution</b><br>{esc(w['institution'])}</div>")
    if w.get("venue"):
        details.append(f"<div><b>Venue</b><br>{esc(w['venue'])}</div>")
    details.append(f"<div><b>Year</b><br>{esc(w.get('year',''))}</div>")
    if w.get("reg_no"):
        details.append(f"<div><b>Registration no.</b><br>{esc(w['reg_no'])}</div>")

    body_block = ""
    if full_text and body_html:
        body_block = f"""
<div class="pagebreak"></div>
<h2 class="fulltext-h">Full text</h2>
<p class="fulltext-note">Reproduced below is the complete text of the source document as submitted, reformatted
for reading on the web and in print. The original file is also available alongside this PDF.</p>
<div class="fulltext">{body_html}</div>"""

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>{esc(w['title'])}</title>
<style>
  @page {{ size: A4; margin: 20mm 18mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Georgia, 'Times New Roman', serif; color:#2b1d30; line-height:1.62; margin:0; font-size:11.2pt; }}
  .rule-top {{ height:5px; background:linear-gradient(90deg,#C5A880,#D9C2D3,#D2DBCE); margin-bottom:22px; }}
  .kicker {{ font-family:'Poppins',Arial,sans-serif; font-size:8pt; letter-spacing:.2em; text-transform:uppercase; color:#8E5572; font-weight:600; }}
  h1 {{ font-size:20pt; line-height:1.22; margin:8px 0 6px; font-weight:700; }}
  .sub {{ font-size:11pt; color:#6B5470; font-style:italic; margin:0 0 14px; }}
  .authors {{ border-top:1px solid #e2d7c9; border-bottom:1px solid #e2d7c9; padding:12px 0; margin:16px 0 6px; font-size:10.4pt; }}
  .authors .co {{ color:#6B5470; font-size:9.6pt; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:6px 28px; font-size:9.4pt; margin:14px 0 22px; color:#4a3550; }}
  .hook {{ font-size:11.6pt; font-style:italic; color:#8E5572; border-left:3px solid #C5A880; padding:6px 0 6px 14px; margin:18px 0 22px; }}
  h2 {{ font-size:12.4pt; margin:24px 0 8px; padding-bottom:5px; border-bottom:1px solid #e2d7c9; }}
  .abstract {{ background:#FAF6F0; border:1px solid #eee2d3; padding:16px 18px; }}
  .kwrow {{ margin-top:14px; }}
  .kw {{ display:inline-block; font-family:'Poppins',Arial,sans-serif; font-size:8pt; border:1px solid #d9c9b4;
         border-radius:999px; padding:3px 10px; margin:0 5px 5px 0; color:#6B5470; }}
  .cite {{ font-size:9.4pt; background:#fff; border:1px solid #eee2d3; padding:10px 14px; margin:8px 0; }}
  .citelbl {{ font-family:'Poppins',Arial,sans-serif; font-size:7.4pt; letter-spacing:.16em; text-transform:uppercase; color:#8E5572; font-weight:600; }}
  .foot {{ margin-top:30px; padding-top:12px; border-top:1px solid #e2d7c9; font-size:8.6pt; color:#6B5470;
           font-family:'Poppins',Arial,sans-serif; }}
  .foot a {{ color:#8E5572; }}
  .pagebreak {{ page-break-before: always; break-before: page; }}
  .fulltext-h {{ border-bottom:2px solid #C5A880; }}
  .fulltext-note {{ font-size:9.4pt; color:#6B5470; font-style:italic; margin-bottom:16px; }}
  .fulltext p {{ margin:0 0 9px; text-align:justify; hyphens:auto; }}
  .fulltext h2 {{ font-size:12pt; margin:20px 0 7px; border-bottom:none; color:#6d3f57; }}
  .fulltext h2.slide-title {{ color:#6d3f57; }}
</style></head><body>
<div class="rule-top"></div>
<div class="kicker">{esc(w.get('type_label', w['type']))}</div>
<h1>{esc(w['title'])}</h1>
{f'<p class="sub">{esc(w["subtitle"])}</p>' if w.get('subtitle') else ''}
<div class="authors">{authors}</div>
<div class="meta">{''.join(details)}</div>
<div class="hook">{esc(w['hook'])}</div>
<h2>Abstract</h2>
<div class="abstract"><p>{esc(w['abstract'])}</p>
<div class="kwrow">{kw}</div></div>
<h2>Cite this work</h2>
<div class="citelbl">APA 7th</div><div class="cite">{esc(cite_apa(w))}</div>
<div class="citelbl">Vancouver</div><div class="cite">{esc(cite_vancouver(w))}</div>
{body_block}
<div class="foot">
  Open-access copy published by the author at {SITE}/publications/{w['slug']}.html<br>
  Dr. Nidhi Sanjay Patel — {AUTHOR['email']} &middot; Licensed CC BY 4.0
</div>
</body></html>
"""


# ---------------------------------------------------------------- index page
def person_jsonld():
    """Person + profile + publication list for the root page."""
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": SITE + "/#person",
        "name": AUTHOR["name"],
        "alternateName": ["Dr. Nidhi Patel", "Nidhi Sanjay Patel", "N. Patel"],
        "honorificPrefix": "Dr.",
        "jobTitle": "Assistant Professor, Department of Prasuti Tantra & Stree Roga",
        "description": ("Ayurvedic physician and Assistant Professor specialising in Prasuti Tantra & Stree Roga "
                        "(Ayurvedic obstetrics and gynaecology). Clinical researcher in Uttarbasti, fertility, "
                        "Panchakarma and preventive women's health."),
        "url": SITE + "/",
        "image": SITE + "/dr-nidhi-patel-profile.jpg",
        "email": "mailto:" + AUTHOR["email"],
        "telephone": AUTHOR["phone"],
        "medicalSpecialty": "Ayurvedic Medicine",
        "knowsAbout": ["Ayurvedic Gynecology", "Prasuti Tantra", "Stree Roga", "PCOS (PCOD)",
                       "Ayurvedic Fertility Treatment", "Uttar Basti", "Panchakarma",
                       "Antenatal Care (Garbhini Paricharya)", "Menstrual Disorders"],
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Dr. N.R.S. Govt. Ayurvedic College, Vijayawada"},
            {"@type": "CollegeOrUniversity", "name": "Dr. N.T.R. University of Health Sciences, Vijayawada"},
            {"@type": "CollegeOrUniversity", "name": "Parul University, Vadodara"},
        ],
        "affiliation": {"@type": "CollegeOrUniversity", "name": "Uka Tarsadia University (UTU), Bardoli"},
        "worksFor": {"@type": "CollegeOrUniversity", "name": "Uka Tarsadia University (UTU), Bardoli"},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "M.S. (Ayurveda) — Prasuti Tantra & Stree Roga",
             "credentialCategory": "degree", "educationalLevel": "Postgraduate",
             "alumniOf": {"@type": "CollegeOrUniversity", "name": "Dr. N.T.R. University of Health Sciences, Vijayawada"}},
            {"@type": "EducationalOccupationalCredential", "name": "B.A.M.S. — Bachelor of Ayurvedic Medicine & Surgery",
             "credentialCategory": "degree", "educationalLevel": "Undergraduate",
             "alumniOf": {"@type": "CollegeOrUniversity", "name": "Parul University, Vadodara"}},
        ],
        "hasPublished": [
            {"@type": "ScholarlyArticle", "name": w["title"], "datePublished": str(w.get("year", "")),
             "url": f"{SITE}/publications/{w['slug']}.html"} for w in WORKS
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_publications_section():
    """The 'Publications' block injected into the root page."""
    featured = sorted([w for w in WORKS if w.get("featured")], key=lambda x: -x.get("year", 0))
    cards = []
    for w in featured:
        cards.append(f"""
                    <div class="pub-card">
                        <span class="pub-badge">{esc(w.get('type_label', w['type']))}</span>
                        <h3><a href="publications/{w['slug']}.html">{esc(w['title'])}</a></h3>
                        <p>{esc(w['hook'])}</p>
                        <div class="pub-card-meta">
                            <span>{esc(w.get('year',''))}</span>
                            {f'<span>&middot; {esc(w.get("venue",""))}</span>' if w.get('venue') else ''}
                        </div>
                        <a class="pub-link" href="publications/{w['slug']}.html">Read &amp; download &rarr;</a>
                    </div>""")

    counts = {
        "works": len(WORKS),
        "articles": sum(1 for w in WORKS if w["type"] == "Article"),
        "abstracts": sum(1 for w in WORKS if w["type"] == "Abstract"),
        "seminars": sum(1 for w in WORKS if w["type"] == "Seminar"),
    }

    return f"""
        <section id="publications" class="container">
            <div class="section-card">
                <h2 class="gradient-text-animated">Publications &amp; Academic Works</h2>
                <div class="section-divider"></div>
                <p>The research behind the practice. Every abstract, article, seminar and the full M.S. (Ayurveda)
                dissertation are published open access on this site — free to read, free to download, and supplied
                with ready-made citations so that the work can be read, cited and built upon.</p>

                <div class="pub-stats">
                    <div class="pub-stat"><b>{counts['works']}</b><span>Works published</span></div>
                    <div class="pub-stat"><b>{counts['articles']}</b><span>Journal articles</span></div>
                    <div class="pub-stat"><b>{counts['abstracts']}</b><span>Conference abstracts</span></div>
                    <div class="pub-stat"><b>{counts['seminars']}</b><span>Seminar presentations</span></div>
                </div>

                <div class="pub-grid">{''.join(cards)}</div>

                <div class="pub-cta-row">
                    <a href="publications/" class="cta-button">Browse the full publication library</a>
                    <a href="publications/library.json" class="pub-text-link">Machine-readable catalogue (JSON)</a>
                </div>
            </div>
        </section>
"""


def patch_index():
    """Idempotently inject the publications markup + JSON-LD into the root index.html."""
    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        html_src = f.read()
    original = html_src

    # 1. Person JSON-LD block (inserted before the closing </head>)
    if "PUBLICATIONS_JSONLD_START" not in html_src:
        block = ("\n    <!-- PUBLICATIONS_JSONLD_START -->\n    <script type=\"application/ld+json\">\n"
                 + person_jsonld() + "\n    </script>\n    <!-- PUBLICATIONS_JSONLD_END -->\n")
        html_src = html_src.replace("</head>", block + "</head>", 1)

    # 2. Publications section
    if "PUBLICATIONS_SECTION_START" in html_src:
        html_src = re.sub(
            r"(<!-- PUBLICATIONS_SECTION_START -->).*?(<!-- PUBLICATIONS_SECTION_END -->)",
            lambda m: m.group(1) + render_publications_section().rstrip() + "\n        " + m.group(2),
            html_src, flags=re.S)
    else:
        html_src = html_src.replace(
            "        <section id=\"testimonials\"",
            render_publications_section() + "\n        <section id=\"testimonials\"", 1)

    if html_src != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_src)
        return True
    return False


def render_index():
    ordered = sorted(WORKS, key=lambda x: (x.get("year", 0), x["slug"]), reverse=True)
    types = []
    for w in ordered:
        if w["type"] not in types:
            types.append(w["type"])

    cards = []
    for w in ordered:
        search = " ".join([w["title"], w.get("subtitle", ""), w.get("type_label", ""),
                           w.get("venue", ""), " ".join(w.get("keywords", [])), w.get("hook", "")])
        chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in
                         [w.get("type_label", w["type"]), str(w.get("year", ""))])
        cards.append(f"""
        <article class="work-card" data-work-card data-type="{esc(w['type'])}" data-search="{esc(search)}">
          <span class="work-type">{esc(w.get('type_label', w['type']))}</span>
          <h3><a href="{w['slug']}.html">{esc(w['title'])}</a></h3>
          <p>{esc(w['hook'])}</p>
          <div class="work-meta">{chips}</div>
          <a class="work-cta" href="{w['slug']}.html">Read &amp; download &rarr;</a>
        </article>""")

    filters = ['<button class="filter-btn active" data-filter="all" aria-pressed="true">All works</button>']
    for t in types:
        n = sum(1 for w in WORKS if w["type"] == t)
        label = {"Thesis": "Thesis", "Article": "Articles", "Abstract": "Abstracts",
                 "Seminar": "Seminar talks"}.get(t, t)
        filters.append(f'<button class="filter-btn" data-filter="{esc(t)}" aria-pressed="false">{esc(label)} ({n})</button>')

    featured = [w for w in ordered if w.get("featured")]
    feat_html = ""
    if featured:
        items = "".join(
            f'<li><a href="{w["slug"]}.html">{esc(w["title"])}</a> '
            f'<span style="color:var(--text-soft)"> — {esc(w.get("type_label",""))}, {w.get("year","")}</span></li>'
            for w in featured)
        feat_html = f"""
        <section class="pub-section">
          <div class="section-label">Featured</div>
          <h2 class="pub-h2">Start here</h2>
          <div class="rule"></div>
          <ul class="related-list">{items}</ul>
        </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Publications &amp; Academic Works | Dr. Nidhi Patel (M.S.) Ayurveda</title>
<meta name="description" content="The complete published record of Dr. Nidhi Sanjay Patel (M.S. Ayurveda, Prasuti Tantra &amp; Stree Roga) — an M.S. dissertation on Uttar Basti in Artava Kshaya, a peer-reviewed article on Pumsavana Karma, conference abstracts and seminar presentations, all open access.">
<meta name="author" content="Dr. Nidhi Sanjay Patel">
<meta name="keywords" content="Dr Nidhi Patel, Ayurveda, Prasuti Tantra, Stree Roga, Uttarbasti, Artava Kshaya, Hypomenorrhoea, Pumsavana, Panchakarma, Vandyatwa, Preconceptional care, fertility, women's health, research publications, open access">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{SITE}/publications/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dr. Nidhi Patel (M.S.) Ayurveda">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="Publications &amp; Academic Works | Dr. Nidhi Patel (M.S.) Ayurveda">
<meta property="og:description" content="Dissertation, peer-reviewed article, conference abstracts and seminar presentations in Ayurvedic women's health — all open access.">
<meta property="og:url" content="{SITE}/publications/">
<meta property="og:image" content="{SITE}/dr-nidhi-patel-profile.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Publications &amp; Academic Works | Dr. Nidhi Patel">
<meta name="twitter:description" content="Dissertation, peer-reviewed article, conference abstracts and seminar presentations in Ayurvedic women's health — all open access.">
<meta name="twitter:image" content="{SITE}/dr-nidhi-patel-profile.jpg">
<link rel="icon" type="image/png" href="{SITE}/1.png">
<link rel="alternate" type="application/rss+xml" title="Dr. Nidhi Patel — Publications" href="{SITE}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Sacramento&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/pub.css">
<script type="application/ld+json">
{collection_jsonld()}
</script>
</head>
<body>
<nav class="pub-nav">
  <div class="wrap">
    <a class="pub-brand" href="{SITE}/">Dr. Nidhi <span>Patel</span></a>
    <ul>
      <li><a href="{SITE}/">Home</a></li>
      <li><a href="{SITE}/#about">About</a></li>
      <li><a href="{SITE}/#services">Services</a></li>
      <li><a href="{SITE}/#professional-journey">Journey</a></li>
      <li><a href="{SITE}/publications/" aria-current="page">Publications</a></li>
      <li><a href="{SITE}/#contact">Contact</a></li>
    </ul>
  </div>
</nav>

<header class="pub-hero">
  <div class="wrap">
    <span class="eyebrow">Open Access &middot; Free to read &amp; share</span>
    <h1 class="pub-title">Publications &amp;<br><span class="accent">Academic Works</span></h1>
    <p class="pub-lede">The complete published record of <strong>Dr. Nidhi Sanjay Patel</strong> — M.S. (Ayurveda)
    in Prasuti Tantra &amp; Stree Roga. A clinical dissertation on Uttar Basti for scanty menstruation, a
    peer-reviewed article on Pumsavana Karma, conference abstracts and seminar presentations — every one of them
    readable in full, free to download, and ready to cite.</p>
    <div class="pub-stats">
      <div class="pub-stat"><b>{len(WORKS)}</b><span>Works</span></div>
      <div class="pub-stat"><b>{sum(1 for w in WORKS if w['type']=='Seminar')}</b><span>Seminar talks</span></div>
      <div class="pub-stat"><b>{sum(1 for w in WORKS if w['type']=='Abstract')}</b><span>Conference abstracts</span></div>
      <div class="pub-stat"><b>{sum(1 for w in WORKS if w['type']=='Article')}</b><span>Articles</span></div>
      <div class="pub-stat"><b>1</b><span>M.S. dissertation</span></div>
    </div>
  </div>
</header>

<main class="wrap">
  {feat_html}
  <section class="pub-section">
    <div class="section-label">Full catalogue</div>
    <h2 class="pub-h2">Every work, searchable</h2>
    <div class="rule"></div>
    <div class="filter-bar">
      <input type="search" id="pubSearch" placeholder="Search titles, topics, keywords&hellip;" aria-label="Search publications">
      {''.join(filters)}
      <span class="filter-count" id="pubCount"></span>
    </div>
    <div class="work-grid">
      {''.join(cards)}
    </div>
    <p id="pubEmpty" style="display:none;color:var(--text-soft)">No works match that search. Try a broader term such as
    &ldquo;Ayurveda&rdquo;, &ldquo;fertility&rdquo;, &ldquo;labour&rdquo; or &ldquo;Prasuti Tantra&rdquo;.</p>
  </section>

  <section class="pub-section">
    <div class="section-label">For researchers &amp; clinicians</div>
    <h2 class="pub-h2">Reuse, cite, and build on this work</h2>
    <div class="rule"></div>
    <p style="color:var(--text-soft); max-width:820px">Every page on this site carries a formatted citation in APA 7th,
    Vancouver and BibTeX, together with <code>ScholarlyArticle</code> structured data so that scholarly indexes,
    reference managers and citation trackers can pick the work up automatically. The whole catalogue is also
    available as a machine-readable file at
    <a href="library.json">publications/library.json</a> and as an
    <a href="{SITE}/rss.xml">RSS feed</a> of new work.</p>
    <p style="color:var(--text-soft); max-width:820px">If you are a postgraduate student or researcher working in
    Prasuti Tantra, Stree Roga, fertility, or Ayurvedic management of women's disorders, these papers are a
    starting point rather than an end point — please build on them, and consider the
    <a href="{SITE}/#contact">clinical practice</a> that sits behind them.</p>
  </section>
</main>
{FOOT_TPL.format(SITE=SITE, email=AUTHOR['email'], phone=AUTHOR['phone'], year=TODAY[:4]).replace("</body>\n</html>\n", "")}
<script src="assets/pub.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- files
def stage_files():
    """Copy the original documents into publications/files/ with clean names."""
    staged = {}
    for w in WORKS:
        src = os.path.join(NEW, w["primary"])
        ext = os.path.splitext(w["primary"])[1].lower().lstrip(".")
        dst = os.path.join(FILES, f"{w['slug']}-source.{ext}")
        shutil.copy2(src, dst)
        w["source_ext"] = ext
        staged[w["slug"]] = dst
    return staged


def build_library_json():
    data = {
        "version": "1.0",
        "generated": TODAY,
        "author": {
            "name": AUTHOR["name"], "short": AUTHOR["short"], "degrees": AUTHOR["degrees"],
            "designation": AUTHOR["designation"], "affiliation": AUTHOR["affiliation"],
            "email": AUTHOR["email"], "phone": AUTHOR["phone"], "regNo": AUTHOR["reg_no"],
            "profilePage": SITE + "/", "publicationsPage": SITE + "/publications/",
        },
        "license": "CC BY 4.0",
        "count": len(WORKS),
        "works": []
    }
    for w in sorted(WORKS, key=lambda x: (x.get("year", 0), x["slug"]), reverse=True):
        data["works"].append({
            "slug": w["slug"],
            "type": w["type"],
            "typeLabel": w.get("type_label", w["type"]),
            "title": w["title"],
            "subtitle": w.get("subtitle", ""),
            "hook": w["hook"],
            "abstract": w["abstract"],
            "year": w.get("year"),
            "venue": w.get("venue", ""),
            "degree": w.get("degree", ""),
            "institution": w.get("institution", ""),
            "guide": w.get("guide", ""),
            "coauthors": w.get("coauthors", []),
            "keywords": w.get("keywords", []),
            "regNo": w.get("reg_no", ""),
            "url": f"{SITE}/publications/{w['slug']}.html",
            "pdf": f"{SITE}/publications/files/{w['slug']}.pdf",
            "source": f"{SITE}/publications/files/{w['slug']}-source.{w.get('source_ext','')}",
            "citations": {"apa": cite_apa(w), "vancouver": cite_vancouver(w), "bibtex": cite_bibtex(w)},
        })
    with open(os.path.join(PUB, "library.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data


def build_pdfs():
    """Render each work to a full-text open-access PDF using headless Chrome.

    For sources that are already a PDF, the printed cover sheet is merged in front of
    the original document with pypdf so the download carries both the citation-ready
    metadata and the complete original text.
    """
    import extractor
    made, failed, notes = [], [], []
    for w in WORKS:
        src_path = os.path.join(NEW, w["primary"])
        is_pdf = w["source_ext"] == "pdf"

        body_html = ""
        if not is_pdf:
            body_html, plain = extractor.extract(src_path)
            if len(plain.strip()) < 200:
                notes.append(f"{w['slug']}: little extractable text ({len(plain.strip())} chars) — cover sheet only")
                body_html = ""

        tmpl = os.path.join(PRINT, f"{w['slug']}.html")
        with open(tmpl, "w", encoding="utf-8") as f:
            f.write(render_print_page(w, body_html=body_html, full_text=not is_pdf))

        cover = os.path.join(PRINT, f"{w['slug']}-cover.pdf")
        final = os.path.join(FILES, f"{w['slug']}.pdf")
        for p in (cover, final):
            if os.path.exists(p):
                os.remove(p)

        cmd = [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
               f"--print-to-pdf={cover}", f"file:///{tmpl.replace(os.sep, '/')}"]
        try:
            subprocess.run(cmd, capture_output=True, timeout=180)
        except Exception as e:
            failed.append((w["slug"], str(e)[:200]))
            continue

        if not (os.path.exists(cover) and os.path.getsize(cover) > 2000):
            failed.append((w["slug"], "cover render failed"))
            continue

        try:
            if is_pdf:
                from pypdf import PdfReader, PdfWriter
                writer = PdfWriter()
                for page in PdfReader(cover).pages:
                    writer.add_page(page)
                for page in PdfReader(src_path).pages:
                    writer.add_page(page)
                writer.add_metadata({
                    "/Title": w["title"], "/Author": AUTHOR["name"],
                    "/Subject": clean_inline(w["abstract"])[:250], "/Keywords": "; ".join(w.get("keywords", [])),
                    "/Creator": "Dr. Nidhi Patel open-access publications",
                })
                with open(final, "wb") as f:
                    writer.write(f)
            else:
                shutil.copy2(cover, final)
            made.append(w["slug"])
        except Exception as e:
            failed.append((w["slug"], f"merge failed: {e}"))
    return made, failed, notes


def build_sitemap():
    """sitemap.xml covering the home page, the publications index and every work."""
    urls = [(SITE + "/", TODAY, "1.0", "weekly"),
            (SITE + "/publications/", TODAY, "0.9", "weekly")]
    for w in WORKS:
        urls.append((f"{SITE}/publications/{w['slug']}.html", TODAY, "0.8", "monthly"))
    body = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for loc, lm, pr, cf in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + body + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    return len(urls)


def build_robots():
    txt = f"""# robots.txt for {SITE}
User-agent: *
Allow: /
Disallow: /publications/print/

# Crawl the whole publication library at a gentle pace.
Crawl-delay: 1

User-agent: Googlebot
Allow: /

User-agent: Googlebot-News
Allow: /

User-agent: bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: SemanticScholarBot
Allow: /

User-agent: academic crawlers
Allow: /

Sitemap: {SITE}/sitemap.xml
"""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def build_rss():
    items = []
    for w in sorted(WORKS, key=lambda x: (-x.get("year", 0), x["title"])):
        url = f"{SITE}/publications/{w['slug']}.html"
        items.append(f"""    <item>
      <title>{esc(w['title'])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{datetime.datetime(w.get('year', 2024), 1, 1).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
      <category>{esc(w.get('type_label', w['type']))}</category>
      <description>{esc(clean_inline(w['abstract'])[:600])}</description>
      <dc:creator>Dr. Nidhi Sanjay Patel</dc:creator>
    </item>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Dr. Nidhi Patel (M.S.) — Publications &amp; Academic Works</title>
    <link>{SITE}/publications/</link>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>Open-access publications of Dr. Nidhi Sanjay Patel, M.S. (Ayurveda) in Prasuti Tantra &amp; Stree Roga: dissertation, journal articles, conference abstracts and seminar presentations.</description>
    <language>en-in</language>
    <copyright>Dr. Nidhi Sanjay Patel</copyright>
    <lastBuildDate>{datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    <generator>DrNidhi_portfolio build pipeline</generator>
{chr(10).join(items)}
  </channel>
</rss>
"""
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    print("staging source files...")
    stage_files()
    print("writing pages...")
    with open(os.path.join(PUB, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index())
    for w in WORKS:
        with open(os.path.join(PUB, f"{w['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(render_work_page(w))
    build_library_json()
    print("patching root index.html...")
    print("  index patched" if patch_index() else "  index already current")
    n = build_sitemap()
    build_robots()
    build_rss()
    print(f"  sitemap: {n} urls | robots.txt + rss.xml written")
    print("rendering PDFs...")
    made, failed, notes = build_pdfs()
    print(f"  PDFs made: {len(made)} | failed: {len(failed)}")
    for s, e in failed:
        print("   FAIL", s, e.replace("\n", " ")[:200])
    for n in notes:
        print("   NOTE", n)
    print("done.")


if __name__ == "__main__":
    main()
