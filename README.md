# DrNidhi_portfolio

Personal website and academic publication record of **Dr. Nidhi Sanjay Patel** (B.A.M.S., M.S. Ayurveda —
Prasuti Tantra & Stree Roga), Assistant Professor at Uka Tarsadia University (UTU), Bardoli, Gujarat.

**Live site: <https://www.drnidhi.net/>** — static HTML, CSS and JavaScript, deployed by Vercel from this
repository. `drnidhi.net` redirects to `www`, which is the canonical host on every page.

![The home page](./web.png)

---

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | The single-page website: hero, about, personal note, services, journey, publications preview, FAQ, contact. Carries the `Person` JSON-LD. |
| `style.css` | All site styles. |
| `script.js` | Navigation, scroll reveal, compass widget, dinacharya tabs, FAQ. |
| `writing/` | The publications library — a self-contained sub-site. See below. |
| `sitemap.xml` | XML sitemap, 22 URLs. |
| `robots.txt` | Allows search engines, AI answer engines and academic crawlers. |
| `rss.xml` | RSS feed of the publication record. |
| `writing/upload-kit/` | Ready-to-paste metadata for every external platform. |
| `newdata/` | **Source material** (7.2 GB of original documents). *Not committed* — the working archive the publications were built from. |

---

## The Writing library

`writing/` is a complete, self-contained open-access publication site. Every work authored or presented by
Dr. Nidhi Patel is published there in full, with metadata, citations and a downloadable PDF.

```
writing/
├── index.html            searchable, filterable catalogue
├── library.json          machine-readable catalogue of all 20 works
├── <slug>.html           one page per work (20 pages)
├── assets/               pub.css, pub.js
├── files/                open-access PDF + the original document, per work
├── print/                print templates used to generate the PDFs
├── upload-kit/           ready-to-paste metadata for every external platform
├── catalog.py            the single source of truth for the catalogue
├── build.py              generates the pages, PDFs, sitemap, robots, RSS
├── build_kit.py          generates the upload kit
├── build_deploy.py       writes deploy/DEPLOY.md (and a portable zip on request)
├── extractor.py          DOCX/PPTX/PDF text extraction
└── verify.py             validation — run this after any change
```

### The catalogue

20 works, all authored or presented by Dr. Nidhi Patel:

| Type | Count | Works |
|---|---|---|
| M.S. dissertation | 1 | Lashuna Kalpa & Rasnadi Taila Uttar Basti in Artava Kshaya — a randomised clinical study in 30 subjects |
| Peer-reviewed article | 2 | Effect of Pumsavana Karma in Conception (IJCRT); Role of Dinacharya in the Prevention of Health Hazards of Pollution |
| Conference abstracts | 4 | Panchakarma in Vandhyatwa; Preconceptional Care; Role of Uttarbasti in Yonivyapada; Ayurveda for Public Health |
| Seminar presentations | 13 | Pathya, Rasa, Sadarasa, Vomiting in Pregnancy, Stages of Labour, Epilepsy in Pregnancy, GDM, Artava Kshaya, Delivery of IUGR, Abnormal Development of Fallopian Tube and Ovary, Applied Anatomy of the Abdomen, Prasava Vigyana, Dinacharya & Immunity |

Material belonging to other doctors and colleagues is deliberately excluded, as are all patient records,
admission letters, score cards and other personal documents.

### Rebuilding

```bash
py writing/build.py          # pages, PDFs, sitemap.xml, robots.txt, rss.xml, index.html patch
py writing/build_kit.py      # upload-kit/ (CSV per platform + guides)
py writing/build_deploy.py   # deploy/DEPLOY.md
py writing/verify.py         # validation — should report 0 errors
```

Requires Python 3, `pypdf` (`py -m pip install pypdf`) and Google Chrome (for PDF rendering).

`verify.py` is the gate. It checks JSON-LD, tag balance, every internal link target, XML well-formedness,
catalogue consistency, PDF presence, that no page still points at the retired host, and that every header
nav item resolves to a real section or page.

### Upload kit

`writing/upload-kit/` contains everything needed to publish the same work on other platforms, with the
exact title, abstract, keywords, description and citation for each:

| File | What it gives you |
|---|---|
| `MASTER-UPLOAD-PLAN.md` | The whole route: which platform, in what order, and why. |
| `UPLOAD-GUIDE.md` | Step-by-step instructions for each platform. |
| `ORDER-RECOMMENDATION.md` | Which work to upload first, and which audience each platform reaches. |
| `HOOKS.md` | The hook strategy — content, technical, citation and link hooks. |
| `PROFILE-COPY.md` | Bio and profile text for each platform. |
| `MANIFEST.json` | Every work, every platform field, machine-readable. |
| `upload-console.html` | Click-to-copy version of the manifest, with progress tracking. |
| `TRACKER.csv` | The audit trail: fill in the public URL as you upload. |
| `researchgate.csv` `academia.csv` `academia_india.csv` `scribd.csv` `slideshare.csv` `zenodo.csv` `osf.csv` `scholar.csv` `doaj.csv` | One row per work, ready to paste. |

Every description in the kit ends with the work's canonical `https://www.drnidhi.net/writing/...` URL, so
each external copy cites the original. Fill in the `Public URL (after upload)` column as you go.

---

## Header navigation

The header is a single sticky row: **Home · About · My Note · Services · Writing · FAQ · Contact**.

`Writing` is the only item that leaves the home page, so it carries a gold dot. The `Rhythms` and `Journey`
sections still exist on the page; they were removed from the header because nine items overflowed the bar.

Sections carry `scroll-margin-top`, so deep links such as `https://www.drnidhi.net/#about` (used by the
publications sub-site) land below the floating nav instead of behind it.

---

## SEO / discovery hooks

- `ScholarlyArticle` + `citation_*` JSON-LD on every work page
- `BreadcrumbList` on every work page, `ItemList` on the index, `Person` with `hasPublished` on the home page
- Canonical URLs, Open Graph and Twitter card tags on every page
- `sitemap.xml` (22 URLs), `robots.txt` explicitly allowing scholarly and AI crawlers, `rss.xml`
- APA / Vancouver / BibTeX citation blocks on every work page
- Internal topic clusters linking the works to each other; keywords link back into the filtered index
- `library.json` for any tool that wants to ingest the whole record

---

## Stack

Vanilla HTML, CSS and JavaScript. No bundler, no framework, no runtime dependencies. The Python scripts in
`writing/` are a one-off content pipeline, not part of the site.

## Deployment

Pushing to the default branch is the deploy — Vercel builds the static site and serves it at
`https://www.drnidhi.net`. Details, DNS records and the post-deploy check list are in
[`deploy/DEPLOY.md`](deploy/DEPLOY.md).
