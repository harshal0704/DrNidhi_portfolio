#!/usr/bin/env python3
"""Deposit all 20 works to Zenodo and mint a DOI for each.

No third-party packages — uses only the standard library.

Setup
-----
1. Create a free account:            https://zenodo.org/signup
2. Create a personal access token:   https://zenodo.org/account/settings/applications/tokens/new/
   Scopes: deposit:write and deposit:actions
3. Set it in the environment:

   PowerShell:   $env:ZENODO_TOKEN = "your-token"
   bash:         export ZENODO_TOKEN=your-token

Usage
-----
    py writing/upload-kit/zenodo_deposit.py --dry-run
    py writing/upload-kit/zenodo_deposit.py                 # create drafts only
    py writing/upload-kit/zenodo_deposit.py --publish       # publish + mint DOIs
    py writing/upload-kit/zenodo_deposit.py --publish --yes # no confirmation prompt
    py writing/upload-kit/zenodo_deposit.py --only lashuna-kalpa-rasnadi-taila-uttar-basti-artava-kshya

State is kept in `zenodo-deposits.json`, so re-running resumes instead of duplicating.
Results are written to `zenodo-dois.csv`.

Safety: nothing is published without --publish. Publishing is permanent — a published
Zenodo record cannot be deleted, only versioned.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRITING = HERE.parent
STATE_FILE = HERE / "zenodo-deposits.json"
RESULTS_FILE = HERE / "zenodo-dois.csv"

PROD = "https://zenodo.org/api"
SANDBOX = "https://sandbox.zenodo.org/api"

TYPE_MAP = {
    "Thesis": {"upload_type": "publication", "publication_type": "thesis"},
    "Article": {"upload_type": "publication", "publication_type": "article"},
    "Abstract": {"upload_type": "publication", "publication_type": "conferencepaper"},
    "Seminar": {"upload_type": "presentation"},
}


# --------------------------------------------------------------------------- http

def _multipart(fields: dict[str, str], file_field: str, path: Path) -> tuple[bytes, str]:
    boundary = "----zenodo" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields.items():
        out += f"--{boundary}\r\n".encode()
        out += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        out += str(value).encode() + b"\r\n"
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    out += f"--{boundary}\r\n".encode()
    out += f'Content-Disposition: form-data; name="{file_field}"; filename="{path.name}"\r\n'.encode()
    out += f"Content-Type: {ctype}\r\n\r\n".encode()
    out += path.read_bytes() + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def api(method: str, url: str, token: str, payload: dict | None = None,
        file_path: Path | None = None) -> dict:
    data = None
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if file_path is not None:
        data, ctype = _multipart({}, "file", file_path)
        headers["Content-Type"] = ctype
    elif payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = resp.read().decode("utf-8", "replace")
            return json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method} {url} -> HTTP {exc.code}\n{detail[:2000]}") from None


# ----------------------------------------------------------------------- metadata

def build_metadata(work: dict, orcid: str | None) -> dict:
    creators = [{"name": "Patel, Nidhi Sanjay", "affiliation": "Uka Tarsadia University"}]
    if orcid:
        creators[0]["orcid"] = orcid

    # Only the year is recorded in the catalogue; 1 January is the convention used.
    date = f"{work['year']}-01-01"

    meta = {
        "title": work["title"],
        "description": "<p>" + html.escape(work["abstract"]).replace("\n\n", "</p><p>") + "</p>",
        "creators": creators,
        "access_right": "open",
        "license": "cc-by-4.0",
        "publication_date": date,
        "keywords": work["keywords"],
        "language": "eng",
        "related_identifiers": [{
            "identifier": work["url"],
            "relation": "isIdenticalTo",
            "scheme": "url",
        }],
        "notes": "Open-access copy also available at " + work["url"],
    }
    meta.update(TYPE_MAP[work["type"]])

    if work.get("coauthors"):
        for name in work["coauthors"]:
            creators.append({"name": name, "affiliation": "Uka Tarsadia University"})
    return meta


def local_pdf(work: dict) -> Path | None:
    name = work["pdf"].rsplit("/", 1)[-1]
    for base in (WRITING / "files", HERE.parent / "files", HERE / "files"):
        candidate = base / name
        if candidate.exists():
            return candidate
    return None


# ---------------------------------------------------------------------------- run

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def write_results(state: dict, works: list[dict]) -> None:
    by_slug = {w["slug"]: w for w in works}
    fields = ["slug", "title", "doi", "doi_url", "record_url", "status", "deposition_id"]
    with RESULTS_FILE.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for slug, rec in state.items():
            work = by_slug.get(slug, {})
            writer.writerow({
                "slug": slug,
                "title": work.get("title", rec.get("title", "")),
                "doi": rec.get("doi", ""),
                "doi_url": ("https://doi.org/" + rec["doi"]) if rec.get("doi") else "",
                "record_url": rec.get("record_url", ""),
                "status": rec.get("status", "draft"),
                "deposition_id": rec.get("id", ""),
            })


def read_token(explicit: str | None, token_file: str | None) -> str | None:
    """Token from --token, --token-file, ZENODO_TOKEN, or a local .zenodo-token file."""
    if explicit:
        return explicit.strip()
    if token_file:
        return Path(token_file).read_text(encoding="utf-8").strip()
    env = os.environ.get("ZENODO_TOKEN")
    if env:
        return env.strip()
    for candidate in (HERE / ".zenodo-token", HERE.parent.parent / ".zenodo-token"):
        if candidate.exists():
            return candidate.read_text(encoding="utf-8").strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-deposit Dr. Nidhi Patel's works to Zenodo.")
    parser.add_argument("--publish", action="store_true", help="publish and mint DOIs (irreversible)")
    parser.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and exit")
    parser.add_argument("--sandbox", action="store_true", help="use sandbox.zenodo.org")
    parser.add_argument("--only", action="append", metavar="SLUG", help="limit to these slugs")
    parser.add_argument("--orcid", default=os.environ.get("ORCID_ID"), help="ORCID iD to attach")
    parser.add_argument("--token", default=None,
                        help="API token (or set ZENODO_TOKEN, or save .zenodo-token)")
    parser.add_argument("--token-file", default=None, help="path to a file containing the token")
    args = parser.parse_args()
    args.token = read_token(args.token, args.token_file)

    library = json.loads((WRITING / "library.json").read_text(encoding="utf-8"))
    works = library["works"]
    if args.only:
        wanted = set(args.only)
        works = [w for w in works if w["slug"] in wanted]
        missing = wanted - {w["slug"] for w in works}
        if missing:
            print("Unknown slug(s): " + ", ".join(sorted(missing)))
            return 2

    state = load_state()
    base = SANDBOX if args.sandbox else PROD

    todo = []
    for work in works:
        rec = state.get(work["slug"], {})
        if rec.get("status") == "published":
            continue
        pdf = local_pdf(work)
        if pdf is None:
            print(f"  ! missing PDF for {work['slug']}")
            continue
        todo.append((work, rec, pdf))

    print(f"Zenodo target : {base}")
    print(f"Works         : {len(works)} selected, {len(todo)} to process")
    print(f"Publish       : {'YES' if args.publish else 'no — drafts only'}")
    print()

    if args.dry_run:
        for work, rec, pdf in todo:
            meta = build_metadata(work, args.orcid)
            print(f"— {work['title']}")
            print(f"    type   : {meta.get('upload_type')}/{meta.get('publication_type', '-')}")
            print(f"    file   : {pdf.relative_to(WRITING.parent)} ({pdf.stat().st_size / 1_048_576:.1f} MB)")
            print(f"    related: {work['url']}")
            print(f"    keywords: {', '.join(meta['keywords'])}")
        print("\nDry run — nothing sent.")
        return 0

    if not args.token:
        print("ERROR: no token. Set ZENODO_TOKEN or pass --token.")
        return 2

    if args.publish and not args.yes:
        print("About to PUBLISH permanently and mint DOIs. This cannot be undone.")
        if sys.stdin.isatty():
            if input("Type 'publish' to continue: ").strip().lower() != "publish":
                print("Cancelled.")
                return 1
        else:
            print("Refusing to publish non-interactively without --yes.")
            return 2

    ok = failed = 0
    for index, (work, rec, pdf) in enumerate(todo, 1):
        print(f"[{index}/{len(todo)}] {work['title'][:78]}")
        try:
            if rec.get("id"):
                dep_id = rec["id"]
                print(f"    resuming deposition {dep_id}")
            else:
                created = api("POST", f"{base}/deposit/depositions", args.token, payload={})
                dep_id = created["id"]
                rec = {"id": dep_id, "status": "draft", "title": work["title"]}
                state[work["slug"]] = rec
                save_state(state)
                print(f"    created deposition {dep_id}")

            api("PUT", f"{base}/deposit/depositions/{dep_id}", args.token,
                payload={"metadata": build_metadata(work, args.orcid)})
            print("    metadata set")

            bucket = f"{base}/deposit/depositions/{dep_id}/files"
            existing = api("GET", bucket, args.token)
            names = {f.get("filename") for f in existing} if isinstance(existing, list) else set()
            if pdf.name in names:
                print(f"    {pdf.name} already on the deposition, skipping")
            else:
                api("POST", bucket, args.token, file_path=pdf)
                print(f"    uploaded {pdf.name}")

            if args.publish:
                published = api("POST", f"{base}/deposit/depositions/{dep_id}/actions/publish", args.token)
                rec["doi"] = published.get("doi") or published.get("metadata", {}).get("doi", "")
                rec["record_url"] = published.get("links", {}).get("html", "")
                rec["status"] = "published"
                save_state(state)
                print(f"    published — DOI {rec['doi']}")
            else:
                print("    draft saved (not published)")
            ok += 1
        except Exception as exc:  # noqa: BLE001 - report and continue
            failed += 1
            print(f"    FAILED: {exc}")
        time.sleep(0.4)

    write_results(state, library["works"])
    print(f"\nDone: {ok} ok, {failed} failed. Results: {RESULTS_FILE.name}")
    if args.publish:
        print("Next: add these DOIs to catalog.py, rebuild, and paste them into ORCID / Scholar.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
