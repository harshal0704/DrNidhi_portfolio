# Master upload plan — Dr. Nidhi Patel

**Goal:** get all 20 works onto the platforms that matter, point every one of them back to
**https://www.drnidhi.net**, and build the kind of visible, checkable credibility that makes a
patient comfortable booking a consultation.

This file is the route. The copy is already written in the CSVs. `upload-console.html` is the
click-to-copy version. `TRACKER.csv` is the audit trail.

---

## Read this first — the honest version

**1. Academic uploads do not bring patients.**
ResearchGate, Academia.edu, Google Scholar and Zenodo build *credibility*. They are what a patient,
a journalist, a university or a referring doctor finds when they check whether you are real and
qualified. They are not where a woman in Surat looks for a gynaecologist at 11 p.m.

**2. Patients come from four places, in this order:**
- **Google Maps / Google Business Profile** — the single biggest source of "doctor near me" calls.
- **Reviews** — 15 to 25 genuine Google reviews will outperform every academic upload combined.
- **Practo / Lybrate / Justdial** — where Indian patients actually shortlist doctors.
- **Short, useful video and posts** — Instagram Reels and YouTube Shorts, in Gujarati and Hindi.

**3. "Famous" is the wrong target; "verifiable" is the right one.**
Nobody books a doctor because she has 40 uploads. They book because the credentials check out, the
answers are specific, the clinic is easy to find, and other women say she listened. The plan below
is built for that, with reach as a by-product.

**4. I cannot create accounts for you.**
Every one of these platforms needs your email, your OTP and your identity. What I *can* do is:
- generate every field so you only copy and paste (done — `upload-console.html`);
- run the entire Zenodo deposit for you, including DOI minting, if you paste a free API token
  (done — `zenodo_deposit.py`, see the last section).

**A note on medical advertising.** Indian medical conduct rules (NMC / State Medical Council) and
the Drugs and Magic Remedies Act restrict soliciting patients and using superlatives. Everything in
this kit is written as factual credential and research disclosure — no "best doctor", no cure
promises, no before/after patient photos, no testimonials that reveal a diagnosis. Keep it that way
and the profile is both compliant and more convincing. If you are unsure about a specific post,
check with your institution's ethics cell before publishing.

---

## What you already have

| Asset | Count | Where |
|---|---|---|
| Works (thesis, articles, abstracts, seminars) | 20 | `writing/library.json` |
| Open-access PDFs, print-ready, with citation block | 20 | `writing/files/*.pdf` |
| Original source files (docx / pptx / pdf) | 20 | `writing/files/*-source.*` |
| Per-platform metadata rows | 9 CSVs | `writing/upload-kit/*.csv` |
| Upload actions in the tracker | 105 | `writing/upload-kit/TRACKER.csv` |
| Live site | 22 URLs | https://www.drnidhi.net |

By type: 1 M.S. dissertation, 2 peer-reviewed articles, 4 conference abstracts, 13 seminar
presentations.

---

## Do these six first

If you do nothing else this month, do these. They cover ~80% of the value.

| # | Action | Exact link | Time | Cost | What it unlocks |
|---|---|---|---|---|---|
| 1 | **Google Business Profile** — the clinic/practice listing | https://business.google.com/add | 30 min + verification | Free | Appears in Maps and "doctor near me"; reviews; calls; directions. The highest-ROI hour in this document. |
| 2 | **ORCID iD** — your permanent researcher ID | https://orcid.org/register | 15 min | Free | Every other academic platform can pull from it. It is the identity anchor for all 20 works. |
| 3 | **Zenodo** — deposit all 20 works, mint 20 DOIs | https://zenodo.org/signup | 2–3 h total (or 10 min with the script) | Free | A citable DOI per work. Harvested by OpenAIRE, CORE, BASE, Semantic Scholar and Google Scholar. The highest-leverage academic move. |
| 4 | **Google Scholar profile** | https://scholar.google.com/citations?view_op=new_profile | 45 min | Free | Puts the works in the index clinicians and journals actually search, with `[PDF]` links back to your site. |
| 5 | **Practo + Lybrate listings** | https://www.practo.com/providers · https://doctor.lybrate.com/ | 40 min | Free (paid tiers optional) | Indian patients shortlist here. Direct appointment enquiries. |
| 6 | **LinkedIn** — profile + publications section + one post | https://www.linkedin.com/signup | 45 min | Free | Where colleagues, universities, conference organisers and journalists verify you. Also ranks well for your name. |

