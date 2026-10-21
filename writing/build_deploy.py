# -*- coding: utf-8 -*-
"""
Writes the deployment guide, and optionally a portable bundle.

The site is a static document set served from **https://www.drnidhi.net**.
It deploys from this repository (Vercel watches the default branch), so pushing
is the deploy — there is nothing to copy by hand.

    py writing/build_deploy.py          # refresh deploy/DEPLOY.md only
    py writing/build_deploy.py --zip    # also build deploy/site + DrNidhi_deploy.zip

The zip is a build artefact for offline copies and never needs to be committed.
The old InfinityFree host (drnidhi.great-site.net) is retired; its instructions
were removed because the host no longer answers.
"""
import os, shutil, zipfile, sys

ROOT = r"C:\Users\nidhi\harshal\DrNidhi_portfolio"
OUT = os.path.join(ROOT, "deploy")
STAGE = os.path.join(OUT, "site")

ROOT_FILES = ["index.html", "style.css", "script.js", "robots.txt", "rss.xml", "sitemap.xml",
              "1.png", "dr-nidhi-patel-profile.jpg", "web.png"]
SKIP_DIRS = {"print", "upload-kit", "__pycache__"}

SITE = "https://www.drnidhi.net"


def copy_tree(src, dst, skip=()):
    for dp, dn, fn in os.walk(src):
        rel = os.path.relpath(dp, src)
        parts = [] if rel == "." else rel.split(os.sep)
        if any(p in skip for p in parts):
            dn[:] = []
            continue
        target = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(target, exist_ok=True)
        dn[:] = [d for d in dn if d not in skip]
        for n in fn:
            if n.endswith(".pyc") or n.startswith("_"):
                continue
            shutil.copy2(os.path.join(dp, n), os.path.join(target, n))


DEPLOY_MD = r"""# Deploying drnidhi.net

The site is static HTML, CSS and JavaScript. It is served at
**https://www.drnidhi.net** by **Vercel**, which builds from this repository on
every push to the default branch.

**Pushing is the deploy.** There is no file manager, no FTP, no zip to copy.
The old InfinityFree host (`drnidhi.great-site.net`) is retired — it no longer
answers, and every canonical URL now points at `www.drnidhi.net`.

## What makes up the site

```
index.html                  home page (hero, about, note, services, journey, publications, FAQ, contact)
style.css                   all site styles
script.js                   nav, scroll reveal, compass, dinacharya tabs, FAQ
robots.txt                  allows search, AI and academic crawlers
sitemap.xml                 22 URLs
rss.xml                     RSS feed of the publication record
1.png, dr-nidhi-patel-profile.jpg, web.png
writing/                    the publications sub-site
    index.html              searchable, filterable catalogue
    library.json            machine-readable catalogue of all 20 works
    <slug>.html             one page per work (20)
    assets/                 pub.css, pub.js
    files/                  open-access PDFs + the original documents
```

`writing/print/` and `writing/upload-kit/` are build and working files. They stay
in the repository but are not part of the public site.

## The deploy

1. `git push` the default branch.
2. Vercel builds and promotes the deployment automatically (roughly 30 seconds).
3. Open <https://www.drnidhi.net/> and hard-refresh once to clear the old CSS.

If a push does not appear live, check the Vercel dashboard for the project's
latest deployment — a failed build is almost always a missing file, not a
hosting problem.

## DNS

`drnidhi.net` and `www.drnidhi.net` both point at Vercel:

| Record | Name | Value |
|---|---|---|
| A | `@` | the two Vercel apex addresses shown in the dashboard |
| CNAME | `www` | `cname.vercel-dns.com` |

The apex redirects to `www`, which is the canonical host used by every page's
`<link rel="canonical">`, the sitemap and the RSS feed.

## After a deploy — the check list

1. Every URL below returns 200:

   ```
   https://www.drnidhi.net/
   https://www.drnidhi.net/writing/
   https://www.drnidhi.net/writing/lashuna-kalpa-rasnadi-taila-uttar-basti-artava-kshya.html
   https://www.drnidhi.net/writing/library.json
   https://www.drnidhi.net/writing/files/vomiting-in-pregnancy.pdf
   https://www.drnidhi.net/sitemap.xml
   https://www.drnidhi.net/rss.xml
   ```

2. The **Writing** tab in the header opens `/writing/` (it is the only nav link
   that leaves the home page).
3. `py writing/verify.py` reports **0 errors**.
4. Submit `sitemap.xml` once in Google Search Console → Sitemaps.
5. Check one work page at <https://search.google.com/test/rich-results> — it
   should report a scholarly article with no errors.

## What must never be committed

- `newdata/` — 7.2 GB of original source documents.
- `.zenodo-token`, `.osf-token`, `.env` — API credentials.

Both are already covered by `.gitignore`. The upload kit needs the tokens at run
time; it reads them from those files and never writes them into the site.

## Publishing the same works elsewhere

`writing/upload-kit/` holds every field for every platform, already written to
point back at `https://www.drnidhi.net`. Start with
`writing/upload-kit/MASTER-UPLOAD-PLAN.md`, then use `upload-console.html` to
click-to-copy each field. The rule is simple: wherever a work is uploaded, the
description ends with its canonical `www.drnidhi.net/writing/...` URL, so every
copy cites the original.
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "DEPLOY.md"), "w", encoding="utf-8") as f:
        f.write(DEPLOY_MD)
    print("guide  :", os.path.join(OUT, "DEPLOY.md"))

    if "--zip" not in sys.argv:
        print("bundle : skipped (pass --zip to build deploy/site + DrNidhi_deploy.zip)")
        return

    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE, exist_ok=True)

    for f in ROOT_FILES:
        s = os.path.join(ROOT, f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(STAGE, f))
        else:
            print("  (skipped, not found:", f, ")")

    copy_tree(os.path.join(ROOT, "writing"), os.path.join(STAGE, "writing"), skip=SKIP_DIRS)

    zp = os.path.join(OUT, "DrNidhi_deploy.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(STAGE):
            for n in fn:
                p = os.path.join(dp, n)
                z.write(p, os.path.relpath(p, STAGE))

    n = sum(len(fn) for _, _, fn in os.walk(STAGE))
    size = sum(os.path.getsize(os.path.join(dp, n2)) for dp, _, fn in os.walk(STAGE) for n2 in fn)
    print(f"bundle : {n} files, {size/1024/1024:.1f} MB")
    print(f"  folder : {STAGE}")
    print(f"  zip    : {zp}")


if __name__ == "__main__":
    main()
