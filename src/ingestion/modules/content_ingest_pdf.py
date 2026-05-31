import re
import fitz  # pymupdf
import pandas as pd
from pathlib import Path

ARXIV_SECTIONS = (
    "abstract", "introduction", "related work", "background",
    "methodology", "method", "methods", "approach", "model",
    "experiments", "experiment", "results", "evaluation",
    "discussion", "conclusion", "conclusions", "references",
    "appendix", "acknowledgements", "acknowledgments",
    "limitations", "future work", "contributions", "motivation",
    "problem statement", "theoretical framework", "analysis",
    "implementation", "setup", "dataset", "datasets", "baselines",
    "ablation", "ablation study", "supplementary", "notation"
)


HEADING_SCORE_THRESHOLD = 5  # tune this if needed

def ingest_pdf(pdf_path: str, output_dir: str = "dataset/ingested") -> dict:
    print(f"  Reading PDF: {pdf_path}")
    doc      = fitz.open(pdf_path)
    full_text, sections_metadata, text_by_section = extract_pdf_content(doc)

    # One row per section
    rows = []
    for section in sections_metadata:
        heading = section["text"]
        rows.append({
            "url":               f"{pdf_path}/{heading}",
            "sections_metadata": section,
            "text_by_section":   heading,
            "full_text":         text_by_section.get(heading, ""),
        })

    print(f"    {len(rows)} sections | {len(full_text):,} chars")

    # Save to parquet
    out_path = Path(output_dir) / f"{Path(pdf_path).stem}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(out_path, index=False)
    print(f"  Saved to {out_path}")

    return rows


def extract_pdf_content(doc: fitz.Document) -> tuple[str, list, dict]:
    blocks         = _extract_blocks(doc)
    font_sizes     = [b["size"] for b in blocks if b["text"].strip()]
    heading_thresh = _heading_threshold(font_sizes)

    sections_metadata = []
    text_by_section   = {}
    current_heading   = None
    current_text      = []
    full_lines        = []

    for block in blocks:
        text = block["text"].strip()
        if not text:
            continue

        full_lines.append(text)
        score = _heading_score(text, block["size"], heading_thresh)

        if score >= HEADING_SCORE_THRESHOLD:
            if current_heading and current_text:
                text_by_section[current_heading] = " ".join(current_text).strip()

            current_heading = text
            current_text    = []
            sections_metadata.append({
                "text":  text,
                "level": _heading_level(block["size"], heading_thresh),
                "page":  block["page"],
                "score": score,
            })
        else:
            current_text.append(text)

    if current_heading and current_text:
        text_by_section[current_heading] = " ".join(current_text).strip()

    return "\n".join(full_lines), sections_metadata, text_by_section







def _heading_score(text: str, size: float, threshold: float) -> int:
    score = 0
    clean = text.strip().lower().rstrip(".")

    # Reject obvious noise immediately
    if len(text.strip()) < 3:           return 0  # single chars, commas
    if re.match(r"^[\W\d]+$", text):    return 0  # only symbols/numbers
    if re.match(r"^\d+$", text):        return 0  # page numbers
    if "@" in text:                     return 0  # emails
    if re.match(r"^\*+$", text):        return 0  # footnote markers

    # Font size signals
    if size >= threshold + 6:   score += 4
    elif size >= threshold + 3: score += 3
    elif size >= threshold:     score += 2

    # Known section name
    if clean in ARXIV_SECTIONS:
        score += 3

    # Numbered section: "1. Introduction" or "2.1 Background"
    if re.match(r"^\d+(\.\d+)*\.?\s+[A-Z]", text.strip()):
        score += 3

    # Short line (headings are rarely long paragraphs)
    if len(text.strip()) < 60:
        score += 1

    # ALL CAPS
    if text.strip().isupper():
        score += 2
    elif text.strip().istitle():
        score += 1

    # Ends with colon
    if text.strip().endswith(":"):
        score += 1

    return score




# def extract_pdf_content(doc: fitz.Document) -> tuple[str, list, dict]:
#     blocks         = _extract_blocks(doc)
#     font_sizes     = [b["size"] for b in blocks if b["text"].strip()]
#     heading_thresh = _heading_threshold(font_sizes)

#     sections_metadata = []
#     text_by_section   = {}
#     current_heading   = None
#     current_text      = []
#     full_lines        = []

#     for block in blocks:
#         text = block["text"].strip()
#         if not text:
#             continue

#         full_lines.append(text)
#         score = _heading_score(text, block["size"], heading_thresh)

#         if score >= HEADING_SCORE_THRESHOLD:
#             if current_heading and current_text:
#                 text_by_section[current_heading] = " ".join(current_text).strip()

#             current_heading = text
#             current_text    = []
#             sections_metadata.append({
#                 "text":  text,
#                 "level": _heading_level(block["size"], heading_thresh),
#                 "page":  block["page"],
#                 "score": score,   # useful for debugging
#             })
#         else:
#             current_text.append(text)

#     if current_heading and current_text:
#         text_by_section[current_heading] = " ".join(current_text).strip()

#     return "\n".join(full_lines), sections_metadata, text_by_section


def _extract_blocks(doc: fitz.Document) -> list[dict]:
    blocks = []
    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    blocks.append({
                        "text": span["text"],
                        "size": round(span["size"]),
                        "page": page_num,
                    })
    return blocks


def _heading_threshold(font_sizes: list[float]) -> float:

    if not font_sizes:
        return 12.0
    sorted_sizes = sorted(font_sizes)
    idx          = int(len(sorted_sizes) * 0.75)
    return sorted_sizes[idx]


def _heading_level(size: float, threshold: float) -> int:

    diff = size - threshold
    if diff >= 6:
        return 1
    elif diff >= 3:
        return 2
    else:
        return 3