---

## Track A — Credibility and citation (academic)

Ordered by what actually returns value, not by popularity.

| Platform | Link | What goes there | Effort | Verdict |
|---|---|---|---|---|
| **ORCID** | https://orcid.org/register | All 20 works, affiliation, degrees, DOIs | 15 min setup, 1 h works | **Essential.** Do first. |
| **Zenodo** | https://zenodo.org/uploads/new | All 20 PDFs, one deposit each | 2–3 h manual, 10 min scripted | **Essential.** Only route here that mints real DOIs. |
| **Google Scholar** | https://scholar.google.com/citations?view_op=new_profile | All 20, each linked to the PDF on your domain | 45 min | **Essential.** The citation surface that matters. |
| **ResearchGate** | https://www.researchgate.net/ | Thesis + 2 articles + 4 abstracts (7 works) | 90 min | **High.** Where PG supervisors and journal editors look. |
| **Academia.edu** | https://www.academia.edu/upload | All 20, with topic tags | 2 h | **High reach, medium prestige.** Each upload is indexed separately. |
| **OSF** | https://osf.io/register | Thesis + master chart + statistics as an open project | 60 min | **High for transparency.** Reviewers and future supervisors ask for exactly this. |
| **Semantic Scholar** | https://www.semanticscholar.org/ | Nothing to upload — claim the author page once DOIs exist | 10 min | **Free win.** Auto-indexes from Zenodo DOIs. |
| **LinkedIn** | https://www.linkedin.com/feed/ | Publications section, 2–3 posts | 45 min | **High.** Professional verification and referral traffic. |
| **SlideShare** | https://www.slideshare.net/upload | 13 seminar decks (pptx) | 3 h | **Medium.** Good topical reach; low academic weight. |
| **Scribd** | https://www.scribd.com/upload | Thesis + long write-ups | 1 h | **Conditional.** Only if you set free download — see warnings. |
| **Wikidata** | https://www.wikidata.org/wiki/Special:NewItem | One item for the person, linked to ORCID | 30 min | **Optional / advanced.** Helps entity recognition, but self-created items can be challenged for notability. Wait until 3+ independent sources mention you. |

### Platform steps

**ORCID**
1. Register at https://orcid.org/register — use the email you will keep for life.
2. Add employment: *Assistant Professor, Uka Tarsadia University*; add education: B.A.M.S. and
   M.S. (Ayurveda), Prasuti Tantra & Stree Roga.
3. **Works → Add works → Search & link → DataCite.** After the Zenodo deposits exist, this imports
   all 20 DOIs automatically. This is why Zenodo comes before this step.
4. Set visibility to **Public** for everything you want indexed.
5. Copy your ORCID iD (format `0000-0000-0000-0000`) into the site and every other profile.

**Zenodo**
1. Sign up at https://zenodo.org/signup, then verify the email.
2. Either upload manually at https://zenodo.org/uploads/new, or run `zenodo_deposit.py`.
3. Per work: upload `writing/files/<slug>.pdf`; paste Title, Description (abstract), Keywords;
   licence **CC BY 4.0**; type **Publication → Thesis / Journal article / Conference paper**, or
   **Presentation** for the seminars.
4. Add **Related identifiers → URL** = the canonical `https://www.drnidhi.net/writing/<slug>.html`.
5. Publish. Zenodo mints the DOI and the landing page.
6. Paste the DOI back into `catalog.py` (the field already exists) and rebuild the site.

**Google Scholar**
1. Create the profile at the link above. Use your `@utu.ac.in` address if you have one — it makes
   verification and affiliation matching much easier.
2. Add each work manually: title, authors, year, venue, and **the PDF URL on your own domain**
   (`https://www.drnidhi.net/writing/files/<slug>.pdf`). That is what produces the `[PDF]` marker.
3. Set the profile to **public** and copy the profile URL into your site's `sameAs`.

**ResearchGate**
1. Sign up, set organisation to *Uka Tarsadia University*.
2. **Add new → Publication** for the thesis and the two articles; **Conference paper** for the four
   abstracts; **Presentation** for seminars.
