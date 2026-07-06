#!/usr/bin/env python3
"""Extract text and images from legacy diodi.if.ua (Joomla) site."""

from __future__ import annotations

import html as htmlmod
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

BASE_URL = "https://diodi.if.ua"
UA = "Mozilla/5.0 (compatible; DiodiLegacyExtractor/1.0)"
ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "content" / "legacy"
TEXT_DIR = OUTPUT / "text"
IMAGES_DIR = OUTPUT / "images"

PAGES: list[dict[str, str]] = [
    {"path": "/", "slug": "home", "file": "home.md"},
    {"path": "/pro-nas", "slug": "pro-nas", "file": "pro-nas.md"},
    {"path": "/pro-nas/nasha-komanda", "slug": "nasha-komanda", "file": "team/nasha-komanda.md"},
    {"path": "/pro-nas/fotohalereia", "slug": "fotohalereia", "file": "fotohalereia.md"},
    {"path": "/kontakty", "slug": "kontakty", "file": "kontakty.md"},
    {"path": "/posluhy", "slug": "posluhy", "file": "posluhy.md"},
    {"path": "/tsiny", "slug": "tsiny", "file": "tsiny.md"},
    {"path": "/vidhuky", "slug": "vidhuky", "file": "vidhuky.md"},
    {"path": "/labaratoriia", "slug": "labaratoriia", "file": "labaratoriia.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia", "slug": "terapevtychna", "file": "posluhy/terapevtychna-stomatolohiia.md"},
    {"path": "/posluhy/ortopedychna-stomatolohiia", "slug": "ortopedychna", "file": "posluhy/ortopedychna-stomatolohiia.md"},
    {"path": "/posluhy/implantolohiia", "slug": "implantolohiia", "file": "posluhy/implantolohiia.md"},
    {"path": "/posluhy/renthenohrafiia", "slug": "renthenohrafiia", "file": "posluhy/renthenohrafiia.md"},
    {"path": "/posluhy/khirurhiia", "slug": "khirurhiia", "file": "posluhy/khirurhiia.md"},
    {"path": "/posluhy/3d-skanuvannya", "slug": "3d-skanuvannya", "file": "posluhy/3d-skanuvannya.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/endodontiia-likuvannia-korenevykh-kanaliv", "slug": "endodontiia", "file": "posluhy/endodontiia.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/estetychna-restavratsiia", "slug": "estetychna-restavratsiia", "file": "posluhy/estetychna-restavratsiia.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/likuvannia-paradontu", "slug": "likuvannia-paradontu", "file": "posluhy/likuvannia-paradontu.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/plombuvannia-usikh-vydiv-kariiesu", "slug": "plombuvannia", "file": "posluhy/plombuvannia.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/profesiina-hihiiena-rotovoi-porozhnyny", "slug": "profesiina-hihiiena", "file": "posluhy/profesiina-hihiiena.md"},
    {"path": "/posluhy/terapevtychna-stomatolohiia/profesiine-vidbiliuvannia", "slug": "profesiine-vidbiliuvannia", "file": "posluhy/profesiine-vidbiliuvannia.md"},
    {"path": "/posluhy/ortopedychna-stomatolohiia/neznimne-protezuvannia", "slug": "neznimne-protezuvannia", "file": "posluhy/neznimne-protezuvannia.md"},
    {"path": "/posluhy/ortopedychna-stomatolohiia/znimne-protezuvannia", "slug": "znimne-protezuvannia", "file": "posluhy/znimne-protezuvannia.md"},
    {"path": "/pro-nas/nasha-komanda/dyrektor", "slug": "dyrektor", "file": "team/dyrektor.md"},
    {"path": "/pro-nas/nasha-komanda/holovnyi-likar", "slug": "holovnyi-likar", "file": "team/holovnyi-likar.md"},
    {"path": "/pro-nas/nasha-komanda/likar-skovorodniev", "slug": "likar-skovorodniev", "file": "team/likar-skovorodniev.md"},
    {"path": "/pro-nas/nasha-komanda/administrator-platonova-olena", "slug": "administrator", "file": "team/administrator.md"},
    {"path": "/pro-nas/nasha-komanda/cerednii-medychnyi-personal-petrushka-snizhana-serhiivna", "slug": "basarab", "file": "team/basarab.md"},
    {"path": "/pro-nas/nasha-komanda/cerednii-medychnyi-personal-volochii-ivanna-serhiivna", "slug": "volochii", "file": "team/volochii.md"},
    {"path": "/pro-nas/nasha-komanda/molodshyi-medychnyi-personal-svintsytska-nataliia-valeriivna", "slug": "svintsytska", "file": "team/svintsytska.md"},
    {"path": "/pro-nas/nasha-komanda/zubnyi-tekhnik-moderuk", "slug": "moderuk", "file": "team/moderuk.md"},
    {"path": "/pro-nas/nasha-komanda/likar-stomatoloh-dubishchak-vitaliia-yakivna", "slug": "dubishchak", "file": "team/dubishchak.md"},
    {"path": "/pro-nas/nasha-komanda/cerednii-medychnyi-personal-dutchak-halyna-mykolaivna", "slug": "dutchak", "file": "team/dutchak.md"},
]

