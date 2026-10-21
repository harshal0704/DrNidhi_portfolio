# Upload guide — distributing Dr. Nidhi Patel's publications

**Everything you need is in this folder.** Each `*.csv` has one row per work, with the exact
title, abstract, keywords, description and citation to paste into that platform. The file to
upload is named in the `File to upload` column and lives in `../files/`.

> **Start with `MASTER-UPLOAD-PLAN.md`.** It adds the patient-facing channels that this guide does
> not cover, ranks every platform by real impact, and lists the mistakes to avoid. Use
> `upload-console.html` to copy fields without opening the CSVs, and `TRACKER.csv` to track the
> 105 individual uploads.

Two rules that matter more than anything else:

1. **Upload the open-access PDF first** (`writing/files/<slug>.pdf`). It already contains the
   title page, the abstract, the full text and the citation block. It is the same file that is
   live on `drnidhi.net`, so the two never drift apart.
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
  Academia.edu records, and to `writing/catalog.py` so the site itself carries the DOI.

### OSF
- Create a project, e.g. *Ayurvedic management of Artava Kshaya — thesis, data & manuscripts*.
- Attach the thesis PDF, the master chart and the statistics files.
- OSF gives a DOI for the project; add it to the thesis record on every other platform.

### Google Scholar
- Create a **public profile** (not a verified one — verification is optional and slow).
- Add each work: title, publication type, year, authors, keywords, and the abstract.
- In the **link** field use `https://www.drnidhi.net/writing/files/<slug>.pdf`
  so Google indexes the open-access copy and shows the green `[PDF]` marker.
- This is what makes the works citable, and it is where the citation count accumulates.

### DOAJ / journal submission
- **DOAJ is a directory of journals, not a place authors upload articles.** Do not try to submit a
  paper to it. Use `doaj.csv` only as a checklist when choosing where to submit.
- Only the two peer-reviewed articles. Submit to a **DOAJ-indexed** journal with a real editorial
  board (for example *AYU*, *Journal of Ayurveda and Integrative Medicine*, *Journal of
  Research in Ayurvedic Sciences*). Reformat to the target journal's template, keep the
  DOI of the existing published version, and cite the author's earlier work
  (the *Effect of Pumsavana Karma in Conception* article) to build the author's citation graph.
- Read `MASTER-UPLOAD-PLAN.md` first: it explains the prior-publication caveat if the thesis is
  later submitted to a journal.

---

## Description to use everywhere (single-line bio)

> Dr. Nidhi Sanjay Patel is an Ayurvedic physician (B.A.M.S., M.S. Ayurveda — Prasuti Tantra &
> Stree Roga) and Assistant Professor at Uka Tarsadia University, Bardoli, Gujarat, India. Her
> clinical and research work focuses on Ayurvedic management of menstrual and fertility
> disorders, antenatal and postnatal care, and the evidence base for Panchakarma and Uttar
> Basti in women's health. Her M.S. dissertation examined Lashuna Kalpa and Rasnadi Taila
> Uttar Basti in Artava Kshaya (hypomenorrhoea) in a 30-subject randomised clinical study.
