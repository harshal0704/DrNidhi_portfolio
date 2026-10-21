# -*- coding: utf-8 -*-
"""
Validates the generated publications site.

Checks: JSON-LD validity, tag balance, internal link targets, XML well-formedness,
catalogue consistency, PDF presence, and that every work has the metadata a platform needs.

    py writing/verify.py
"""
import os, re, json, sys, glob
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from catalog import WORKS, AUTHOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "writing")
FILES = os.path.join(PUB, "files")
SITE = "https://drnidhi.great-site.net"

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_html(path):
    src = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, ROOT)
    for i, b in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)):
        try:
            json.loads(b)
        except Exception as e:
            err(f"{rel}: JSON-LD block {i} invalid: {e}")
    for tag in ("section", "article", "div", "table", "ul", "nav", "main", "body", "html"):
        o = len(re.findall(rf"<{tag}[\s>]", src))
        c = len(re.findall(rf"</{tag}>", src))
        if o != c:
            err(f"{rel}: <{tag}> imbalance open={o} close={c}")
    for m in re.finditer(r'(?:href|src)="([^"#]+)"', src):
        t = m.group(1).split("?")[0]
        if t.startswith(("http", "mailto:", "tel:", "data:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), t))
        if not os.path.exists(target):
            err(f"{rel}: broken local link -> {t}")
    if "<title>" not in src:
        err(f"{rel}: no <title>")
    if 'name="description"' not in src:
        err(f"{rel}: no meta description")
    if 'rel="canonical"' not in src:
        err(f"{rel}: no canonical link")
    if 'name="twitter:card"' not in src:
        warn(f"{rel}: no twitter:card")
    return src


def main():
    print("== checking html ==")
    pages = [os.path.join(ROOT, "index.html"), os.path.join(PUB, "index.html")]
    for w in WORKS:
        pages.append(os.path.join(PUB, f"{w['slug']}.html"))
    for p in pages:
        if not os.path.exists(p):
            err(f"missing page {os.path.relpath(p, ROOT)}")
            continue
        check_html(p)
    print(f"   {len(pages)} pages checked")

    print("== checking xml ==")
    for x in ("sitemap.xml", "rss.xml"):
        fp = os.path.join(ROOT, x)
        if not os.path.exists(fp):
            err(f"missing {x}")
            continue
        try:
            ET.parse(fp)
            print(f"   {x} well-formed")
        except Exception as e:
            err(f"{x}: {e}")

    print("== checking catalogue ==")
    lib_p = os.path.join(PUB, "library.json")
    if not os.path.exists(lib_p):
        err("missing writing/library.json")
    else:
        lib = json.load(open(lib_p, encoding="utf-8"))
        if lib["count"] != len(WORKS) or len(lib["works"]) != len(WORKS):
            err(f"library.json count mismatch: {lib['count']} / {len(lib['works'])} vs {len(WORKS)}")
        for w in lib["works"]:
            for f in ("title", "abstract", "keywords", "url", "pdf", "citations"):
                if not w.get(f):
                    err(f"library.json: {w['slug']} missing {f}")
        print(f"   {len(lib['works'])} works in catalogue")

    print("== checking files ==")
    for w in WORKS:
        for f in (f"{w['slug']}.pdf", f"{w['slug']}-source.pdf", f"{w['slug']}-source.docx",
                  f"{w['slug']}-source.pptx"):
            p = os.path.join(FILES, f)
            if os.path.exists(p) and os.path.getsize(p) < 500:
                err(f"suspiciously small file: {f}")
    n_pdf = len(glob.glob(os.path.join(FILES, "*.pdf")))
    n_src = len(glob.glob(os.path.join(FILES, "*-source.*")))
    print(f"   {n_pdf} pdf, {n_src} source files")
    for w in WORKS:
        if not os.path.exists(os.path.join(FILES, f"{w['slug']}.pdf")):
            err(f"missing open-access PDF for {w['slug']}")

    print("== checking upload kit ==")
    kit = os.path.join(PUB, "upload-kit")
    for f in ("MANIFEST.json", "UPLOAD-GUIDE.md", "ORDER-RECOMMENDATION.md", "HOOKS.md",
              "researchgate.csv", "academia.csv", "scribd.csv", "slideshare.csv",
              "zenodo.csv", "osf.csv", "scholar.csv", "doaj.csv"):
        p = os.path.join(kit, f)
        if not os.path.exists(p) or os.path.getsize(p) < 100:
            err(f"upload kit: missing or empty {f}")
    print("   kit files present")

    print("== checking sitemap coverage ==")
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    for w in WORKS:
        if f"/writing/{w['slug']}.html" not in sm:
            err(f"sitemap missing {w['slug']}")
    if "/writing/" not in sm:
        err("sitemap missing publications index")

    print()
    print(f"ERRORS: {len(errors)}")
    for e in errors:
        print("  ✗", e)
    print(f"WARNINGS: {len(warnings)}")
    for w_ in warnings:
        print("  !", w_)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