EMAIL_FALLBACK = "diodi2001@gmail.com"


def fetch(url: str, retries: int = 3) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            last_err = exc
            time.sleep(1 + attempt)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<script[^>]*>.*?</script>", "", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<style[^>]*>.*?</style>", "", fragment, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = htmlmod.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def clean_paragraph(text: str) -> str:
    text = strip_tags(text)
    if not text or text in ("\xa0", "&nbsp;"):
        return ""
    if "document.getElementById" in text or "var prefix" in text:
        return ""
    if "Ця електронна адреса захищена" in text:
        return f"e-mail: {EMAIL_FALLBACK}"
    return text


def extract_meta(html: str) -> dict[str, str]:
    title_m = re.search(r"<title>([^<]+)</title>", html, re.I)
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    kw_m = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', html, re.I)
    og_img = re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', html, re.I)
    return {
        "title": title_m.group(1).strip() if title_m else "",
        "description": desc_m.group(1) if desc_m else "",
        "keywords": kw_m.group(1) if kw_m else "",
        "og_image": og_img.group(1) if og_img else "",
    }


def extract_images(html: str) -> list[str]:
    found: set[str] = set()
    for match in re.findall(r'(?:src|href)="(/images/[^"?#]+)"', html, re.I):
        if "/thumbnails/" in match:
            continue
        found.add(match)
    return sorted(found)


def table_to_markdown(table_html: str) -> str:
    rows: list[list[str]] = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.S | re.I):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S | re.I)
        if cells:
            rows.append([clean_paragraph(c) for c in cells])
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    norm = [r + [""] * (width - len(r)) for r in rows]
    lines = [
        "| " + " | ".join(norm[0]) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for row in norm[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def parse_article(html: str, path: str) -> dict:
    art_m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S | re.I)
    body = art_m.group(1) if art_m else html
    headings: list[dict[str, str]] = []
    for level in range(1, 4):
        for m in re.finditer(rf"<h{level}[^>]*>(.*?)</h{level}>", body, re.S | re.I):
            text = clean_paragraph(m.group(1))
            if text:
                headings.append({"level": level, "text": text})

    paragraphs = [
        clean_paragraph(p)
        for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S | re.I)
    ]
    paragraphs = [p for p in paragraphs if p]

    tables_md: list[str] = []
    for table in re.findall(r"<table[^>]*>(.*?)</table>", body, re.S | re.I):
        md = table_to_markdown(table)
        if md:
            tables_md.append(md)

    images = extract_images(body)
    return {
        "headings": headings,
        "paragraphs": paragraphs,
        "tables_md": tables_md,
        "images": images,
    }


