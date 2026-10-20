# -*- coding: utf-8 -*-
"""
Generates the multi-platform upload kit.

Produces, for every published work, ready-to-paste metadata for each academic /
document-sharing platform, plus a machine-readable manifest and a step-by-step guide.

    publications/upload-kit/
        MANIFEST.json          one record per work, all platforms
        <platform>.csv         one row per work, ready to paste into each platform
        UPLOAD-GUIDE.md        step-by-step, platform by platform
        ORDER-RECOMMENDATION.md  which platform, in what order, and why
"""
import os, csv, json, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from catalog import WORKS, AUTHOR
from build import cite_apa, cite_vancouver, cite_bibtex, SITE, clean_inline

ROOT = r"C:\Users\nidhi\harshal\DrNidhi_portfolio"
KIT = os.path.join(ROOT, "publications", "upload-kit")
os.makedirs(KIT, exist_ok=True)
TODAY = datetime.date.today().isoformat()

AUTHOR_LINE = f"{AUTHOR['name']}, {AUTHOR['degrees']}"
AFFIL_SHORT = "Department of Prasuti Tantra & Stree Roga, Uka Tarsadia University (UTU), Bardoli, Gujarat, India"
AFFIL_ORIG = "Department of Prasuti Tantra & Stree Roga, Dr. N.R.S. Govt. Ayurvedic College, Vijayawada, Andhra Pradesh, India"


def affiliation(w):
    return AFFIL_ORIG if w.get("institution") else AFFIL_SHORT


def platform_fields(w):
    """The per-platform metadata blocks for one work."""
    title = w["title"]
    abstract = w["abstract"]
    kw = w.get("keywords", [])
    kwlist = [k for k in kw]
    kwsemi = "; ".join(kwlist)
    kwcomma = ", ".join(kwlist)
    short = w["hook"]
    # a genuinely short description for platforms with a 250-char box
    desc = (short + " " + w["abstract"])[:480]
    desc_short = short[:250]
    return {
        "title": title,
        "subtitle": w.get("subtitle", ""),
        "abstract": abstract,
        "description_250": desc_short,
        "description_480": desc[:480],
        "keywords": kwcomma,
        "keywords_semicolon": kwsemi,
        "tags_lower": [k.lower() for k in kwlist],
        "topics": ["Ayurveda", "Prasuti Tantra", "Stree Roga", "Women's health", "Fertility",
                   "Clinical study", "Open access"],
        "citation_apa": cite_apa(w),
        "citation_vancouver": cite_vancouver(w),
        "citation_bibtex": cite_bibtex(w),
        "author_line": AUTHOR_LINE,
        "affiliation": affiliation(w),
        "coauthors": w.get("coauthors", []),
        "guide": w.get("guide", ""),
        "year": w.get("year", ""),
        "venue": w.get("venue", ""),
        "degree": w.get("degree", ""),
        "reg_no": w.get("reg_no", ""),
        "type": w["type"],
        "type_label": w.get("type_label", w["type"]),
    }


PLATFORMS = [
    ("researchgate", "ResearchGate", "Highest-value academic network; heavy traffic from researchers and clinicians. Public full-text PDF + 'publications' profile."),
    ("academia", "Academia.edu", "Very large readership in the health/medical fields; free PDF upload; good for conference abstracts and slides."),
    ("scribd", "Scribd", "Excellent organic search reach for long documents; each upload is a discoverable page. Good for the thesis."),
    ("slideshare", "SlideShare", "Presentation-first; the seminar decks land on a very large slide-sharing audience."),
    ("zenodo", "Zenodo", "Permanent DOI per record, indexed by Google and harvested by OpenAIRE / CORE / BASE. The strongest long-term citation hook."),
    ("osf", "OSF (Open Science Framework)", "Open projects + preprint space; good for sharing the thesis and data alongside it."),
    ("scholar", "Google Scholar (via a public profile)", "The primary citation index for a clinical academic. Every work should be listed with a 'Cited by' link to the open-access PDF."),
    ("doaj", "DOAJ / Open-access journals", "Only for peer-reviewed articles; the route to indexing in Scopus and PubMed-adjacent services."),
    ("academia_india", "Academia.edu (Ayurvedic topic tags)", "Same upload, but tagged to Ayurveda / Indian medicine communities where the readership is concentrated."),
]


