# -*- coding: utf-8 -*-
"""
Text extraction for DOCX / PPTX / PDF, used to build the full-text open-access PDFs.

DOCX  -> paragraphs in document order, heading styles become <h2>
PPTX  -> slides in numeric order, slide title becomes <h2>
PDF   -> page text via pypdf
"""
import os, re, zipfile, html

DEV = r"ऀ-ॿ"  # Devanagari + digits block


def _xml_to_text(xml, keep_newlines=True):
    xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    xml = re.sub(r"<w:br[^>]*/>", "\n", xml)
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"</a:p>", "\n", xml)
    xml = re.sub(r"<[^>]+>", "", xml)
    return html.unescape(xml)


def docx_html(path):
    """Return (html, plain_text)."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
            styles = {}
            try:
                sx = z.read("word/styles.xml").decode("utf-8", "ignore")
                for m in re.finditer(r'<w:style[^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', sx, re.S):
                    nm = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
                    if nm:
                        styles[m.group(1)] = nm.group(1).lower()
            except KeyError:
                pass
    except Exception as e:
        return f"<p>[Could not read source document: {e}]</p>", ""

    blocks = re.split(r"(?=<w:p[ >])", xml)
    out, plain = [], []
    for b in blocks:
        if "<w:t" not in b and "<w:pPr" not in b:
            continue
        txt = _xml_to_text(b)
        txt = re.sub(r"[ \t]+", " ", txt).replace("\u00a0", " ").strip()
        if not txt:
            continue
        style = ""
        ms = re.search(r'<w:pStyle w:val="([^"]+)"', b)
        if ms:
            style = styles.get(ms.group(1), ms.group(1).lower())
        plain.append(txt)
        is_head = bool(re.search(r"heading\s*1|heading\s*2|title", style))
        if not is_head:
            # heuristic: short ALL-CAPS or Title-ish line followed by content
            if len(txt) < 90 and txt.isupper() and re.search(r"[A-Z]{3}", txt):
                is_head = True
        if is_head:
            out.append(f"<h2>{html.escape(txt)}</h2>")
        else:
            out.append(f"<p>{html.escape(txt)}</p>")
    return "\n".join(out), "\n".join(plain)


def pptx_html(path):
    try:
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
            names.sort(key=lambda n: int(re.search(r"(\d+)", n).group(1)))
            slides = []
            plain = []
            for n in names:
                xml = z.read(n).decode("utf-8", "ignore")
                # split into shapes
                shapes = re.split(r"(?=<p:sp>|<p:graphicFrame>)", xml)
                lines = []
                for s in shapes:
                    if "<a:t>" not in s:
                        continue
                    t = _xml_to_text(s)
                    t = re.sub(r"[ \t]+", " ", t).strip()
                    if t:
                        lines.extend([l.strip() for l in t.split("\n") if l.strip()])
                if not lines:
                    continue
                slides.append((n, lines))
                plain.extend(lines)
    except Exception as e:
        return f"<p>[Could not read source presentation: {e}]</p>", ""

    out = []
    for i, (n, lines) in enumerate(slides):
        title = lines[0]
        rest = lines[1:]
        out.append(f'<h2 class="slide-title">Slide {i+1} &mdash; {html.escape(title)}</h2>')
        for l in rest:
            out.append(f"<p>{html.escape(l)}</p>")
    return "\n".join(out), "\n".join(plain)


def pdf_text(path, max_pages=60):
    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        parts = []
        for pg in r.pages[:max_pages]:
            try:
                parts.append(pg.extract_text() or "")
            except Exception:
                pass
        t = "\n".join(parts)
        return re.sub(r"\n{3,}", "\n\n", t).strip()
    except Exception as e:
        return f"[Could not read source PDF: {e}]"


def extract(path):
    """Return (html, plain) for any supported file."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return docx_html(path)
    if ext in (".pptx", ".pptm"):
        return pptx_html(path)
    if ext == ".pdf":
        t = pdf_text(path)
        blocks = [b for b in re.split(r"\n{2,}", t) if b.strip()]
        return "\n".join(f"<p>{html.escape(b)}</p>" for b in blocks), t
    if ext in (".txt", ".rtf", ".md"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            t = f.read()
        return "\n".join(f"<p>{html.escape(b)}</p>" for b in re.split(r"\n{2,}", t) if b.strip()), t
    return "<p>[Unsupported source format]</p>", ""