3. Paste the hook + abstract + canonical URL. ResearchGate renders the URL as a link.

**Academia.edu**
1. Add the affiliation first — the topic graph is built from it.
2. **Upload → Research**, paste the 250-character description from `academia.csv`, full abstract in
   the body, lowercase tags from the same row.
3. Upload the `-source.pptx` for seminars so the slide text is extractable.

**OSF**
1. Create a project: *Ayurvedic management of Artava Kshaya — thesis, data & manuscripts*.
2. Add components: Thesis, Master chart, Statistics, Manuscripts.
3. OSF mints a project DOI; add it to the thesis record elsewhere.

**Semantic Scholar**
Once 5–10 DOIs resolve, search your name, open the author page and use **Claim this author page**.
No upload needed — it harvests Zenodo/DataCite automatically.

**LinkedIn**
Add a **Publications** section (Profile → Add section → Publications) with title, date and the
canonical URL. Then post once: the thesis, one paragraph on what it found, and the link. Do not
post all 20 at once.

**SlideShare**
Upload the 13 `-source.pptx` decks. Use the hook line as the description and the lowercase keyword
list as tags. Verify the first upload renders correctly before doing the other twelve — the
platform has changed hands and the uploader is inconsistent.

**Scribd**
Only worth it if the document stays downloadable for free (see warnings). Upload the thesis as one
document with a contents page so the chapters are indexed separately.

---

## Track B — Patients and local trust

This is the track that actually fills a clinic. Academic uploads support it; they do not replace it.

| # | Channel | Link | What to do | Cost | Impact |
|---|---|---|---|---|---|
| 1 | **Google Business Profile** | https://business.google.com/add | Claim the practice location; add hours, phone, services, photos, appointment link to drnidhi.net; verify | Free | **Highest.** Maps + local pack + reviews. |
| 2 | **Google reviews** | via the GBP app | Ask every satisfied patient once, in person or by WhatsApp, with a direct review link | Free | **Highest.** 20 reviews changes everything. |
| 3 | **Practo** | https://www.practo.com/providers | Claim/create the doctor profile; set fees, timings, online consultation; link the site | Free / paid boost | **High.** High-intent appointment searches. |
| 4 | **Lybrate** | https://doctor.lybrate.com/ | Doctor profile, specialities, timings, Q&A | Free | **High.** Strong Ayurveda and women's-health traffic. |
| 5 | **Justdial** | https://www.justdial.com/Free-Listing | Free business listing with category *Ayurvedic Doctors* | Free | **Medium-high.** Still heavily used in Gujarat. |
| 6 | **Instagram** | https://www.instagram.com/accounts/emailsignup/ | 3 Reels/week: PCOS, irregular periods, pregnancy diet, Dinacharya. Gujarati + Hindi + English captions | Free | **High reach.** Where patients under 40 are. |
| 7 | **YouTube** | https://www.youtube.com/create_channel | Same videos, longer cut; Shorts cross-posted | Free | **High.** Second-largest search engine; videos rank in Google. |
| 8 | **Facebook page** | https://www.facebook.com/pages/create | Mirror Instagram; local community groups | Free | **Medium.** Still strong for 35+ in Gujarat. |
| 9 | **WhatsApp Business** | https://business.whatsapp.com/ | Catalogue of services, quick replies, appointment hours, away message | Free | **High.** Indian patients prefer it. |
| 10 | **Google Search Console** | https://search.google.com/search-console | Verify drnidhi.net, submit `sitemap.xml`, watch queries | Free | **Essential plumbing.** |
| 11 | **Bing Webmaster Tools** | https://www.bing.com/webmasters | Import from Search Console in one click | Free | **Low effort, real coverage.** Feeds Copilot. |
| 12 | **Sulekha / ClinicSpots / DocIndia / Credihealth** | https://www.sulekha.com/ · https://www.clinicspots.com/ · https://www.docindia.org/ · https://www.credihealth.com/ | Duplicate the verified listing (same name, address, phone) | Free | **Medium.** Citation consistency helps local ranking. |

### The three things that make Track B work

