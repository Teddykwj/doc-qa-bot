"""
Scrape LangChain / LangGraph docs from docs.langchain.com and save as markdown.
Usage: python scripts/scrape_docs.py
"""
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT_DIR = Path(__file__).parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"

SITEMAP_URL = "https://docs.langchain.com/sitemap.xml"

# URL prefix 기준으로 수집 대상 분리
TARGETS = {
    "langchain": "https://docs.langchain.com/oss/python/langchain/",
    "langgraph": "https://docs.langchain.com/oss/python/langgraph/",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; doc-qa-bot/1.0)"}
DELAY = 0.5


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    resp = requests.get(sitemap_url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)  # bytes로 파싱 (인코딩 문제 방지)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
    print(f"  Total URLs in sitemap: {len(urls)}")
    return urls


def url_to_filename(url: str, prefix: str) -> Path:
    rel = url.removeprefix(prefix).strip("/") or "index"
    rel = re.sub(r"[^\w/\-]", "_", rel)
    return Path(rel + ".md")


def scrape_page(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"  SKIP {url} — {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    content = (
        soup.find("article")
        or soup.find("main")
        or soup.find(class_="md-content")
        or soup.find(class_="content")
        or soup.body
    )
    if not content:
        return None

    for tag in content.find_all(["nav", "footer", "aside", "script", "style"]):
        tag.decompose()

    return markdownify(str(content), heading_style="ATX", strip=["a"]).strip()


def collect(name: str, prefix: str, all_urls: list[str]):
    dest_dir = RAW_DIR / name
    dest_dir.mkdir(parents=True, exist_ok=True)

    urls = [u for u in all_urls if u.startswith(prefix)]
    print(f"\n[{name}] {len(urls)} pages matched (prefix: {prefix})")

    saved = 0
    for i, url in enumerate(urls, 1):
        rel_path = url_to_filename(url, prefix)
        dest = dest_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)

        md = scrape_page(url)
        if md:
            dest.write_text(md, encoding="utf-8")
            saved += 1
            print(f"  [{i}/{len(urls)}] {rel_path}")

        time.sleep(DELAY)

    print(f"[{name}] Done — {saved}/{len(urls)} pages saved.")


if __name__ == "__main__":
    print(f"Fetching sitemap: {SITEMAP_URL}")
    all_urls = fetch_sitemap_urls(SITEMAP_URL)

    for name, prefix in TARGETS.items():
        collect(name, prefix, all_urls)

    total = len(list(RAW_DIR.rglob("*.md")))
    print(f"\nTotal: {total} files in {RAW_DIR}")
