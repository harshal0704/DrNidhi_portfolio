#!/usr/bin/env python3
"""Regenerate the writing pages, library.json, sitemap, robots and RSS.

This is the same as build.py minus two expensive steps:
  * it does not copy the source documents out of newdata/
  * it does not re-render the 20 PDFs with headless Chrome

Use it after a metadata-only change (titles, DOIs, citations). Use build.py when the
PDFs themselves need to be regenerated.

    py writing/build_pages.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build  # noqa: E402
from catalog import WORKS  # noqa: E402


def attach_source_ext() -> None:
    for w in WORKS:
        matches = glob.glob(os.path.join(build.FILES, f"{w['slug']}-source.*"))
        w["source_ext"] = os.path.splitext(matches[0])[1].lstrip(".") if matches else "pdf"


def main() -> None:
    attach_source_ext()

    print("writing pages...")
    with open(os.path.join(build.PUB, "index.html"), "w", encoding="utf-8") as f:
        f.write(build.render_index())
    for w in WORKS:
        with open(os.path.join(build.PUB, f"{w['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(build.render_work_page(w))

    build.build_library_json()
    print("  library.json written")

    print("  index patched" if build.patch_index() else "  index already current")

    n = build.build_sitemap()
    build.build_robots()
    build.build_rss()
    print(f"  sitemap: {n} urls | robots.txt + rss.xml written")
    print("done.")


if __name__ == "__main__":
    main()
