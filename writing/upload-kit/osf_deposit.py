#!/usr/bin/env python3
"""Create an OSF project and upload all 20 works to it.

Standard library only. OSF's API is a JSON:API; files are uploaded to Waterbutler.

Setup
-----
1. Sign in / register:  https://osf.io/register
2. Create a token:      https://osf.io/settings/tokens
   Scopes: osf.full_write
3. Save it to `.osf-token` in the repository root (git-ignored), or set OSF_TOKEN.

Usage
-----
    py writing/upload-kit/osf_deposit.py --dry-run
    py writing/upload-kit/osf_deposit.py                 # private project, uploads
    py writing/upload-kit/osf_deposit.py --publish       # make it public
    py writing/upload-kit/osf_deposit.py --publish --yes # no prompt

Nothing is made public without --publish. Re-running resumes: the node id is kept in
`osf-project.json` and files already present are skipped.

Results are written to `osf-project.json` and printed at the end.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRITING = HERE.parent
STATE_FILE = HERE / "osf-project.json"
API = "https://api.osf.io/v2"

PROJECT_TITLE = "Dr. Nidhi Patel — Ayurvedic women's health: publications, thesis and data"
PROJECT_DESC = (
    "Open-access collection of the academic work of Dr. Nidhi Patel (B.A.M.S., M.S. Ayurveda — "
    "Prasuti Tantra & Stree Roga), Assistant Professor at Uka Tarsadia University, Bardoli, Gujarat. "
    "The collection includes the M.S. dissertation on Lashuna Kalpa and Rasnadi Taila Uttar Basti in "
    "Artava Kshaya, two peer-reviewed articles, four conference abstracts and thirteen seminar "
    "presentations. Every work is also published on Zenodo with a DOI and on the author's site at "
    "https://www.drnidhi.net. Licence: CC BY 4.0."
)


# --------------------------------------------------------------------------- http

def _request(method: str, url: str, token: str, *, body: bytes | None = None,
             content_type: str = "application/json", timeout: int = 180):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        return exc.code, {"error": raw[:2000]}


def api(method: str, path: str, token: str, payload: dict | None = None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    return _request(method, API + path, token, body=body,
                    content_type="application/vnd.api+json")


def upload_file(url: str, token: str, path: Path):
    return _request("PUT", url, token, body=path.read_bytes(),
                    content_type="application/pdf")


# ----------------------------------------------------------------------- helpers

def read_token(explicit: str | None, token_file: str | None) -> str | None:
    if explicit:
        return explicit.strip()
    if token_file:
        return Path(token_file).read_text(encoding="utf-8").strip()
    env = os.environ.get("OSF_TOKEN")
    if env:
        return env.strip()
    for candidate in (HERE / ".osf-token", HERE.parent.parent / ".osf-token"):
        if candidate.exists():
            return candidate.read_text(encoding="utf-8").strip()
    return None


def local_pdf(work: dict) -> Path | None:
    name = work["pdf"].rsplit("/", 1)[-1]
    candidate = WRITING / "files" / name
    return candidate if candidate.exists() else None


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def create_project(token: str) -> dict:
    status, data = api("POST", "/nodes/", token, {
        "data": {
            "type": "nodes",
            "attributes": {
                "title": PROJECT_TITLE,
                "description": PROJECT_DESC,
                "category": "project",
                "public": False,
            },
        }
    })
    if status not in (200, 201):
        raise RuntimeError(f"create project failed ({status}): {data.get('error', data)}")
    node = data["data"]
    return {"id": node["id"], "url": node.get("links", {}).get("html", ""), "files": {}}


def upload_root(node_id: str, token: str) -> str:
    status, data = api("GET", f"/nodes/{node_id}/files/", token)
    if status != 200:
        raise RuntimeError(f"cannot list storage ({status}): {data.get('error', data)}")
    providers = data.get("data", [])
    if not providers:
        raise RuntimeError("no storage provider on this project")
    return providers[0]["links"]["upload"]


def existing_files(node_id: str, token: str) -> set[str]:
    status, data = api("GET", f"/nodes/{node_id}/files/osfstorage/?page[size]=100", token)
    if status != 200:
        return set()
    return {f["attributes"]["name"] for f in data.get("data", [])
            if f.get("attributes", {}).get("kind") == "file"}


# ---------------------------------------------------------------------------- run

def main() -> int:
    parser = argparse.ArgumentParser(description="Upload all works to an OSF project.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--publish", action="store_true", help="make the project public")
    parser.add_argument("--yes", action="store_true", help="skip confirmation")
    parser.add_argument("--only", action="append", metavar="SLUG")
    parser.add_argument("--token")
    parser.add_argument("--token-file")
    args = parser.parse_args()

    token = read_token(args.token, args.token_file)
    works = json.loads((WRITING / "library.json").read_text(encoding="utf-8"))["works"]
    if args.only:
        wanted = set(args.only)
        works = [w for w in works if w["slug"] in wanted]

    missing = [w["slug"] for w in works if local_pdf(w) is None]
    if missing:
        print("missing PDF for: " + ", ".join(missing))
        return 2

    print(f"OSF project : {PROJECT_TITLE}")
    print(f"Works       : {len(works)}")
    print(f"Publish     : {'YES — public' if args.publish else 'no — private project'}")
    print()

    if args.dry_run:
        for i, w in enumerate(works, 1):
            print(f"{i:>2}. {w['title'][:82]:<82} {w['doi']}")
        print("\nDry run — nothing sent.")
        return 0

    if not token:
        print("ERROR: no token. Set OSF_TOKEN or pass --token / --token-file.")
        return 2

    if args.publish and not args.yes:
        print("About to make the OSF project PUBLIC. Anyone will be able to read and download it.")
        if sys.stdin.isatty():
            if input("Type 'publish' to continue: ").strip().lower() != "publish":
                print("Cancelled.")
                return 1
        else:
            print("Refusing to publish non-interactively without --yes.")
            return 2

    state = load_state()
    try:
        if not state.get("id"):
            state = create_project(token)
            save_state(state)
            print(f"created project {state['id']} — {state['url']}")
        else:
            print(f"resuming project {state['id']} — {state['url']}")

        root = upload_root(state["id"], token)
        already = existing_files(state["id"], token)

        ok = skipped = failed = 0
        for i, w in enumerate(works, 1):
            pdf = local_pdf(w)
            name = pdf.name
            print(f"[{i}/{len(works)}] {name}")
            if name in already:
                print("    already uploaded, skipping")
                skipped += 1
                continue
            status, data = upload_file(f"{root}?kind=file&name={urllib.parse.quote(name)}",
                                       token, pdf)
            if status in (200, 201):
                link = data.get("data", {}).get("links", {}).get("download", "")
                state["files"][w["slug"]] = {"name": name, "download": link}
                save_state(state)
                print("    uploaded")
                ok += 1
            else:
                print(f"    FAILED ({status}): {str(data.get('error', data))[:300]}")
                failed += 1
            time.sleep(0.2)

        if args.publish:
            status, data = api("PATCH", f"/nodes/{state['id']}/", token, {
                "data": {"id": state["id"], "type": "nodes", "attributes": {"public": True}}
            })
            if status in (200, 201):
                state["public"] = True
                save_state(state)
                print(f"\nproject is public: {state['url']}")
            else:
                print(f"\ncould not make public ({status}): {str(data.get('error', data))[:400]}")
                print("You can toggle it in the OSF web UI: Project settings -> Make public.")

        print(f"\nDone: {ok} uploaded, {skipped} skipped, {failed} failed.")
        print(f"Project: {state.get('url')}")
        print(f"State:   {STATE_FILE.name}")
        return 0 if failed == 0 else 1
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