**1. Name, address, phone must match exactly everywhere.**
`Dr. Nidhi Patel (M.S.)`, the UTU hospital address, `+91 70966 40893`. One inconsistent phone number
splits your local ranking. Use the same string in every listing.

**2. Reviews are the trust engine.**
Ask in person at the end of a good visit, then send one WhatsApp message with the review link. Never
offer anything in exchange, never write reviews yourself, never ask a patient to name their
condition in public. Reply to every review, including the bad ones, in one calm paragraph.

**3. Content must answer a question a patient is already typing.**
Not "What is Artava Kshaya." Instead: *"Periods getting lighter every month — when should you
worry?"* Each post ends with the same line: *"Full guide and references on drnidhi.net."* That is
how the audience and the backlinks both grow.

---

## Field map — what to paste where

Every CSV is keyed to the same work. Use this to translate.

| What the platform asks for | Take it from | Notes |
|---|---|---|
| Title | `Title` | Use exactly; do not shorten on Zenodo/Scholar/ORCID |
| Short description / hook | `Description (short, max 250 chars)` or the hook column | Written to be read, not skimmed |
| Abstract / full description | `Abstract` | Complete, already structured |
| Keywords / tags | `Keywords` (semicolon) or `Tags (lowercase)` (comma) | Match the platform's separator |
| Citation | `APA citation` | Also paste Vancouver where offered |
| Link / related identifier | **`Canonical open-access URL`** | Always `https://www.drnidhi.net/...` |
| File | `File to upload` | Relative to `writing/` |
| Public PDF link | `Open-access PDF (link this)` | The same PDF that is live on your site |

**The one rule:** every description ends with the canonical URL. A citation without a URL is a dead
end; a citation with one is a backlink that compounds.

---

## Routing — which work goes where

| Type | Works | Platforms |
|---|---|---|
| **M.S. dissertation** | Lashuna Kalpa & Rasnadi Taila Uttar Basti | Zenodo, ORCID, Scholar, OSF, ResearchGate, Academia, LinkedIn, Scribd |
| **Peer-reviewed articles** | Pumsavana Karma; Dinacharya & Pollution | Zenodo, ORCID, Scholar, ResearchGate, Academia, LinkedIn |
| **Conference abstracts** | Uttarbasti; Panchakarma in Vandhyatwa; Preconceptional Care; Public Health | Zenodo, ResearchGate, ORCID, Scholar, Academia |
| **Seminar presentations** | 13 decks | Zenodo, Academia, SlideShare, ORCID, Scribd |

`TRACKER.csv` expands this into all 105 individual actions, sorted by priority.

---

## Warnings — the mistakes that waste weeks

| Don't | Why |
|---|---|
| **Try to submit an article to DOAJ** | DOAJ is a directory of *journals*, not a place authors upload papers. `doaj.csv` is only useful as a checklist when choosing a journal. Submit the articles to a DOAJ-*indexed* journal instead — for example *AYU*, *Journal of Ayurveda and Integrative Medicine*, or *Journal of Research in Ayurvedic Sciences*. Confirm the journal is currently listed before you submit. |
| **Upload the thesis to Scribd without checking** | Scribd often puts uploads behind a subscription. Your open-access PDF must stay free, or the whole point is lost. Check the document as a logged-out visitor; if it is paywalled, delete it and use Zenodo. |
| **Publish the thesis everywhere before deciding on a journal** | Some journals treat a publicly deposited thesis as prior publication. If you plan to submit the dissertation to a journal, deposit it on Zenodo as a **preprint/thesis with a DOI anyway** (most journals accept this) but check that journal's policy first. |
| **Upload to any journal that emails you** | Predatory journals will find you after the first upload. Criteria: DOAJ listing, Scopus/Web of Science indexing, a real editorial board, no fee before peer review. |
| **Paste a different description on every site** | Inconsistent titles split your identity and confuse citation matching. Same title, same author string, same canonical URL. |
| **Post patient cases, before/after photos or names** | Never, even with verbal consent. The thesis PDF was checked: page 120 is a blank proforma template, no patient identifiers. Keep it that way. |
| **Buy reviews, citations or followers** | Detectable, removable, and reputationally fatal. Slow is fine. |
| **Use superlatives** ("best", "No.1", "guaranteed cure") | NMC ethics rules; also reads as advertising and lowers trust with educated patients. |
| **Upload all 20 works to all 9 platforms on day one** | You will burn out and the profiles will look spammy. Follow the sprint below. |