def path_to_markdown(page: dict, meta: dict, parsed: dict) -> str:
    lines = [
        "---",
        f"source_url: {BASE_URL}{page['path']}",
        f"title: {meta['title']}",
        f"slug: {page['slug']}",
        "---",
        "",
    ]
    if parsed["headings"]:
        h1 = next((h["text"] for h in parsed["headings"] if h["level"] == 1), meta["title"])
        lines.append(f"# {h1}")
        lines.append("")
    for h in parsed["headings"]:
        if h["level"] == 1:
            continue
        lines.append(f"{'#' * (h['level'] + 1)} {h['text']}")
        lines.append("")

    for para in parsed["paragraphs"]:
        lines.append(para)
        lines.append("")

    for table in parsed["tables_md"]:
        lines.append(table)
        lines.append("")

    if parsed["images"]:
        lines.append("## Зображення")
        lines.append("")
        for img in parsed["images"]:
            name = Path(img).name
            local = f"../images/{image_local_rel(img)}"
            lines.append(f"![{name}]({local})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def suggest_seo(page: dict, meta: dict, parsed: dict) -> dict[str, str]:
    h1 = next((h["text"] for h in parsed["headings"] if h["level"] == 1), meta["title"])
    first_para = parsed["paragraphs"][0] if parsed["paragraphs"] else ""
    brand = "Стоматологія ДіОДі"
    city = "Івано-Франківськ"

    if page["path"] == "/":
        title = f"{brand} — клініка в {city}"
    elif page["path"].startswith("/pro-nas/nasha-komanda/"):
        title = f"{h1} | {brand}"
    else:
        title = f"{h1} | {brand}, {city}"

    desc = first_para[:155] + ("…" if len(first_para) > 155 else "")
    if not desc:
        desc = f"{h1}. Стоматологічна клініка «ДіОДі» у {city}. Запис: (050) 537-76-57."

    og_image = parsed["images"][0] if parsed["images"] else "/images/logo.jpg"
    if og_image.startswith("http"):
        og_full = og_image
    else:
        og_full = f"{BASE_URL}{og_image}"

    return {
        "title": title,
        "description": desc,
        "og_title": title,
        "og_description": desc,
        "og_image": og_full,
        "canonical": f"{BASE_URL}{page['path']}" if page["path"] != "/" else f"{BASE_URL}/",
    }


def image_local_rel(img_path: str) -> str:
    return img_path.removeprefix("/images/").lstrip("/")


def image_local_path(img_path: str) -> Path:
    return IMAGES_DIR / image_local_rel(img_path)


def image_url(img_path: str) -> str:
    encoded = "/".join(quote(part, safe="") for part in img_path.split("/"))
    return BASE_URL + encoded


def download_image(img_path: str, log: list[str]) -> bool:
    local = image_local_path(img_path)
    if local.exists() and local.stat().st_size > 0:
        return True
    local.parent.mkdir(parents=True, exist_ok=True)
    url = image_url(img_path)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            local.write_bytes(resp.read())
        return True
    except Exception as exc:
        log.append(f"FAIL {img_path}: {exc}")
        return False


def build_seo_markdown(entries: list[dict]) -> str:
    lines = [
        "# SEO-рекомендації для нового сайту",
        "",
        "Згенеровано на основі викачаного контенту legacy-сайту diodi.if.ua.",
        "",
        "**Поточний стан legacy:** meta description і keywords відсутні на всіх сторінках.",
        "",
    ]
    for entry in entries:
        if entry.get("status") == "404":
            continue
        seo = entry["seo"]
        lines.append(f"## {entry['meta']['title']}")
        lines.append("")
        lines.append(f"- **URL:** `{entry['path']}`")
        lines.append(f"- **Файл контенту:** `text/{entry['file']}`")
        lines.append(f"- **title:** `{seo['title']}`")
        lines.append(f"- **description:** `{seo['description']}`")
        lines.append(f"- **og:title:** `{seo['og_title']}`")
        lines.append(f"- **og:description:** `{seo['og_description']}`")
        lines.append(f"- **og:image:** `{seo['og_image']}`")
        lines.append(f"- **canonical:** `{seo['canonical']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "seo").mkdir(parents=True, exist_ok=True)

    all_images: set[str] = set()
    entries: list[dict] = []
    download_log: list[str] = []

    for page in PAGES:
        url = BASE_URL + page["path"]
        print(f"Fetching {url}")
        html = fetch(url)
        if html is None:
            print(f"  SKIP 404: {url}")
            entries.append({
                "path": page["path"],
                "slug": page["slug"],
                "file": page["file"],
                "status": "404",
                "meta": {"title": "", "description": "", "keywords": "", "og_image": ""},
                "seo": {},
                "headings": [],
                "paragraph_count": 0,
                "image_count": 0,
                "has_tables": False,
            })
            continue
        meta = extract_meta(html)
        parsed = parse_article(html, page["path"])
        seo = suggest_seo(page, meta, parsed)

        md_path = TEXT_DIR / page["file"]
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(path_to_markdown(page, meta, parsed), encoding="utf-8")

        all_images.update(parsed["images"])
        entries.append({
            "path": page["path"],
            "slug": page["slug"],
            "file": page["file"],
            "status": "ok",
            "meta": meta,
            "seo": seo,
            "headings": parsed["headings"],
            "paragraph_count": len(parsed["paragraphs"]),
            "image_count": len(parsed["images"]),
            "has_tables": bool(parsed["tables_md"]),
        })

    # Global images from homepage footer/header
    home_html = fetch(BASE_URL + "/")
    all_images.update(extract_images(home_html))
    all_images.add("/images/logo.jpg")

    print(f"Downloading {len(all_images)} images...")
    ok = 0
    for img in sorted(all_images):
        if download_image(img, download_log):
            ok += 1

    index = {
        "source": BASE_URL,
        "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "page_count": len(entries),
        "image_count": len(all_images),
        "images_downloaded": ok,
        "download_errors": download_log,
        "pages": entries,
    }
    (TEXT_DIR / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUTPUT / "seo" / "recommendations.md").write_text(
        build_seo_markdown(entries), encoding="utf-8"
    )

    print(f"Done: {len(entries)} pages, {ok}/{len(all_images)} images")
    if download_log:
        print(f"Image errors: {len(download_log)}")


if __name__ == "__main__":
    main()
