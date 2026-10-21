#!/usr/bin/env python3
"""Generate the upload console (upload-console.html) and TRACKER.csv.

Reads writing/library.json and writes:
  writing/upload-kit/upload-console.html
  writing/upload-kit/TRACKER.csv

Run from the repository root:
  py writing/build_console.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KIT = ROOT / "upload-kit"

# platform key -> (label, upload page, field note)
PLATFORMS = {
    "orcid": ("ORCID", "https://orcid.org/my-orcid", "Works -> Add works -> Add manually"),
    "scholar": ("Google Scholar", "https://scholar.google.com/citations?view_op=new_profile", "Profile -> Add article manually"),
    "zenodo": ("Zenodo", "https://zenodo.org/uploads/new", "New upload -> paste metadata -> upload PDF -> Publish"),
    "osf": ("OSF", "https://osf.io/dashboard", "Create project -> add components -> upload files"),
    "researchgate": ("ResearchGate", "https://www.researchgate.net/", "Add new -> Publication / Conference paper"),
    "academia": ("Academia.edu", "https://www.academia.edu/upload", "Upload -> Research"),
    "scribd": ("Scribd", "https://www.scribd.com/upload", "Upload -> set free download + CC BY 4.0"),
    "slideshare": ("SlideShare", "https://www.slideshare.net/upload", "Upload -> use the hook as the description"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com/feed/", "Profile -> Add section -> Publications"),
}

# works by type -> ordered platform list with priority
PLAN = {
    "Thesis": [("zenodo", 1), ("orcid", 1), ("scholar", 1), ("osf", 1),
               ("researchgate", 1), ("academia", 2), ("linkedin", 2), ("scribd", 3)],
    "Article": [("zenodo", 1), ("orcid", 1), ("scholar", 1), ("researchgate", 1),
                ("academia", 2), ("linkedin", 2)],
    "Abstract": [("zenodo", 1), ("researchgate", 1), ("orcid", 2), ("scholar", 2), ("academia", 2)],
    "Seminar": [("zenodo", 2), ("academia", 2), ("slideshare", 2), ("orcid", 3), ("scribd", 3)],
}


def load_works() -> list[dict]:
    data = json.loads((ROOT / "library.json").read_text(encoding="utf-8"))
    return data["works"]


def build_tracker(works: list[dict]) -> None:
    fields = [
        "Priority", "Platform", "Work", "Type", "Year", "Upload file", "Upload page",
        "Title", "Short description / hook", "Canonical URL", "Status",
        "Public URL (after upload)", "DOI", "Date uploaded", "Notes",
    ]
    rows = []
    for work in works:
        for key, priority in PLAN.get(work["type"], []):
            label, upload_page, note = PLATFORMS[key]
            rows.append({
                "Priority": priority,
                "Platform": label,
                "Work": work["title"],
                "Type": work["typeLabel"],
                "Year": work["year"],
                "Upload file": work["pdf"].split("drnidhi.net/", 1)[-1],
                "Upload page": upload_page,
                "Title": work["title"],
                "Short description / hook": work["hook"],
                "Canonical URL": work["url"],
                "Status": "Not started",
                "Public URL (after upload)": "",
                "DOI": "",
                "Date uploaded": "",
                "Notes": note,
            })
    rows.sort(key=lambda r: (r["Priority"], r["Platform"], r["Work"]))
    with (KIT / "TRACKER.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"TRACKER.csv: {len(rows)} rows")


def build_console(works: list[dict]) -> None:
    payload = []
    for work in works:
        payload.append({
            "slug": work["slug"],
            "type": work["type"],
            "typeLabel": work["typeLabel"],
            "title": work["title"],
            "hook": work["hook"],
            "abstract": work["abstract"],
            "keywords": "; ".join(work["keywords"]),
            "year": work["year"],
            "url": work["url"],
            "pdf": work["pdf"],
            "source": work["source"],
            "apa": work["citations"]["apa"],
            "vancouver": work["citations"]["vancouver"],
            "bibtex": work["citations"]["bibtex"],
            "platforms": [{"key": k, "priority": p} for k, p in PLAN.get(work["type"], [])],
        })

    platforms_json = json.dumps({k: {"label": v[0], "url": v[1], "note": v[2]} for k, v in PLATFORMS.items()}, ensure_ascii=False)
    works_json = json.dumps(payload, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Upload console — Dr. Nidhi Patel</title>
<style>
  :root {{
    --bg:#0f1419; --panel:#161d26; --panel2:#1d2733; --line:#2a3644;
    --ink:#e8eef6; --muted:#93a4b8; --accent:#5cc8a1; --accent2:#f0b46a;
    --done:#2f6b55;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    background:var(--bg); color:var(--ink); }}
  header {{ position:sticky; top:0; z-index:5; background:rgba(15,20,25,.96);
    border-bottom:1px solid var(--line); padding:16px 22px; backdrop-filter:blur(8px); }}
  h1 {{ margin:0 0 4px; font-size:19px; letter-spacing:-.01em; }}
  .sub {{ color:var(--muted); font-size:13px; }}
  .bar {{ height:6px; background:var(--panel2); border-radius:99px; margin-top:12px; overflow:hidden; }}
  .bar > i {{ display:block; height:100%; width:0; background:linear-gradient(90deg,var(--accent),var(--accent2)); transition:width .3s; }}
  .stats {{ display:flex; gap:18px; flex-wrap:wrap; margin-top:8px; font-size:12.5px; color:var(--muted); }}
  .stats b {{ color:var(--ink); }}
  .wrap {{ display:grid; grid-template-columns:220px 1fr; gap:0; align-items:start; }}
  nav {{ position:sticky; top:110px; padding:18px 12px; border-right:1px solid var(--line); min-height:calc(100vh - 110px); }}
  nav button {{ display:flex; justify-content:space-between; gap:8px; width:100%; text-align:left;
    background:none; border:1px solid transparent; color:var(--muted); padding:9px 11px; border-radius:9px;
    cursor:pointer; font-size:13.5px; margin-bottom:3px; font-family:inherit; }}
  nav button:hover {{ background:var(--panel); color:var(--ink); }}
  nav button.on {{ background:var(--panel2); color:var(--ink); border-color:var(--line); }}
  nav button span {{ color:var(--muted); font-variant-numeric:tabular-nums; font-size:12px; }}
  main {{ padding:22px; max-width:1050px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin-bottom:14px; }}
  .card.done {{ border-color:var(--done); background:#141f1b; }}
  .top {{ display:flex; gap:11px; align-items:flex-start; }}
  .top input {{ margin-top:3px; width:17px; height:17px; accent-color:var(--accent); flex:none; cursor:pointer; }}
  .badge {{ display:inline-block; font-size:11px; text-transform:uppercase; letter-spacing:.06em;
    color:var(--accent2); border:1px solid #3a3025; background:#241d14; padding:1px 7px; border-radius:99px; }}
  .ttl {{ font-weight:650; font-size:15.5px; line-height:1.35; margin:6px 0 0; }}
  .hook {{ color:var(--muted); font-size:13.5px; margin:6px 0 0; }}
  .fields {{ margin-top:14px; display:grid; gap:8px; }}
  .field {{ background:var(--panel2); border:1px solid var(--line); border-radius:9px; padding:9px 11px; }}
  .field .lbl {{ display:flex; justify-content:space-between; align-items:center; gap:10px;
    font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); margin-bottom:5px; }}
  .field .val {{ font-size:13px; color:#cbd8e6; max-height:74px; overflow:auto; white-space:pre-wrap; word-break:break-word; }}
  .copy {{ background:#27333f; color:var(--ink); border:1px solid #364656; border-radius:6px;
    font-size:11px; padding:3px 9px; cursor:pointer; font-family:inherit; }}
  .copy:hover {{ background:#31414f; }}
  .copy.ok {{ background:var(--done); border-color:var(--done); }}
  .links {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:12px; font-size:12.5px; }}
  .links a {{ color:var(--accent); text-decoration:none; }}
  .links a:hover {{ text-decoration:underline; }}
  .empty {{ color:var(--muted); padding:40px; text-align:center; }}
  .tip {{ background:#1b232c; border:1px solid var(--line); border-left:3px solid var(--accent);
    padding:12px 15px; border-radius:0 10px 10px 0; color:var(--muted); font-size:13px; margin-bottom:18px; }}
  @media (max-width:760px) {{
    .wrap {{ grid-template-columns:1fr; }}
    nav {{ position:static; display:flex; overflow-x:auto; border-right:0; border-bottom:1px solid var(--line);
      min-height:0; padding:10px; gap:6px; }}
    nav button {{ width:auto; white-space:nowrap; margin:0; }}
    main {{ padding:14px; }}
  }}
</style>
</head>
<body>
<header>
  <h1>Upload console — Dr. Nidhi Patel</h1>
  <div class="sub">Every field pre-written. Click a copy button, paste it on the platform, tick the box. Canonical site: <b>https://www.drnidhi.net</b></div>
  <div class="bar"><i id="bar"></i></div>
  <div class="stats">
    <span><b id="doneCount">0</b> done</span>
    <span><b id="totalCount">0</b> uploads</span>
    <span><b id="pct">0%</b> complete</span>
    <span style="margin-left:auto"><a href="#" id="reset" style="color:#93a4b8">reset progress</a></span>
  </div>
</header>
<div class="wrap">
  <nav id="nav"></nav>
  <main id="main"></main>
</div>
<script>
const PLATFORMS = {platforms_json};
const WORKS = {works_json};
const KEY = 'drnidhi-upload-progress-v1';
let state = JSON.parse(localStorage.getItem(KEY) || '{{}}');
let current = 'all';

function save() {{ localStorage.setItem(KEY, JSON.stringify(state)); renderStats(); }}
function id(slug, p) {{ return slug + '::' + p; }}
function isDone(slug, p) {{ return !!state[id(slug, p)]; }}

function renderStats() {{
  let total = 0, done = 0;
  WORKS.forEach(w => w.platforms.forEach(p => {{ total++; if (isDone(w.slug, p.key)) done++; }}));
  document.getElementById('totalCount').textContent = total;
  document.getElementById('doneCount').textContent = done;
  const pct = total ? Math.round(done / total * 100) : 0;
  document.getElementById('pct').textContent = pct + '%';
  document.getElementById('bar').style.width = pct + '%';
  document.querySelectorAll('nav button').forEach(b => {{
    const k = b.dataset.key;
    const c = b.querySelector('span');
    if (k === 'all') c.textContent = total;
    else {{
      let t = 0, d = 0;
      WORKS.forEach(w => w.platforms.filter(p => p.key === k).forEach(() => {{ t++; if (isDone(w.slug, k)) d++; }}));
      c.textContent = d + '/' + t;
    }}
  }});
}}

function buildNav() {{
  const nav = document.getElementById('nav');
  const opts = [['all', 'All platforms']].concat(Object.entries(PLATFORMS).map(([k, v]) => [k, v.label]));
  nav.innerHTML = opts.map(([k, label]) => `<button data-key="${{k}}" class="${{k === current ? 'on' : ''}}">${{label}}<span></span></button>`).join('');
  nav.querySelectorAll('button').forEach(b => b.onclick = () => {{ current = b.dataset.key; buildNav(); render(); }});
}}

function esc(s) {{ return String(s).replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c])); }}

function field(label, value, slug, name) {{
  return `<div class="field"><div class="lbl"><span>${{label}}</span>
    <button class="copy" data-copy="${{esc(value).replace(/"/g, '&quot;')}}" data-key="${{slug}}::${{name}}">copy</button></div>
    <div class="val">${{esc(value)}}</div></div>`;
}}

function render() {{
  const main = document.getElementById('main');
  let cards = '';
  WORKS.forEach(w => {{
    const list = current === 'all' ? w.platforms : w.platforms.filter(p => p.key === current);
    if (!list.length) return;
    list.forEach(p => {{
      const pl = PLATFORMS[p.key];
      const done = isDone(w.slug, p.key);
      cards += `<div class="card ${{done ? 'done' : ''}}">
        <div class="top">
          <input type="checkbox" data-tick="${{w.slug}}::${{p.key}}" ${{done ? 'checked' : ''}}>
          <div>
            <span class="badge">${{esc(pl.label)}} · P${{p.priority}}</span>
            <div class="ttl">${{esc(w.title)}}</div>
            <div class="hook">${{esc(w.hook)}}</div>
          </div>
        </div>
        <div class="fields">
          ${{field('Title', w.title, w.slug, 'title')}}
          ${{field('Short description / hook', w.hook, w.slug, 'hook')}}
          ${{field('Abstract', w.abstract, w.slug, 'abstract')}}
          ${{field('Keywords', w.keywords, w.slug, 'keywords')}}
          ${{field('APA citation', w.apa, w.slug, 'apa')}}
          ${{field('Canonical URL (always paste this)', w.url, w.slug, 'url')}}
        </div>
        <div class="links">
          <a href="${{esc(w.pdf)}}" target="_blank" rel="noopener">open PDF ↗</a>
          <a href="${{esc(w.source)}}" target="_blank" rel="noopener">open source file ↗</a>
          <a href="${{esc(pl.url)}}" target="_blank" rel="noopener">${{esc(pl.label)}} upload page ↗</a>
          <span style="color:#93a4b8">${{esc(pl.note)}}</span>
        </div>
      </div>`;
    }});
  }});
  main.innerHTML = cards || '<div class="empty">Nothing here.</div>';

  main.querySelectorAll('[data-tick]').forEach(cb => {{
    cb.onchange = () => {{
      const k = cb.dataset.tick;
      if (cb.checked) state[k] = true; else delete state[k];
      save();
      cb.closest('.card').classList.toggle('done', cb.checked);
    }};
  }});

  main.querySelectorAll('.copy').forEach(btn => {{
    btn.onclick = async () => {{
      const text = btn.dataset.copy;
      try {{
        await navigator.clipboard.writeText(text);
      }} catch (e) {{
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try {{ document.execCommand('copy'); }} catch (e2) {{}}
        ta.remove();
      }}
      btn.textContent = 'copied';
      btn.classList.add('ok');
      setTimeout(() => {{ btn.textContent = 'copy'; btn.classList.remove('ok'); }}, 1200);
    }};
  }});
  renderStats();
}}

document.getElementById('reset').onclick = (e) => {{
  e.preventDefault();
  if (confirm('Clear all ticked progress?')) {{ state = {{}}; save(); buildNav(); render(); }}
}};

buildNav();
render();
</script>
</body>
</html>
"""
    (KIT / "upload-console.html").write_text(html, encoding="utf-8")
    print("upload-console.html written")


if __name__ == "__main__":
    works = load_works()
    build_tracker(works)
    build_console(works)