---

## Fourteen-day sprint

| Day | Task | Time |
|---|---|---|
| 1 | Google Business Profile: claim, complete, submit verification | 45 min |
| 2 | ORCID: register, affiliation, degrees, public visibility | 30 min |
| 3 | Zenodo: create account + API token; run the script on 3 works | 45 min |
| 4 | Zenodo: remaining 17 works; check DOIs resolve | 60 min |
| 5 | ORCID: Search & link → DataCite, import all DOIs | 20 min |
| 6 | Google Scholar: profile + first 7 works (thesis, articles, abstracts) | 60 min |
| 7 | Google Scholar: remaining 13; add PDF links | 45 min |
| 8 | ResearchGate: profile + 7 works | 60 min |
| 9 | Academia.edu: profile + first 10 works | 60 min |
| 10 | Academia.edu: remaining 10; topic tags | 45 min |
| 11 | LinkedIn: profile, publications section, first post | 45 min |
| 12 | Practo + Lybrate + Justdial listings | 60 min |
| 13 | Search Console + Bing: verify, submit sitemap; add `sameAs` to site | 45 min |
| 14 | SlideShare + Scribd (only if free download); update `TRACKER.csv` | 90 min |

Patient content is not a sprint; it is three posts a week from day 15 onwards.

---

## How you will know it is working

| Signal | Where to look | Good looks like | Realistic timing |
|---|---|---|---|
| Site indexed | Google `site:drnidhi.net` | All 22 URLs | 2–10 days |
| Scholar profile live | Google Scholar | 20 works, `[PDF]` on most | 1–2 weeks |
| DOIs resolve | `https://doi.org/<doi>` | Every one opens the Zenodo page | Same day |
| Citations appear | Scholar profile | First citation of the thesis | 6–18 months |
| Local visibility | Google Maps, incognito, "ayurvedic gynaecologist near me" | You appear in the top 3 | 4–12 weeks |
| Reviews | GBP dashboard | 15+ genuine reviews, all replied to | 3–6 months |
| Traffic | Search Console | Rising impressions on question-style queries | 4–12 weeks |
| Referral links | Search Console → Links | University, conference and journal domains | 3–12 months |

**The compounding effect:** Zenodo DOIs → ORCID → Scholar → ResearchGate → Semantic Scholar. Each
one is a machine-readable statement that these 20 works belong to one person. That is what turns a
name into an entity Google can trust, and it is what a patient finds when they check you.

---

## Do it for me — the one part I can automate

Zenodo is the only platform here with a clean public API. If you create a free account and a token,
I can deposit, describe, upload and publish all 20 works in one run, then hand back the DOIs.

1. Sign up: https://zenodo.org/signup
2. Create a token with `deposit:write` and `deposit:actions`:
   https://zenodo.org/account/settings/applications/tokens/new/
3. Run:

```powershell
$env:ZENODO_TOKEN = "paste-token-here"
py writing/upload-kit/zenodo_deposit.py --dry-run     # shows what will happen
py writing/upload-kit/zenodo_deposit.py               # creates drafts, no publishing
py writing/upload-kit/zenodo_deposit.py --publish     # publishes and mints DOIs
```

Results land in `writing/upload-kit/zenodo-dois.csv`. Paste those DOIs into `catalog.py`, rebuild,
and the site carries its own DOIs.

---

## Files in this kit

| File | Use |
|---|---|
| `MASTER-UPLOAD-PLAN.md` | This file — the route |
| `upload-console.html` | Open in a browser: every field with a copy button, per platform, with progress saved |
| `TRACKER.csv` | 105 upload actions with status columns |
| `PROFILE-COPY.md` | Bios, service descriptions, FAQs, review request scripts, post ideas |
| `zenodo_deposit.py` | Bulk deposit + DOI minting |
| `UPLOAD-GUIDE.md` | Original per-platform guide (still valid) |
| `ORDER-RECOMMENDATION.md` | Which work to upload first and why |
| `HOOKS.md` | The hook and link strategy |
| `*.csv` | Per-platform metadata, one row per work |
| `MANIFEST.json` | Everything above, machine-readable |
