"""
help_doc_crawler.py
-------------------
Document Ingestion Agent — crawls the SDP OnDemand help guide at
https://help.sdpondemand.com/ and extracts structured feature knowledge
per module/entity.

How it works:
  1. Intercepts the internal `topic/nav/load_toc_tree` JSON API to
     discover all topics with their IDs and permalinks — no scraping needed.
  2. For each topic, calls `topic/get_content` to fetch the raw HTML.
  3. Strips HTML tags → clean text, extracts:
       - title, permalink, module (parent section)
       - steps (numbered actions)
       - fields (UI field names + descriptions)
       - notes / warnings
  4. Saves to `knowledge_base/raw/help_topics.json` (full raw)
     and  `knowledge_base/raw/help_topics_flat.json` (one item per field/step)
     ready for ingestion into ChromaDB.

Usage:
    python ingestion/help_doc_crawler.py
    python ingestion/help_doc_crawler.py --module requests
    python ingestion/help_doc_crawler.py --module changes --module assets
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

# ── Path bootstrap ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ────────────────────────────────────────────────────────────────────────────

BASE_URL      = "https://help.sdpondemand.com"
COMPANY_ID    = "866"
PROJECT_ID    = "2514"
OUT_RAW       = ROOT / "knowledge_base/raw/help_topics.json"
OUT_FLAT      = ROOT / "knowledge_base/raw/help_topics_flat.json"

# Modules we care about for automation test generation
TARGET_MODULES = {
    "Requests", "Problems", "Changes", "Projects", "Releases",
    "Solutions", "Assets", "Purchase", "Contracts", "Maintenance",
    "Setup", "General", "Activities",
    "Configuration Management Database (CMDB)",
}

# ── HTML → structured text helpers ────────────────────────────────────────

def _clean_text(html: str) -> str:
    """Strip all HTML tags and collapse whitespace, scoped to main content area."""
    soup = BeautifulSoup(html, "lxml")
    # Scope to the main article div; fall back to body
    root = (
        soup.find("div", id="topic-content")
        or soup.find("div", class_="hiq-t")
        or soup
    )
    # Remove breadcrumb navigation noise
    for crumb in root.find_all("ul", class_="breadcrumbs"):
        crumb.decompose()
    text = root.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _extract_steps(soup: BeautifulSoup) -> list[str]:
    """Extract numbered/bulleted step instructions, skipping navigation noise."""
    # Scope to main content div
    root = (
        soup.find("div", id="topic-content")
        or soup.find("div", class_="hiq-t")
        or soup
    )
    steps = []
    for ol in root.find_all("ol"):
        for i, li in enumerate(ol.find_all("li"), 1):
            steps.append(f"{i}. {li.get_text(separator=' ').strip()}")
    for ul in root.find_all("ul"):
        # Skip breadcrumb / nav lists
        if "breadcrumbs" in (ul.get("class") or []):
            continue
        for li in ul.find_all("li"):
            text = li.get_text(separator=" ").strip()
            if text and len(text) > 10:
                steps.append(f"- {text}")
    return steps[:50]  # cap


def _extract_fields(soup: BeautifulSoup) -> list[dict]:
    """
    Extract field name → description pairs from tables or definition lists.
    Typical help doc pattern: <table> with two columns: Field | Description
    """
    # Scope to main content div
    root = (
        soup.find("div", id="topic-content")
        or soup.find("div", class_="hiq-t")
        or soup
    )
    fields = []
    for table in root.find_all("table"):
        rows = table.find_all("tr")
        for row in rows[1:]:  # skip header
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                name = cells[0].get_text(separator=" ").strip()
                desc = cells[1].get_text(separator=" ").strip()
                if name and desc and len(name) < 80:
                    fields.append({"field": name, "description": desc[:300]})
    # Also definition lists
    for dl in root.find_all("dl"):
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        for dt, dd in zip(dts, dds):
            fields.append({
                "field": dt.get_text().strip(),
                "description": dd.get_text(separator=" ").strip()[:300],
            })
    return fields[:40]


def _extract_notes(soup: BeautifulSoup) -> list[str]:
    """Extract Info/Tip/Warning callout boxes."""
    root = (
        soup.find("div", id="topic-content")
        or soup.find("div", class_="hiq-t")
        or soup
    )
    notes = []
    for el in root.find_all(class_=re.compile(r'note|tip|warn|info|callout', re.I)):
        text = el.get_text(separator=" ").strip()
        if text and len(text) > 10:
            notes.append(text[:300])
    return notes[:10]


def _detect_module(title: str, parent_text: str) -> str:
    """Map a topic to its canonical module name."""
    combined = (title + " " + parent_text).lower()
    mapping = {
        "request": "requests",
        "incident": "requests",
        "service request": "requests",
        "problem": "problems",
        "change": "changes",
        "release": "releases",
        "project": "projects",
        "asset": "assets",
        "cmdb": "cmdb",
        "contract": "contracts",
        "purchase": "purchase",
        "solution": "solutions",
        "maintenance": "maintenance",
        "setup": "setup",
        "general": "general",
    }
    for key, module in mapping.items():
        if key in combined:
            return module
    return "general"


def _parse_topic_html(html_content: str, title: str, permalink: str, parent: str) -> dict:
    """Parse raw HTML content → structured topic dict."""
    soup = BeautifulSoup(html_content, "lxml")
    full_text  = _clean_text(html_content)
    steps      = _extract_steps(soup)
    fields     = _extract_fields(soup)
    notes      = _extract_notes(soup)
    module     = _detect_module(title, parent)

    # Build embed text — rich description for semantic search
    embed_parts = [f"Module: {module} | Topic: {title}"]
    if steps:
        embed_parts.append("Steps: " + " | ".join(steps[:5]))
    if fields:
        field_names = [f["field"] for f in fields[:10]]
        embed_parts.append("Fields: " + ", ".join(field_names))
    embed_parts.append("Content: " + full_text[:500])
    embed_text = " | ".join(embed_parts)

    return {
        "id":         f"help_{permalink.replace('-', '_')}",
        "title":      title,
        "permalink":  permalink,
        "module":     module,
        "parent":     parent,
        "url":        f"{BASE_URL}/{permalink}",
        "full_text":  full_text[:5000],
        "steps":      steps,
        "fields":     fields,
        "notes":      notes,
        "embed_text": embed_text,
    }


# ── Crawler ────────────────────────────────────────────────────────────────

class HelpDocCrawler:

    def __init__(self, target_modules: Optional[list[str]] = None):
        self.target_modules = {m.lower() for m in (target_modules or [])}
        # Common query-string prefix for the get_content API
        self._session_params = (
            f"company_id={COMPANY_ID}&project_id={PROJECT_ID}&parent_id=null&ui_lang=en"
            f"&prim_index=0&view_mode=view&user_index=false&preview="
            f"&inst_preview=false&highlight_keyword=&script_indexs%5B%5D=&r_req=true"
        )

    async def crawl(self) -> list[dict]:
        """Full crawl — returns list of structured topic dicts."""
        from playwright.async_api import async_playwright

        topics_raw: list[dict] = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page    = await context.new_page()

            # ── Step 1: Load home page and collect full TOC ──────────────
            print("  [1/3] Loading help guide home page...")
            toc_items: list[dict] = []

            async def capture_toc(response):
                if "load_toc_tree" in response.url:
                    try:
                        data = await response.json()
                        toc_items.extend(data)
                    except Exception:
                        pass

            page.on("response", capture_toc)
            await page.goto(f"{BASE_URL}/home", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            # Expand all major modules to trigger their TOC API calls
            modules_to_expand = [
                "Requests", "Problems", "Changes", "Projects", "Releases",
                "Solutions", "Assets", "Purchase", "Contracts", "Maintenance",
                "Setup", "General", "Activities",
                "Configuration Management Database (CMDB)",
            ]
            print("  [2/3] Expanding modules to discover all topics...")
            for module in modules_to_expand:
                try:
                    await page.click(f"text={module}", timeout=3000)
                    await page.wait_for_timeout(1500)
                    print(f"       ✅ {module}")
                except Exception:
                    print(f"       ⚠️  Could not expand: {module}")

            # Deduplicate TOC
            seen: dict[str, dict] = {}
            for item in toc_items:
                if item.get("id") and item.get("permalink"):
                    seen[item["id"]] = item

            print(f"  [3/3] Discovered {len(seen)} topics. Fetching content...")
            await browser.close()

        # ── Step 2: Fetch content for each topic via the REST API ──────────
        # The API is publicly accessible — no cookies required.
        import aiohttp

        async with aiohttp.ClientSession(
            headers={"User-Agent": "Mozilla/5.0"}
        ) as session:
            total    = len(seen)
            done     = 0
            skipped  = 0

            for item_id, item in seen.items():
                permalink = item.get("permalink", "")
                title     = item.get("text", "").strip()
                parent    = item.get("parent_text", "")

                # Filter by target modules if specified
                if self.target_modules:
                    module = _detect_module(title, parent)
                    if module not in self.target_modules:
                        skipped += 1
                        continue

                dc = int(time.time() * 1000)
                url = (
                    f"{BASE_URL}/topic/get_content/?_dc={dc}"
                    f"&{self._session_params}"
                    f"&id=ID{item_id}"
                )

                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                        if resp.status == 200:
                            data = await resp.json(content_type=None)
                            # API structure: {"success": true, "data": {"content": "<html>"}}
                            payload = data.get("data", data) if isinstance(data, dict) else {}
                            html_content = payload.get("content", "") or payload.get("html", "")
                            if not html_content and isinstance(payload, dict):
                                # Try any key containing HTML
                                for v in payload.values():
                                    if isinstance(v, str) and "<" in v:
                                        html_content = v
                                        break

                            if html_content:
                                topic = _parse_topic_html(html_content, title, permalink, parent)
                                topic["topic_id"] = item_id  # preserve numeric ID
                                topics_raw.append(topic)
                                done += 1
                                steps_n  = len(topic.get("steps", []))
                                fields_n = len(topic.get("fields", []))
                                print(f"     [{done:3d}/{total}] ✅ {title[:50]:50s}  steps={steps_n} fields={fields_n}")
                            else:
                                # No HTML — just store metadata
                                topics_raw.append({
                                    "id":        f"help_{permalink.replace('-','_')}",
                                    "topic_id":  item_id,
                                    "title":     title,
                                    "permalink": permalink,
                                    "module":    _detect_module(title, parent),
                                    "parent":    parent,
                                    "url":       f"{BASE_URL}/{permalink}",
                                    "full_text": title,
                                    "steps":     [],
                                    "fields":    [],
                                    "notes":     [],
                                    "embed_text": f"Module: {_detect_module(title, parent)} | Topic: {title}",
                                })
                                done += 1
                        else:
                            print(f"     [{done:3d}/{total}] ⚠️  HTTP {resp.status} — {title[:40]}")
                except Exception as ex:
                    print(f"     ⚠️  Error fetching {title[:40]}: {ex}")

                await asyncio.sleep(0.3)  # polite crawl rate

        return topics_raw

    def run(self, target_modules: Optional[list[str]] = None) -> list[dict]:
        """Synchronous entry point."""
        if target_modules:
            self.target_modules = {m.lower() for m in target_modules}
        return asyncio.run(self.crawl())


# ── Save + flatten ─────────────────────────────────────────────────────────

def save_topics(topics: list[dict]) -> tuple[int, int]:
    """
    Save topics to:
      - knowledge_base/raw/help_topics.json       (full structured)
      - knowledge_base/raw/help_topics_flat.json  (one record per field/step, ready for ChromaDB)
    Returns (raw_count, flat_count).
    """
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)

    # Merge with existing if present
    existing = {}
    if OUT_RAW.exists():
        try:
            for t in json.loads(OUT_RAW.read_text()):
                existing[t["id"]] = t
        except Exception:
            pass

    for t in topics:
        existing[t["id"]] = t

    raw_list = list(existing.values())
    OUT_RAW.write_text(json.dumps(raw_list, indent=2, ensure_ascii=False))

    # Build flat list for embedding
    flat = []
    for topic in raw_list:
        base = {
            "topic_id":   topic["id"],
            "title":      topic["title"],
            "module":     topic["module"],
            "permalink":  topic["permalink"],
            "url":        topic.get("url", ""),
        }

        # One record for the full topic text
        flat.append({
            **base,
            "id":         f"{topic['id']}_full",
            "type":       "full_text",
            "content":    topic.get("full_text", "")[:3000],
            "embed_text": topic.get("embed_text", topic["title"]),
        })

        # One record per field
        for i, f in enumerate(topic.get("fields", [])):
            flat.append({
                **base,
                "id":         f"{topic['id']}_field_{i}",
                "type":       "field",
                "content":    f"{f['field']}: {f['description']}",
                "embed_text": f"Module: {topic['module']} | Topic: {topic['title']} | Field: {f['field']} | {f['description'][:200]}",
            })

        # One record per step group (every 5 steps)
        steps = topic.get("steps", [])
        for i in range(0, len(steps), 5):
            chunk = steps[i:i + 5]
            flat.append({
                **base,
                "id":         f"{topic['id']}_steps_{i}",
                "type":       "steps",
                "content":    "\n".join(chunk),
                "embed_text": f"Module: {topic['module']} | Topic: {topic['title']} | Steps: {' '.join(chunk)[:400]}",
            })

    OUT_FLAT.write_text(json.dumps(flat, indent=2, ensure_ascii=False))
    return len(raw_list), len(flat)


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SDP Help Doc Crawler")
    parser.add_argument(
        "--module", action="append", dest="modules",
        help="Only crawl specific module(s). Can be specified multiple times. "
             "e.g. --module requests --module changes"
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  SDP OnDemand Help Doc Crawler")
    print("=" * 60)

    if args.modules:
        print(f"  Target modules: {args.modules}")
    else:
        print("  Target modules: ALL")

    # Check aiohttp installed
    try:
        import aiohttp
    except ImportError:
        print("\n  Installing aiohttp...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp", "-q"])
        import aiohttp

    crawler = HelpDocCrawler()
    topics  = crawler.run(target_modules=args.modules)

    print(f"\n  📄 Fetched {len(topics)} topics")

    raw_count, flat_count = save_topics(topics)
    print(f"  ✅ Saved {raw_count} topics to {OUT_RAW.relative_to(ROOT)}")
    print(f"  ✅ Saved {flat_count} flat records to {OUT_FLAT.relative_to(ROOT)}")
    print(f"\n  Next step: python knowledge_base/rag_indexer.py")
    print("=" * 60 + "\n")
