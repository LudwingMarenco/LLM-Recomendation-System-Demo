import re
import json
import time
import requests
import subprocess
import trafilatura
import pandas as pd
from pathlib import Path
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag




DELAY = 1.0
MAX_PAGES = 50

HEADERS = {
"User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
),
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
}

SKIP_PREFIXES = (
    "/api/",
    "/_next/",
    "/static/",
    "/favicon",
    "/opengraph",
    "/ai-2027.pdf",
)


SKIP_PATTERNS = re.compile(r"\.(pdf|png|jpg|jpeg|svg|ico|xml|rss|json|css|js)$", re.I)

def ingest_http(base_url: str, output_dir: str)-> None:
    start = normalise(base_url)
    queue = deque([start])
    visited = set()
    all_data = {}
 
    print(f"  Starting crawl from {start}\n")
 
    while queue and len(visited) < MAX_PAGES:
        url = queue.popleft()
        if url not in visited:
            visited.add(url)
            path = urlparse(url).path or "/"
            print(f"  [{len(visited):02d}] {url}")
            html = fetch_html(url)

            if html:
                new_links = extract_links(html, url, base_url)
                added = 0
                for link in new_links:
                    if link not in visited and link not in queue:
                        queue.append(link)
                        added += 1

                sections = discover_sections(html, url)
                body_text = extract_text(html, url)
                text_by_sect = split_by_headings(body_text, [s["text"] for s in sections])
        
                print(f"    {len(sections)} headings | {len(body_text)} chars | {added} new links queued")
        
                all_data[path] = {
                    "url": url,
                    "sections_metadata": sections,
                    "text_by_section": text_by_sect,
                    "full_text": body_text,
                }
    
            time.sleep(DELAY)
 
    print(f"\n  Crawl complete -- {len(visited)} pages visited, {len(all_data)} scraped")

    if all_data:
        
        domain   = urlparse(base_url).netloc.replace(".", "_")
        out_path = Path(output_dir) / f"{domain}.parquet"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(all_data.values()).to_parquet(out_path, index=False)
        print(f"  Saving scraped text to {out_path}")

    return None


def normalise(url: str) -> str:
    url, _ = urldefrag(url)
    p = urlparse(url)
    path = p.path.rstrip("/") or "/"
    return p._replace(path=path, query="", fragment="").geturl()

def fetch_html(url: str) -> str | None:
    
    html = trafilatura.fetch_url(url)
    if html:
        return html

    try:
        session = requests.Session()
        base = "{parsed.scheme}://{parsed.netloc}".format(parsed=urlparse(url))
        session.get(base, headers=HEADERS, timeout=20)
        time.sleep(1)
        
        headers = {**HEADERS, "Referer": base + "/"}
        r = session.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as exc:
        print(f"     requests failed: {exc}")

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-L",
                "-A", HEADERS["User-Agent"],
                "--compressed",
                "-H", f"Accept: {HEADERS['Accept']}",
                "-H", f"Accept-Language: {HEADERS['Accept-Language']}",
                "--max-time", "20",
                url
            ],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception as exc:
        print(f"     curl failed: {exc}")

    return None


def is_internal(url: str, base_url: str) -> bool:
    parsed = urlparse(url)
    base = urlparse(base_url)
    return parsed.netloc in ("", base.netloc)
 
 
def should_skip(url: str) -> bool:
    path = urlparse(url).path
    if SKIP_PATTERNS.search(path):
        return True
    return any(path.startswith(p) for p in SKIP_PREFIXES)  


def extract_links(html: str, page_url: str, base_url: str) -> list[str]:
    soup        = BeautifulSoup(html, "html.parser")
    parsed_base = urlparse(base_url)
    bare_domain = parsed_base.netloc

    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href and not href.startswith(("mailto:", "tel:", "javascript:", "#")):
            if href.startswith(bare_domain):
                href = "/" + href[len(bare_domain):].lstrip("/")
            full = normalise(urljoin(page_url, href))
            if is_internal(full, base_url) and not should_skip(full):
                links.append(full)

    return list(set(links))

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")
 
 
def discover_sections(html: str, page_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    sections = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(separator=" ", strip=True)
        if not text:
            continue
        html_id = tag.get("id") or slugify(text)
        sections.append({
            "id": html_id,
            "level": int(tag.name[1]),
            "text": text,
            "anchor_url": f"{page_url}#{html_id}",
        })
    return sections

def extract_text(html: str, url: str) -> str:
    return trafilatura.extract(
        html,
        url = url,
        include_comments = False,
        include_tables = False,
        favor_recall = True,
        output_format = "txt",
    ) or ""
 
 
def split_by_headings(full_text: str, heading_texts: list[str]) -> dict[str, str]:

    escaped = [re.escape(s) for s in heading_texts if s]
    if not escaped:
        return {"full_page": full_text}
    pattern = re.compile(
        r"^(" + "|".join(escaped) + r")$", re.MULTILINE | re.IGNORECASE
    )
    parts = pattern.split(full_text)
    result = {}
    if parts[0].strip():
        result["_preamble"] = parts[0].strip()
    i = 1
    while i + 1 < len(parts):
        result[parts[i].strip()] = parts[i + 1].strip()
        i += 2
    return result

