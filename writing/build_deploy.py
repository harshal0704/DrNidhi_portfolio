# -*- coding: utf-8 -*-
"""
Builds a ready-to-upload package for the InfinityFree web host that serves
drnidhi.great-site.net.

The live site is hosted on InfinityFree (great-site.net is InfinityFree's free
domain), not on GitHub Pages — so the files have to be copied into the account's
web root. This produces a clean folder tree and a zip that can be dropped in.

    deploy/                 <- copy the CONTENTS of this into the web root
    deploy/DrNidhi_deploy.zip
    deploy/DEPLOY.md
"""
import os, shutil, zipfile, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from catalog import WORKS

ROOT = r"C:\Users\nidhi\harshal\DrNidhi_portfolio"
OUT = os.path.join(ROOT, "deploy")
STAGE = os.path.join(OUT, "site")

ROOT_FILES = ["index.html", "style.css", "script.js", "robots.txt", "rss.xml", "sitemap.xml",
              "1.png", "dr-nidhi-patel-profile.jpg", "web.png"]
SKIP_DIRS = {"print", "upload-kit", "__pycache__"}


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


DEPLOY_MD = r"""# Deploying to drnidhi.great-site.net

`drnidhi.great-site.net` is free shared hosting provided by **InfinityFree** (the
`great-site.net` domain belongs to InfinityFree). It is *not* served from GitHub Pages,
so pushing to GitHub does not change the live site — the files have to be copied into the
hosting account's web root.

## What to upload

Everything in the `site/` folder next to this file. Its contents are the finished site:

```
site/
├── index.html                     home page (now includes the Publications block)
├── style.css
├── script.js
├── robots.txt                     allows search, AI and academic crawlers
├── rss.xml                        RSS feed of the publication record
├── sitemap.xml                    22 URLs
├── 1.png, dr-nidhi-patel-profile.jpg, web.png
└── writing/
    ├── index.html                 searchable catalogue
    ├── library.json               machine-readable catalogue
    ├── <slug>.html                20 work pages
    ├── assets/                    pub.css, pub.js
    └── files/                     open-access PDFs + the original documents
```

(`writing/print/` and `writing/upload-kit/` are deliberately left out — they are
build and working files, not web content.)

## How to upload — choose one

### Option A — the InfinityFree control panel (easiest)

1. Sign in at <https://dash.infinityfree.com>.
2. Open **Control Panel → Website → File Manager** (or the online file manager / FTP link).
3. Open the web root — usually `htdocs`.
4. Upload the contents of `site/`. Two ways:
   - upload `DrNidhi_deploy.zip`, then right-click it in the file manager and choose **Extract**; or
   - upload the folders and files individually, keeping the same names.
5. Confirm the file names are exactly `index.html` (not `index.html.txt`) — Windows
   Notepad and some browsers add `.txt`. Delete any stray `.txt` duplicates.
6. Visit <https://drnidhi.great-site.net/> and <https://drnidhi.great-site.net/writing/>.

### Option B — FTP (fastest for ~25 MB)

InfinityFree gives FTP details on the control panel under **Account → FTP Accounts**.

```powershell
# from the folder that contains `site\`
curl.exe --ftp-create-dirs -T "site\index.html"            ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/index.html
curl.exe --ftp-create-dirs -T "site\style.css"             ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/style.css
curl.exe --ftp-create-dirs -T "site\script.js"             ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/script.js
curl.exe --ftp-create-dirs -T "site\robots.txt"            ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/robots.txt
curl.exe --ftp-create-dirs -T "site\rss.xml"               ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/rss.xml
curl.exe --ftp-create-dirs -T "site\sitemap.xml"           ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/sitemap.xml
curl.exe --ftp-create-dirs -T "site\1.png"                 ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/1.png
curl.exe --ftp-create-dirs -T "site\dr-nidhi-patel-profile.jpg" ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/dr-nidhi-patel-profile.jpg
curl.exe --ftp-create-dirs -T "site\web.png"               ftp://YOURUSER:YOURPASSWORD@ftp.infinityfree.com/htdocs/web.png
```

Then the `publications` folder — upload the tree with any FTP client (FileZilla, WinSCP),
because there are 60+ files:

```powershell
# from inside site\
lftp -u YOURUSER,YOURPASSWORD ftp.infinityfree.com -e "mirror -R publications /htdocs/publications; bye"
```

Or with WinSCP: protocol **FTP**, host **ftp.infinityfree.com**, port **21**, log in with the
FTP account from the control panel, drag `site\\publications` into `/htdocs/`.

## After the upload — the six things that make it work

1. **Test every URL** — the home page, `/writing/`, one work page, and one PDF:
   ```
   https://drnidhi.great-site.net/
   https://drnidhi.great-site.net/writing/
   https://drnidhi.great-site.net/writing/lashuna-kalpa-rasnadi-taila-uttar-basti-artava-kshya.html
   https://drnidhi.great-site.net/writing/library.json
   https://drnidhi.great-site.net/writing/files/vomiting-in-pregnancy.pdf
   ```
2. **Submit the sitemap** in Google Search Console → Sitemaps →
   `https://drnidhi.great-site.net/sitemap.xml`
3. **Check the structured data** at <https://search.google.com/test/rich-results> — every
   work page should report as an academic article with no errors.
4. **Tell Google the domain changed nothing** — the canonical URLs in the pages already
   point at `https://drnidhi.great-site.net/`, so no redirects are needed.
5. **Post the URL** in the university department page, on LinkedIn, and on WhatsApp status.
6. **Upload the same PDFs to ResearchGate, Academia.edu and Zenodo** using
   `writing/upload-kit/` — and put the canonical URL in every description, so each
   upload points back here.

## A note on the same content being live in two places

The same site is also published on GitHub Pages at
<https://harshalsp07.github.io/DrNidhi_portfolio/>. That copy is useful as a fallback and
as a second indexable surface, but the canonical URLs on every page point at
`drnidhi.great-site.net`, so search engines will treat that as the single authoritative
copy and will not treat the two as duplicates.
"""


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(STAGE, exist_ok=True)

    for f in ROOT_FILES:
        s = os.path.join(ROOT, f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(STAGE, f))
        else:
            print("  (skipped, not found:", f, ")")

    copy_tree(os.path.join(ROOT, "writing"), os.path.join(STAGE, "writing"), skip=SKIP_DIRS)

    with open(os.path.join(OUT, "DEPLOY.md"), "w", encoding="utf-8") as f:
        f.write(DEPLOY_MD)

    zp = os.path.join(OUT, "DrNidhi_deploy.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(STAGE):
            for n in fn:
                p = os.path.join(dp, n)
                z.write(p, os.path.relpath(p, STAGE))

    n = sum(len(fn) for _, _, fn in os.walk(STAGE))
    size = sum(os.path.getsize(os.path.join(dp, n2)) for dp, _, fn in os.walk(STAGE) for n2 in fn)
    print(f"deploy package: {n} files, {size/1024/1024:.1f} MB")
    print(f"  folder : {OUT}\\site")
    print(f"  zip    : {zp}")
    print(f"  guide  : {OUT}\\DEPLOY.md")


if __name__ == "__main__":
    main()