CSV_ALIAS = {"academia_india": "academia"}


def build_manifest():
    records = []
    for w in sorted(WORKS, key=lambda x: (x.get("year", 0), x["slug"]), reverse=True):
        pf = platform_fields(w)
        records.append({
            "slug": w["slug"],
            "canonicalUrl": f"{SITE}/publications/{w['slug']}.html",
            "openAccessPdf": f"{SITE}/publications/files/{w['slug']}.pdf",
            "sourceFile": f"publications/files/{w['slug']}-source.{w.get('source_ext','')}",
            "platforms": pf,
        })
    manifest = {
        "generated": TODAY,
        "author": {
            "name": AUTHOR["name"], "degrees": AUTHOR["degrees"],
            "designation": AUTHOR["designation"], "affiliation": AFFIL_SHORT,
            "email": AUTHOR["email"], "phone": AUTHOR["phone"],
            "orcid": "CREATE: https://orcid.org/register",
            "regNo": AUTHOR["reg_no"],
        },
        "canonicalHome": SITE + "/publications/",
        "rss": SITE + "/rss.xml",
        "catalogJson": SITE + "/publications/library.json",
        "license": "CC BY 4.0",
        "works": records,
    }
    with open(os.path.join(KIT, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest


CSV_FIELDS = {
    "researchgate": ["Title", "Type", "Year", "Authors", "Co-authors", "Abstract", "Keywords",
                     "Conference/Journal", "Guide", "File to upload", "Open-access PDF (link this)", "Public URL (after upload)",
                     "APA citation", "Vancouver citation", "Canonical open-access URL", "Suggested tags"],
    "academia": ["Title", "Type", "Year", "Description (short, max 250 chars)", "Abstract", "Keywords",
                  "Tags (lowercase)", "Topics", "File to upload", "Open-access PDF (link this)", "Public URL (after upload)",
                  "APA citation", "Canonical open-access URL"],
    "scribd": ["Title", "Description (max 480 chars)", "Category", "Tags", "Keywords", "License",
               "File to upload", "Open-access PDF (link this)", "Public URL (after upload)", "Suggested folder"],
    "slideshare": ["Title", "Description (max 480 chars)", "Tags", "Category", "Language",
                   "File to upload", "Open-access PDF (link this)", "Public URL (after upload)", "License"],
    "zenodo": ["Title", "Type", "Creators", "Description", "Keywords", "Related identifiers",
               "License", "File to upload", "Open-access PDF (link this)", "DOI (auto)", "Community", "Suggested community"],
    "osf": ["Title", "Description", "Tags", "Resource type", "File to upload", "Open-access PDF (link this)", "Public URL (after upload)"],
    "scholar": ["Title", "Publication type", "Year", "Authors", "Keywords", "Description",
                "Public URL of the open-access PDF", "Canonical open-access URL", "Notes"],
    "doaj": ["Title", "Abstract", "Keywords", "Journal (if published)", "Year", "Authors",
             "DOI (of the published article)", "File to upload", "Open-access PDF (link this)", "Notes"],
}


def upload_file_for(platform, w):
    """Which file to actually upload to this platform."""
    ext = w.get("source_ext") or os.path.splitext(w["primary"])[1].lstrip(".")
    src = f"publications/files/{w['slug']}-source.{ext}"
    oa = f"publications/files/{w['slug']}.pdf"
    if platform == "scribd":
        # Scribd renders native documents best
        return src
    if platform == "slideshare":
        # SlideShare needs the deck itself
        return src
    if platform == "doaj":
        return src
    # researchgate, academia, zenodo, osf, scholar -> the open-access PDF
    return oa


def csv_row(platform, w, pf):
    f = CSV_FIELDS[platform]
    pdf = f"publications/files/{w['slug']}.pdf"
    src = f"publications/files/{w['slug']}-source.{w.get('source_ext','')}"
    co = "; ".join(pf["coauthors"])
    vals = {
        "Title": pf["title"],
        "Type": pf["type_label"],
        "Year": pf["year"],
        "Authors": pf["author_line"],
        "Co-authors": co,
        "Abstract": pf["abstract"],
        "Keywords": pf["keywords_semicolon"],
        "Conference/Journal": pf["venue"],
        "Guide": pf["guide"],
        "File to upload": upload_file_for(platform, w),
        "Open-access PDF (link this)": pdf,
        "Public URL (after upload)": "",
        "APA citation": pf["citation_apa"],
        "Vancouver citation": pf["citation_vancouver"],
        "Canonical open-access URL": f"{SITE}/publications/{w['slug']}.html",
        "Suggested tags": pf["keywords"],

        "Description (short, max 250 chars)": pf["description_250"],
        "Description (max 480 chars)": pf["description_480"],
        "Tags (lowercase)": ", ".join(pf["tags_lower"]),
        "Topics": "; ".join(pf["topics"]),

        "Category": "Research Paper" if w["type"] in ("Thesis", "Article") else "Article",
        "License": "Creative Commons Attribution 4.0 (CC BY 4.0)",
        "Suggested folder": ("Academic research" if w["type"] in ("Thesis", "Article")
                             else "Health & Medicine / Ayurveda"),

        "Language": "English",

        "Creators": pf["author_line"] + (f"; {co}" if co else ""),
        "Related identifiers": f"Related to: {SITE}/publications/{w['slug']}.html",
        "DOI (auto)": "(Zenodo assigns on publish)",
        "Community": "Open Access",
        "Suggested community": "Medicine and Health Sciences / Ayurveda",

        "Resource type": "Thesis" if w["type"] == "Thesis" else "Presentation",
        "Public URL of the open-access PDF": f"{SITE}/publications/files/{w['slug']}.pdf",

        "Publication type": {"Thesis": "Dissertation/thesis",
                             "Article": "Journal article",
                             "Abstract": "Conference abstract",
                             "Seminar": "Conference presentation"}[w["type"]],
        "Authors": pf["author_line"],
        "Description": pf["abstract"],
        "Notes": "List this work on your public profile so it appears in Google Scholar and other indexes.",

        "Journal (if published)": pf["venue"],
        "DOI (of the published article)": "(use the DOI printed in the published article)",
    }
    return {k: vals.get(k, "") for k in f}


def build_csvs():
    for platform, label, _ in PLATFORMS:
        key = CSV_ALIAS.get(platform, platform)
        path = os.path.join(KIT, f"{platform}.csv")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=CSV_FIELDS[key])
            wr.writeheader()
            for w in sorted(WORKS, key=lambda x: (x.get("year", 0), x["slug"]), reverse=True):
                pf = platform_fields(w)
                row = csv_row(key, w, pf)
                if platform == "academia_india":
                    row["Tags (lowercase)"] = ", ".join(
                        pf["tags_lower"] + ["ayurveda", "indian medicine", "prasuti tantra", "stree roga"])
                    row["Topics"] = "; ".join(pf["topics"] + ["Ayurvedic medicine", "Indian medicine"])
                wr.writerow(row)


GUIDE = """# Upload guide — distributing Dr. Nidhi Patel's publications

**Everything you need is in this folder.** Each `*.csv` has one row per work, with the exact
title, abstract, keywords, description and citation to paste into that platform. The file to
upload is named in the `File to upload` column and lives in `../files/`.

Two rules that matter more than anything else:

1. **Upload the open-access PDF first** (`publications/files/<slug>.pdf`). It already contains the
   title page, the abstract, the full text and the citation block. It is the same file that is
   live on `drnidhi.great-site.net`, so the two never drift apart.
2. **Put the canonical URL in the description of every upload.** Every platform makes the
   description crawlable, and the canonical URL is what passes the citation back to the author's
   own site. This is the single most valuable line in each row.

After uploading, paste the resulting public URL back into the `Public URL (after upload)` column
of the same CSV. That column is what makes the kit reusable and auditable.

---

## Order of operations (do these in this order)

| # | Platform | Why first / why here |
|---|----------|----------------------|
| 1 | **ORCID** | Every other platform asks for an ORCID iD, and ORCID is the identifier that connects the name to the works. Register at orcid.org, add the affiliation (Uka Tarsadia University), the BAMS and M.S. credentials, and the 20 works with their DOIs as you create them. |
| 2 | **Google Scholar** | A public profile is free and puts the works into the citation index that clinicians, journals and the AYUSH community actually consult. Upload a PDF to each works entry so it says "[PDF]". |
| 3 | **ResearchGate** | The professional network for academics; puts the thesis and the peer-reviewed article in front of postgraduate supervisors and journal editors. |
| 4 | **Academia.edu** | Largest readership in the health fields; each upload is indexed separately, so the seminar talks and abstracts become individually discoverable. |
| 5 | **Scribd** | Strong organic search; ideal for the full thesis and the longer seminar write-ups. |
| 6 | **SlideShare** | Puts the seminar decks in front of a very large audience that browses by topic. |
| 7 | **Zenodo** | Issues a **DOI** for every upload. This is the long-term hook — DOIs are harvested by CORE, OpenAIRE, BASE, Semantic Scholar and DataCite. |
| 8 | **OSF** | Hosts the thesis, the master chart and the raw statistics as an open project, which is what a reviewer or a future supervisor will ask for. |
| 9 | **DOAJ / journal submission** | Only for the two peer-reviewed articles — a route into Scopus-indexed and PubMed-adjacent indexes. |

---

## Platform notes

### ResearchGate
- Profile → **Add a public profile**. Title: `Dr. Nidhi Patel` · Organisation: `Uka Tarsadia University (UTU)`.
- **Publication → Add** → *Full-text publication* for the thesis and the IJCRT article.
  Title, abstract and keywords come straight from the `researchgate.csv` row.
- For conference abstracts and seminars use **Add → Conference paper** (or *Preprint* / *Poster*).
- Upload `files/<slug>-source.docx` for abstracts (ResearchGate converts and indexes the text)
  and `files/<slug>.pdf` for the thesis and the article.
- Paste the canonical URL at the end of the abstract — ResearchGate renders it as a clickable link.

### Academia.edu
- Add the affiliation first; Academia builds a topic graph from it.
- **Upload → Research** with the *Description (short, max 250 chars)* from the `academia.csv` row
  and the full abstract in the body.
- Tag with the lowercase keyword list; that is what puts the work into the right topic feeds.
- For the seminar decks upload the `pptx` source so Academia can extract the slide text.

### Scribd
- Category: *Academic research* / *Health & Medicine → Ayurveda*.
- Title and the 480-character description from `scribd.csv`.
- Set the license to **CC BY 4.0** — this is what lets other academics re-use it in teaching.
- The thesis should be uploaded as a single document, with a contents page, so Scribd can
  extract and index the individual chapters.

### SlideShare
- Upload the `pptx` source of each seminar talk.
- Use the hook line as the description — it is written to make a reader stop scrolling.
- Tags: the lowercase keyword list plus `ayurveda`, `obgyn`, `fertility`.

### Zenodo
- **New upload → Upload**, then publish. Zenodo mints a DOI and a landing page with the
  description, keywords, licence and the related identifier.
- Suggested community: *Medicine and Health Sciences* → *Ayurveda* (or *Open Access*).
- Add the canonical site URL in **Related identifiers → Related identifier → URL**.
- Once a DOI exists, add it back to the corresponding Google Scholar, ResearchGate and
  Academia.edu records, and to `publications/catalog.py` so the site itself carries the DOI.

### OSF
- Create a project, e.g. *Ayurvedic management of Artava Kshaya — thesis, data & manuscripts*.
- Attach the thesis PDF, the master chart and the statistics files.
- OSF gives a DOI for the project; add it to the thesis record on every other platform.

### Google Scholar
- Create a **public profile** (not a verified one — verification is optional and slow).
- Add each work: title, publication type, year, authors, keywords, and the abstract.
- In the **link** field use `https://drnidhi.great-site.net/publications/files/<slug>.pdf`
  so Google indexes the open-access copy and shows the green `[PDF]` marker.
- This is what makes the works citable, and it is where the citation count accumulates.

### DOAJ / journal submission
- Only the two peer-reviewed articles. Reformat to the target journal's template, keep the
  DOI of the existing published version, and cite the author's earlier work
  (the *Effect of Pumsavana Karma in Conception* article) to build the author's citation graph.

---

## Description to use everywhere (single-line bio)

> Dr. Nidhi Sanjay Patel is an Ayurvedic physician (B.A.M.S., M.S. Ayurveda — Prasuti Tantra &
> Stree Roga) and Assistant Professor at Uka Tarsadia University, Bardoli, Gujarat, India. Her
> clinical and research work focuses on Ayurvedic management of menstrual and fertility
> disorders, antenatal and postnatal care, and the evidence base for Panchakarma and Uttar
> Basti in women's health. Her M.S. dissertation examined Lashuna Kalpa and Rasnadi Taila
> Uttar Basti in Artava Kshaya (hypomenorrhoea) in a 30-subject randomised clinical study.
"""


def build_guide():
    with open(os.path.join(KIT, "UPLOAD-GUIDE.md"), "w", encoding="utf-8") as f:
        f.write(GUIDE)


def build_order():
    lines = ["# Platform recommendation — what to upload where, and why\n",
             "\nThe short version: **the thesis and the journal article first, then the four conference",
             "abstracts, then the thirteen seminar talks.** The thesis and the peer-reviewed article",
             "are the works that carry the most weight with employers, journal editors and postgraduate",
             "supervisors; the seminar talks are the ones that build reach.\n",
             "\n## Priority table\n",
             "| Priority | Work | Type | Best platforms | Why this order |",
             "|---|---|---|---|---|"]
    prio = [
        ("1", "lashuna-kalpa-rasnadi-taila-uttar-basti-artava-kshya", "M.S. dissertation",
         "Scribd, Zenodo, OSF, ResearchGate, Google Scholar, Academia.edu",
         "The flagship work. A 30-subject randomised clinical study is the single most persuasive item in the profile, and it is the one most often asked for at interviews."),
        ("2", "effect-of-pumsavana-karma-in-conception", "Peer-reviewed article (IJCRT)",
         "ResearchGate, Google Scholar, Academia.edu, DOAJ, Zenodo",
         "A published, citable article. This is what makes the profile read as 'researcher' rather than 'student'."),
        ("3", "conceptual-approach-to-preconceptional-care-in-ayurveda", "Conference abstract",
         "ResearchGate, Academia.edu, Google Scholar",
         "Structured abstract with Introduction, Methods, Results and Discussion — the format journals and reviewers recognise immediately."),
        ("4", "role-of-panchakarma-in-vandhyatwa", "Conference abstract",
         "ResearchGate, Academia.edu, Google Scholar",
         "A comprehensive review — reviews are the most re-used and most re-cited format on every academic network."),
        ("5", "role-of-uttarbasti-in-yonivyapada", "Conference abstract",
         "ResearchGate, Academia.edu, Google Scholar",
         "Directly pairs with the thesis topic; uploading it builds a visible cluster around Uttar Basti."),
        ("6", "ayurveda-for-public-health", "Conference abstract",
         "Academia.edu, ResearchGate",
         "Reaches the public-health and preventive-medicine readership, which is the fastest-growing audience for Ayurveda."),
        ("7", "role-of-dinacharya-in-prevention-of-health-hazards-of-pollution", "BAMS compilation",
         "Scribd, Academia.edu",
         "An early undergraduate work; upload it to show academic continuity from 2020 to 2025."),
        ("8-20", "remaining seminar talks", "Seminar presentations",
         "SlideShare, Academia.edu, Scribd",
         "These build reach. SlideShare in particular puts them in front of a very large slide audience and each upload is independently searchable."),
    ]
    for p, slug, typ, plats, why in prio:
        w = next((x for x in WORKS if x["slug"] == slug), None)
        title = w["title"] if w else slug
        lines.append(f"| {p} | {title} | {typ} | {plats} | {why} |")

    lines += ["\n## Reading-level and audience fit\n",
              "| Audience | Send them |",
              "|---|---|",
              "| Postgraduate students in Prasuti Tantra / Stree Roga | The thesis, the abstracts, the seminar decks (SlideShare + Academia.edu) |",
              "| Journal editors and peer reviewers | The IJCRT article, the two review-format abstracts (ResearchGate + Google Scholar) |",
              "| Prospective employers and university departments | The thesis, the published article, and the open-access PDF links (Scribd + Zenodo DOIs) |",
              "| Patients and the general public | The Dinacharya, pollution-prevention and public-health works — these are the ones that bridge to the clinical site |",
              "| Global Ayurveda researchers | All of it, via Zenodo (DOIs) and Academia.edu topic tags |",
              "\n## Do not upload\n",
              "Only material authored by Dr. Nidhi Patel is in this kit. Material belonging to other",
              "doctors and colleagues in the shared folders — Dr. Kola Vijaya Kumari, Dr. Krushna Chaitanya",
              "Patnaik, Dr. Sindhuja, Dr. Sunayana, Dr. Kalpana Malviya, Dr. Vagdevi, Dr. Manoj Gaikwad,",
              "Dr. Purnendu Panda, Dr. Sribala, and the rest — is deliberately excluded, along with all",
              "patient records, admission letters, score cards and other personal documents. A co-author",
              "is credited where the work is genuinely co-authored, and never removed from a joint work.",
              ]
    with open(os.path.join(KIT, "ORDER-RECOMMENDATION.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_hooks():
    """The hook strategy — content hooks, technical hooks, link hooks, measurement."""
    hook_rows = "\n".join(
        f"| [{w['title']}]({SITE}/publications/{w['slug']}.html) | {w['hook']} |"
        for w in sorted(WORKS, key=lambda x: (x.get("year", 0), x["slug"]), reverse=True))

    txt = f"""# The hook strategy

A *hook* is the line, link or field that makes a reader stop — and the same hook is what
tells a machine (Google, a citation index, a journal editor) that this work is connected to
the rest of the record. Both are built into this site already; this page explains what they
are so they can be reused on every platform.

---

## 1. Content hooks — the opening line

Every work on this site opens with a single line that states the question the work answers,
not the topic it covers. A topic gets skimmed; a question gets read. These lines are also the
description used on SlideShare, Academia, Scribd and Zenodo, so one piece of writing serves
both the human reader and the crawler.

{hook_rows}

**The title formulas these hooks are built for**

| Formula | Example | Why it works |
|---|---|---|
| *Can [intervention] [outcome]? This [design] answers the question.* | Can a simple oil-based Uttar Basti measurably restore menstrual flow in arthava kshaya? | States the question, the design and the scale in one sentence. |
| *[Intervention] is rarely [X]. This [work] maps [Y].* | Female infertility is rarely a one-herb problem. | Reframes a familiar thing as more complicated than assumed. |
| *[Concept] is [claim]. This [work] covers [scope].* | Ayurveda does not have an "immunity" chapter — it has a daily schedule. | Surprises the reader and creates a curiosity gap. |
| *[Textual claim] — [translation]. This [work] explains [why it matters].* | "Pumsavanam ithi pumsatva karakam karma" — the ritual that literally means "the ritual that brings forth the child". | Uses the original Sanskrit as a second hook inside the first. |

---

## 2. Technical hooks — what makes the work findable by machines

These are already live on every page. They are the difference between a page that exists and a
page that gets cited.

| Hook | Where | What it does |
|---|---|---|
| `ScholarlyArticle` JSON-LD | every work page | Tells search engines the page is an academic work, not a blog post. |
| `citation_title`, `citation_author`, `citation_publication_date`, `citation_journal_title`, `citation_conference_title`, `citation_pdf_url`, `citation_abstract`, `citation_keywords` | every work page | The classic scholar-citation fields. Reference managers and indexing services read these to build a bibliographic record. |
| `BreadcrumbList` JSON-LD | every work page | Puts the work in a hierarchy: Home → Publications → Work. |
| `ItemList` + `CollectionPage` JSON-LD | publications index | Declares the whole library as one collection, so the list can be surfaced whole. |
| `Person` JSON-LD with `hasCredential`, `alumniOf`, `worksFor`, `hasPublished` | home page | Binds the degrees, the university and every work to the person entity, so the profile accumulates authority. |
| `canonical` link | every page | Stops duplicate content from splitting the authority across the 20 pages. |
| Open Graph + Twitter card tags | every page | Controls how the link looks when shared on WhatsApp, LinkedIn, X and Facebook. This is what the audience actually sees. |
| `sitemap.xml` with all 22 URLs | root | Tells Google exactly what exists and how fresh it is. |
| `rss.xml` | root | A machine-readable feed of the work. Aggregators and tools that watch feeds pick it up. |
| `robots.txt` explicitly allowing scholarly crawlers | root | `GPTBot`, `CCBot`, `SemanticScholarBot` and academic crawlers are allowed in by name — AI answer engines and academic search engines can then quote and cite the work. |
| `library.json` | publications folder | The entire catalogue in one machine-readable file, so any tool can ingest the whole record. |

---

## 3. Citation hooks — making the work citable

Each work page carries a **Cite this work** block in APA 7th, Vancouver and BibTeX. The block
is not decoration: every citation a third party writes is a link back to this site, and each
one strengthens the ranking of the author's other work.

The page also says, in plain words, that citing helps. That single sentence converts a
passive visitor into a citing researcher, which is the highest-value conversion on the page.

**On the platforms:** paste the same three citation formats into the description of every
upload, and always include the canonical URL. A citation with a URL is a link; a citation
without one is a dead end.

---

## 4. Link hooks — internal clusters and external backlinks

### Internal (already built)

Works are cross-linked by shared keywords, so each one passes authority to the others:

- **Uttar Basti cluster** — the dissertation ↔ *Role of Uttarbasti in Yonivyapada* ↔ *Artava Kshaya*
- **Fertility cluster** — *Pumsavana Karma* ↔ *Panchakarma in Vandhyatwa* ↔ *Preconceptional Care* ↔ *Abnormal Development of Fallopian Tube and Ovary*
- **Labour cluster** — *Prasava Vigyana* ↔ *Complications of the Stages of Labour* ↔ *Delivery of IUGR* ↔ *GDM* ↔ *Epilepsy in Pregnancy* ↔ *Vomiting in Pregnancy*
- **Preventive-health cluster** — *Dinacharya and Immunity* ↔ *Dinacharya and Pollution* ↔ *Ayurveda for Public Health*

Keywords on every page link back into the filtered index (`/publications/?q=…`), so a keyword
is also a working internal link rather than a dead label.

### External — the six places that will actually link back

1. **The university department page.** A faculty page that lists publications with a link to
   the open-access PDF is the single most credible backlink available, and it is the one a
   journal editor or an employer will check. This is a request to the H.O.D., not a task.
2. **The AADHYA and Sushruta conference organisers.** They publish abstract books. If the
   abstract is in the book with a link, the link is permanent and indexed. Ask for the URL
   of the abstract and a link to the open-access copy.
3. **The journal.** The IJCRT article's landing page should carry the canonical URL and the
   ORCID in the author metadata. That is a one-line request to the editor.
4. **Google Scholar.** A public profile with `[PDF]` links pointing at the open-access copies
   is the highest-volume citation surface an academic has.
5. **ORCID.** Every DOI and every URL added to the ORCID record is another machine-readable
   statement that this person authored this work.
6. **The institutional repository.** A thesis in a university repository is the standard
   route into Google Scholar and every national indexing service. The Zenodo DOI is a good
   fallback when the university has no repository.

**Anchor text to use** — varied, descriptive, never "click here":
`Dr. Nidhi Patel` · `Patel N. S.` · `Uttar Basti in Artava Kshaya (Patel, 2025)` ·
`Pumsavana Karma in Conception` · `Dr. Nidhi Patel's publications` ·
`Ayurvedic management of Artava Kshaya` · `open-access full text`

---

## 5. What "good" looks like — how to check the hooks are working

| Check | Where | What good looks like |
|---|---|---|
| Indexing | Google `site:drnidhi.great-site.net` | All 22 URLs listed, within days of publishing. |
| Rich result | Google Search Console → Enhancements | The publication pages show as academic content, not just blue links. |
| Structured data | search.google.com/test/rich-results | No errors on `ScholarlyArticle`, `BreadcrumbList`, `Person` or `ItemList`. |
| Citations | Google Scholar profile | The works listed with `[PDF]` markers, and the citation count rising over the following months. |
| DOIs | doi.org resolver | Every Zenodo DOI resolves to the open-access landing page. |
| Referring traffic | Search Console → Traffic → External links | Referring domains from the university, the conference sites and the journals. |
| Social reach | LinkedIn / WhatsApp | The OG card renders with the profile image and a readable title. |

**A realistic timeline.** Indexing takes days. Google Scholar citations take weeks to months.
DOIs take days. The first academic citations of a dissertation often take a year. The value of
this setup is that it is all in place now and compounds from the first upload onwards.

---

## 6. One-page checklist

- [ ] ORCID registered, affiliation and both degrees added
- [ ] Google Scholar public profile created, all 20 works listed with `[PDF]` links
- [ ] ResearchGate profile, thesis + article + 4 abstracts uploaded
- [ ] Academia.edu profile, all 20 works uploaded with Ayurveda topic tags
- [ ] Scribd — thesis uploaded, CC BY 4.0
- [ ] SlideShare — the seminar decks uploaded
- [ ] Zenodo — thesis + article deposited, DOIs minted, DOIs pasted back into `catalog.py`
- [ ] OSF — thesis project with the master chart and statistics attached
- [ ] Every platform description contains the canonical URL
- [ ] Every platform description contains the APA citation
- [ ] `publications/upload-kit/*.csv` → `Public URL (after upload)` column filled in
- [ ] Google Search Console verified, sitemap submitted
- [ ] H.O.D. asked to link the publication list from the department page
"""
    with open(os.path.join(KIT, "HOOKS.md"), "w", encoding="utf-8") as f:
        f.write(txt)


def main():
    m = build_manifest()
    build_csvs()
    build_guide()
    build_order()
    build_hooks()
    print(f"upload kit written: {len(m['works'])} works x {len(PLATFORMS)} platforms")
    for p, l, _ in PLATFORMS:
        print(f"  {p}.csv")


if __name__ == "__main__":
    main()
