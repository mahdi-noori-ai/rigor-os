#!/usr/bin/env python3
"""Extract SEO context from a project's layouts, pages, and metadata.

Deterministic first pass for the SEO Strategist agent (agents/seo-strategist/).
It reads source files — it never fetches the network — and writes:

* ``SEO_CONTEXT.json``  machine-readable inventory (routes, metadata, gaps)
* ``SEO_CONTEXT.md``    the same, summarised for an agent to extend

Supported surfaces: Next.js (app + pages router), Astro, SvelteKit, Nuxt,
Remix/React Router, plain HTML / Vite SPA, Django/Jinja templates, Markdown
content, plus distribution metadata (README, package.json, pyproject.toml,
AndroidManifest/Play listing) for non-web search surfaces.

Usage:
    python tools/seo_context.py [--root PATH] [--out-dir DIR] [--base-url URL] [--check]

``--check`` exits 1 when an indexable page lacks a title or description, so the
SEOGate can run in CI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from itertools import pairwise
from pathlib import Path

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".output",
    "dist",
    "build",
    "out",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    ".turbo",
    ".vercel",
    ".cache",
    "vendor",
    "target",
    ".gradle",
    "Pods",
    "rigor-os",
    ".idea",
    ".vscode",
    "staticfiles",
}

TITLE_MAX = 60
DESC_MIN, DESC_MAX = 70, 160

STOPWORDS = set(
    """a about above after again against all am an and any are as at be because been before being below
    between both but by can could did do does doing down during each few for from further had has have
    having he her here hers herself him himself his how i if in into is it its itself just me more most my
    myself no nor not now of off on once only or other our ours ourselves out over own same she should so
    some such than that the their theirs them themselves then there these they this those through to too
    under until up very was we were what when where which while who whom why will with you your yours
    yourself yourselves get got use using used also may might must can't don't won't one two new via per
    class classname div span div props return const export default import from function true false null
    undefined let var await async type interface string number boolean children href src alt id key
    onclick onchange value style map item items data https http www com org""".split()
)


@dataclass
class Page:
    route: str
    file: str
    kind: str  # page | layout | template | content
    framework: str
    dynamic: bool = False
    title: str | None = None
    title_template: str | None = None
    description: str | None = None
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    canonical: str | None = None
    robots: str | None = None
    lang: str | None = None
    og: dict[str, str] = field(default_factory=dict)
    twitter: dict[str, str] = field(default_factory=dict)
    hreflang: list[str] = field(default_factory=list)
    jsonld_types: list[str] = field(default_factory=list)
    generates_metadata: bool = False
    images: int = 0
    images_missing_alt: int = 0
    internal_links: list[str] = field(default_factory=list)
    words: int = 0
    top_terms: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    @property
    def indexable(self) -> bool:
        return self.kind in ("page", "content", "template") and not (self.robots and "noindex" in self.robots.lower())


# ---------------------------------------------------------------- file walking


def walk(root: Path, suffixes: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            entries = sorted(cur.iterdir())
        except OSError:
            continue
        for p in entries:
            if p.is_dir():
                if p.name not in SKIP_DIRS and not p.name.startswith("."):
                    stack.append(p)
            elif p.suffix in suffixes:
                found.append(p)
    return found


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ---------------------------------------------------------------- extraction

STR = r"""(?:"([^"]*)"|'([^']*)'|`([^`$]*)`)"""


def _first(m: re.Match[str] | None) -> str | None:
    if not m:
        return None
    for g in m.groups():
        if g:
            return clean(g)
    return None


def clean(text: str) -> str:
    text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&quot;", '"')
    return re.sub(r"\s+", " ", text).strip()


def meta_content(src: str, attr: str, name: str) -> str | None:
    pat = re.compile(
        rf"<meta\b[^>]*\b{attr}\s*=\s*[\"']{re.escape(name)}[\"'][^>]*\bcontent\s*=\s*{STR}"
        rf"|<meta\b[^>]*\bcontent\s*=\s*{STR}[^>]*\b{attr}\s*=\s*[\"']{re.escape(name)}[\"']",
        re.I | re.S,
    )
    return _first(pat.search(src))


def extract(src: str, page: Page) -> None:
    # Next.js / Remix metadata objects:  export const metadata = { title: "...", description: "..." }
    meta_obj = re.search(r"export\s+(?:const|let)\s+metadata\b[^=]*=\s*\{(.*?)\n\}", src, re.S)
    if meta_obj:
        body = meta_obj.group(1)
        page.title = page.title or _first(re.search(rf"\btitle\s*:\s*{STR}", body))
        page.title = page.title or _first(re.search(rf"\bdefault\s*:\s*{STR}", body))
        page.title_template = _first(re.search(rf"\btemplate\s*:\s*{STR}", body))
        page.description = page.description or _first(re.search(rf"\bdescription\s*:\s*{STR}", body))
        page.canonical = page.canonical or _first(re.search(rf"\bcanonical\s*:\s*{STR}", body))
        if re.search(r"\bopenGraph\s*:", body):
            page.og.setdefault("declared", "metadata.openGraph")
        if re.search(r"\btwitter\s*:", body):
            page.twitter.setdefault("declared", "metadata.twitter")
        if re.search(r"\brobots\s*:\s*\{[^}]*index\s*:\s*false", body, re.S):
            page.robots = "noindex"
    if re.search(r"export\s+(async\s+)?function\s+generateMetadata\b|export\s+(const\s+)?meta\s*[:=]", src):
        page.generates_metadata = True

    # Markdown / Astro / MDX frontmatter
    fm = re.match(r"^---\s*\n(.*?)\n---", src, re.S)
    if fm:
        block = fm.group(1)
        page.title = page.title or _first(re.search(r"^title\s*:\s*[\"']?(.+?)[\"']?\s*$", block, re.M))
        page.description = page.description or _first(
            re.search(r"^description\s*:\s*[\"']?(.+?)[\"']?\s*$", block, re.M)
        )
        if re.search(r"^(draft\s*:\s*true|noindex\s*:\s*true)", block, re.M):
            page.robots = "noindex"

    # HTML / JSX / templates
    page.title = page.title or _first(re.search(r"<title[^>]*>\s*(.*?)\s*</title>", src, re.S | re.I))
    page.title = page.title or _first(re.search(r"\{%\s*block\s+title\s*%\}(.*?)\{%\s*endblock", src, re.S))
    page.description = page.description or meta_content(src, "name", "description")
    page.robots = page.robots or meta_content(src, "name", "robots")
    canon = re.search(rf"<link\b[^>]*rel\s*=\s*[\"']canonical[\"'][^>]*href\s*=\s*{STR}", src, re.I)
    page.canonical = page.canonical or _first(canon)
    lang = re.search(rf"<html\b[^>]*\blang\s*=\s*{STR}", src, re.I)
    page.lang = page.lang or _first(lang)
    for prop in ("og:title", "og:description", "og:image", "og:type", "og:url"):
        v = meta_content(src, "property", prop)
        if v:
            page.og[prop] = v
    for name in ("twitter:card", "twitter:title", "twitter:image"):
        v = meta_content(src, "name", name)
        if v:
            page.twitter[name] = v
    page.hreflang = sorted(set(re.findall(r"hreflang\s*=\s*[\"']([\w-]+)[\"']", src, re.I)))

    for block in re.findall(r"application/ld\+json.*?(\{.*?\})\s*(?:</script>|\)|`)", src, re.S | re.I):
        page.jsonld_types += re.findall(r"[\"']@type[\"']\s*:\s*[\"']([\w]+)[\"']", block)
    page.jsonld_types += re.findall(r"[\"']?@type[\"']?\s*:\s*[\"']([A-Z][\w]+)[\"']", src)
    page.jsonld_types = sorted(set(page.jsonld_types))

    page.h1 = [t for t in (clean(h) for h in re.findall(r"<h1\b[^>]*>(.*?)</h1>", src, re.S | re.I)) if t]
    md_h1 = re.findall(r"^#\s+(.+)$", src, re.M) if page.file.endswith((".md", ".mdx")) else []
    page.h1 += [clean(h) for h in md_h1]
    page.title = page.title or (page.h1[0] if md_h1 else None)
    page.h2 = [t for t in (clean(h) for h in re.findall(r"<h2\b[^>]*>(.*?)</h2>", src, re.S | re.I)) if t][:12]
    if page.file.endswith((".md", ".mdx")):
        page.h2 += [clean(h) for h in re.findall(r"^##\s+(.+)$", src, re.M)][:12]

    imgs = re.findall(r"<(?:img|Image|NuxtImg|enhanced:img)\b([^>]*)>", src, re.S)
    page.images = len(imgs) + len(re.findall(r"!\[[^\]]*\]\(", src))
    page.images_missing_alt = sum(1 for a in imgs if not re.search(r"\balt\s*=", a)) + len(re.findall(r"!\[\]\(", src))
    page.internal_links = sorted(set(re.findall(r"""(?:href|to)\s*=\s*\{?["'`](/[^"'`#?\s]*)""", src)))[:50]

    text = visible_text(src)
    words = re.findall(r"[^\W\d_][\w'-]{2,}", text.lower())
    page.words = len(words)
    page.top_terms = top_terms(words)


def visible_text(src: str) -> str:
    src = re.sub(r"^---\s*\n.*?\n---", " ", src, flags=re.S)
    src = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S | re.I)
    src = re.sub(r"^\s*(import|export)\b.*$", " ", src, flags=re.M)
    src = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", " ", src, flags=re.S)
    texts = re.findall(r">([^<>{}]+)<", src)
    if src.lstrip().startswith(("#", "-")) or not texts:
        texts.append(re.sub(r"[`*_>#\[\]()]", " ", src))
    return " ".join(texts)


def top_terms(words: list[str], n: int = 12) -> list[str]:
    words = [w for w in words if w not in STOPWORDS and not w.startswith(("http", "www"))]
    uni = Counter(words)
    bi = Counter(f"{a} {b}" for a, b in pairwise(words) if a != b)
    ranked = [t for t, c in bi.most_common(n) if c > 1] + [t for t, _ in uni.most_common(n)]
    seen: list[str] = []
    for t in ranked:
        if t not in seen:
            seen.append(t)
    return seen[:n]


# ---------------------------------------------------------------- route discovery


def route_from(parts: list[str]) -> tuple[str, bool]:
    out: list[str] = []
    dynamic = False
    for p in parts:
        if p.startswith("(") and p.endswith(")"):
            continue  # route group
        if p.startswith("@") or p.startswith("_"):
            continue  # parallel route / private folder
        if p in ("index", "page", "+page", "_index"):
            continue
        if "[" in p or p.startswith("$") or p.startswith(":"):
            dynamic = True
        out.append(p)
    return "/" + "/".join(out), dynamic


def discover(root: Path) -> tuple[list[Page], set[str]]:
    pages: list[Page] = []
    frameworks: set[str] = set()
    pkg = load_json(root / "package.json")
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})} if pkg else {}

    def add(path: Path, route: str, kind: str, fw: str, dynamic: bool = False) -> None:
        page = Page(route=route, file=str(path.relative_to(root)), kind=kind, framework=fw, dynamic=dynamic)
        extract(read(path), page)
        pages.append(page)
        frameworks.add(fw)

    for app_dir in (root / "app", root / "src" / "app"):
        if app_dir.is_dir() and ("next" in deps or any(app_dir.glob("**/page.*"))):
            for f in walk(app_dir, (".tsx", ".jsx", ".ts", ".js", ".mdx")):
                rel = f.relative_to(app_dir).parts
                if f.stem == "page":
                    r, d = route_from(list(rel[:-1]))
                    add(f, r, "page", "nextjs-app", d)
                elif f.stem == "layout":
                    r, _ = route_from(list(rel[:-1]))
                    add(f, r, "layout", "nextjs-app")
    for pages_dir in (root / "pages", root / "src" / "pages"):
        if not pages_dir.is_dir():
            continue
        fw = "astro" if "astro" in deps else "nuxt" if "nuxt" in deps else "nextjs-pages" if "next" in deps else "pages"
        for f in walk(pages_dir, (".tsx", ".jsx", ".js", ".ts", ".astro", ".md", ".mdx", ".vue")):
            rel = f.relative_to(pages_dir).parts
            if rel[0] == "api" or f.stem.startswith("_"):
                if f.stem in ("_document", "_app"):
                    add(f, "/", "layout", fw)
                continue
            r, d = route_from([*rel[:-1], f.stem])
            add(f, r, "page", fw, d)
    for layouts in (root / "src" / "layouts", root / "layouts"):
        for f in walk(layouts, (".astro", ".vue", ".tsx", ".jsx", ".svelte")) if layouts.is_dir() else []:
            add(f, "*", "layout", "astro" if f.suffix == ".astro" else "layout")
    routes_dir = root / "src" / "routes"
    if routes_dir.is_dir():
        for f in walk(routes_dir, (".svelte",)):
            rel = f.relative_to(routes_dir).parts
            if f.name == "+page.svelte":
                r, d = route_from(list(rel[:-1]))
                add(f, r, "page", "sveltekit", d)
            elif f.name == "+layout.svelte":
                r, _ = route_from(list(rel[:-1]))
                add(f, r, "layout", "sveltekit")
    remix = root / "app" / "routes"
    if remix.is_dir() and ("@remix-run/react" in deps or "react-router" in deps):
        for f in walk(remix, (".tsx", ".jsx")):
            r, d = route_from(f.stem.replace("_index", "").split("."))
            add(f, r, "page", "remix", d)

    seen = {p.file for p in pages}
    for f in walk(root, (".html", ".htm", ".jinja", ".jinja2", ".njk")):
        rel = str(f.relative_to(root))
        if rel in seen:
            continue
        src = read(f)
        is_template = "templates" in f.parts or "{%" in src
        if is_template:
            is_layout = re.search(r"base|layout", f.stem) or ("{% block" in src and "{% extends" not in src)
            kind = "layout" if is_layout else "template"
            add(f, "/" + f.stem if kind == "template" else "*", kind, "django-jinja")
        else:
            r = "/" if f.stem == "index" else "/" + str(f.relative_to(root).with_suffix(""))
            add(f, r.replace("/index", "") or "/", "page", "html")
    for content in (root / "content", root / "docs", root / "src" / "content", root / "blog", root / "posts"):
        if not content.is_dir():
            continue
        for f in walk(content, (".md", ".mdx")):
            if str(f.relative_to(root)) in seen:
                continue
            r, d = route_from([*f.relative_to(content).parts[:-1], f.stem])
            add(f, f"/{content.name}{r if r != '/' else ''}", "content", "markdown", d)
    return pages, frameworks


# ---------------------------------------------------------------- site-level


def load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def first_existing(root: Path, candidates: list[str]) -> str | None:
    for c in candidates:
        if (root / c).exists():
            return c
    return None


def site_signals(root: Path) -> dict:
    statics = ["public", "static", "src/static", "assets", "."]
    app = ["app", "src/app"]

    def find(names: list[str]) -> str | None:
        return first_existing(root, [f"{d}/{n}" for d in statics + app for n in names])

    pkg = load_json(root / "package.json")
    readme = first_existing(root, ["README.md", "readme.md", "README.rst"])
    summary = ""
    if readme:
        paras = [p.strip() for p in re.split(r"\n\s*\n", read(root / readme)) if p.strip()]
        summary = next((clean(p) for p in paras if not p.lstrip().startswith(("#", "!", "[", "<", "```", "|"))), "")
    pyproject = read(root / "pyproject.toml")
    py_desc = re.search(r'^description\s*=\s*"([^"]*)"', pyproject, re.M)
    py_kw = re.search(r"^keywords\s*=\s*\[([^\]]*)\]", pyproject, re.M)
    manifests = walk(root, (".xml",))
    android = [str(m.relative_to(root)) for m in manifests if m.name == "AndroidManifest.xml"][:3]
    return {
        "robots_txt": find(["robots.txt", "robots.ts", "robots.js"]),
        "sitemap": find(["sitemap.xml", "sitemap.ts", "sitemap.js", "sitemap-index.xml"])
        or first_existing(root, ["next-sitemap.config.js", "next-sitemap.config.cjs"]),
        "llms_txt": find(["llms.txt"]),
        "web_manifest": find(["manifest.json", "site.webmanifest", "manifest.webmanifest", "manifest.ts"]),
        "favicon": find(["favicon.ico", "favicon.svg", "icon.png", "icon.svg", "icon.tsx"]),
        "og_image_route": find(["opengraph-image.tsx", "opengraph-image.png", "opengraph-image.jpg", "og.png"]),
        "security_txt": find([".well-known/security.txt"]),
        "indexnow_key": next(
            (
                str(p.relative_to(root))
                for d in statics
                if (root / d).is_dir()
                for p in (root / d).glob("*.txt")
                if re.fullmatch(r"[0-9a-f]{8,128}", p.stem)
            ),
            None,
        ),
        "product": {
            "name": pkg.get("name") or (re.search(r'^name\s*=\s*"([^"]*)"', pyproject, re.M) or [None, None])[1],
            "description": pkg.get("description") or (py_desc.group(1) if py_desc else None) or summary[:300] or None,
            "keywords": pkg.get("keywords") or ([k.strip(" '\"") for k in py_kw.group(1).split(",")] if py_kw else []),
            "homepage": pkg.get("homepage"),
            "readme": readme,
        },
        "android_manifests": android,
        "context7": first_existing(root, ["context7.json"]),
    }


# ---------------------------------------------------------------- audit


def audit(pages: list[Page], site: dict) -> list[str]:
    layouts = [p for p in pages if p.kind == "layout"]
    layout_title = any(p.title or p.title_template for p in layouts)
    layout_desc = any(p.description for p in layouts)
    layout_lang = any(p.lang for p in layouts) or any(p.lang for p in pages)
    titles: Counter[str] = Counter()
    descs: Counter[str] = Counter()
    for p in pages:
        if not p.indexable:
            continue
        inherited = p.generates_metadata
        if not p.title and not inherited:
            p.issues.append("missing-title" + ("" if not layout_title else " (inherits layout default only)"))
        if p.title:
            titles[p.title] += 1
            if len(p.title) > TITLE_MAX:
                p.issues.append(f"title-too-long ({len(p.title)}>{TITLE_MAX})")
        if not p.description and not inherited:
            p.issues.append("missing-description" + ("" if not layout_desc else " (inherits layout default only)"))
        if p.description:
            descs[p.description] += 1
            if not DESC_MIN <= len(p.description) <= DESC_MAX:
                p.issues.append(f"description-length ({len(p.description)}, want {DESC_MIN}-{DESC_MAX})")
        if p.kind != "layout" and len(p.h1) == 0 and p.framework not in ("django-jinja",):
            p.issues.append("no-h1")
        if len(p.h1) > 1:
            p.issues.append(f"multiple-h1 ({len(p.h1)})")
        if p.images_missing_alt:
            p.issues.append(f"images-missing-alt ({p.images_missing_alt})")
        if p.words and p.words < 150 and p.kind in ("page", "content") and not p.dynamic:
            p.issues.append(f"thin-content (~{p.words} words)")
    for p in pages:
        if p.title and titles[p.title] > 1:
            p.issues.append("duplicate-title")
        if p.description and descs[p.description] > 1:
            p.issues.append("duplicate-description")

    site_issues = []
    if pages and not site["robots_txt"]:
        site_issues.append("no robots.txt / robots route")
    if pages and not site["sitemap"]:
        site_issues.append("no sitemap.xml / sitemap route")
    if pages and not site["llms_txt"]:
        site_issues.append("no llms.txt (optional, low-cost for AI answer engines)")
    if pages and not layout_lang:
        site_issues.append("no <html lang> found")
    if pages and not any(p.canonical for p in pages) and not any("metadataBase" in read_safe(p) for p in layouts):
        site_issues.append("no canonical URLs declared")
    if pages and not any(p.og for p in pages) and not site["og_image_route"]:
        site_issues.append("no Open Graph metadata")
    if pages and not any(p.jsonld_types for p in pages):
        site_issues.append("no JSON-LD structured data")
    if not site["web_manifest"] and any(p.framework != "markdown" for p in pages):
        site_issues.append("no web app manifest")
    return site_issues


_ROOT: Path = Path(".")


def read_safe(p: Page) -> str:
    return read(_ROOT / p.file)


# ---------------------------------------------------------------- output


def to_markdown(data: dict) -> str:
    lines = ["# SEO Context (generated by tools/seo_context.py)", ""]
    lines += [
        "> Deterministic inventory. The SEO Strategist agent extends this file with keyword clusters,",
        "> entities, per-page metadata, structured data, and channel plans (see workflows/SEOContextGeneration.md).",
        "",
        "## Product",
        "",
    ]
    prod = data["site"]["product"]
    for k in ("name", "description", "homepage", "keywords"):
        lines.append(f"- **{k}**: {prod.get(k) or '_unknown_'}")
    lines += ["", f"Frameworks: {', '.join(data['frameworks']) or 'none detected'}", "", "## Site signals", ""]
    for k, v in data["site"].items():
        if k != "product":
            lines.append(f"- {k}: {v or '—'}")
    lines += ["", "## Site-level gaps", ""]
    lines += [f"- [ ] {i}" for i in data["site_issues"]] or ["- none"]
    lines += [
        "",
        "## Routes",
        "",
        "| Route | Kind | Title | Description | H1 | JSON-LD | Issues |",
        "|---|---|---|---|---|---|---|",
    ]
    for p in data["pages"]:

        def cut(s: str | None, n: int = 48) -> str:
            return "—" if not s else (s[: n - 1] + "…" if len(s) > n else s).replace("|", "\\|")

        lines.append(
            f"| `{p['route']}`{' (dyn)' if p['dynamic'] else ''} | {p['kind']} | {cut(p['title'])} | "
            f"{cut(p['description'])} | {cut(p['h1'][0] if p['h1'] else None, 32)} | "
            f"{', '.join(p['jsonld_types']) or '—'} | {', '.join(p['issues']) or 'ok'} |"
        )
    lines += ["", "## Seed terms (from visible copy)", ""]
    lines.append(", ".join(data["seed_terms"]) or "_none — copy is thin or rendered at runtime_")
    lines += [
        "",
        "## Agent TODO",
        "",
        "- [ ] Audience, intents, and keyword clusters per route (head / mid / long-tail, questions)",
        "- [ ] Entity map (organization, product, people, places) → schema.org types",
        "- [ ] Per-route title / meta description / H1 / canonical / OG / Twitter drafts",
        "- [ ] JSON-LD blocks per template (Organization, WebSite, Product/SoftwareApplication, Article, FAQPage, BreadcrumbList …)",
        "- [ ] robots, sitemap, llms.txt, hreflang plan",
        "- [ ] Channel plan: Google/Bing, AI answer engines, app stores, GitHub/registries, video, social, local",
        "- [ ] Measurement: Search Console, Bing Webmaster Tools, IndexNow, Core Web Vitals field data",
        "",
    ]
    return "\n".join(lines)


def build(root: Path) -> dict:
    global _ROOT
    _ROOT = root
    pages, frameworks = discover(root)
    site = site_signals(root)
    site_issues = audit(pages, site)
    all_terms: Counter[str] = Counter()
    for p in pages:
        all_terms.update(p.top_terms)
    return {
        "generator": "rigor-os/tools/seo_context.py",
        "root": str(root),
        "frameworks": sorted(frameworks),
        "site": site,
        "site_issues": site_issues,
        "pages": [{**asdict(p), "indexable": p.indexable} for p in sorted(pages, key=lambda x: (x.route, x.kind))],
        "seed_terms": [t for t, _ in all_terms.most_common(30)],
    }


def default_out_dir(root: Path) -> Path:
    """Same rule as bootstrap.py: vendored or plugin installs use rigor-os/project-context."""
    if not (root / "rigor-os").is_dir() and (root / "constitution").is_dir() and (root / "skills").is_dir():
        return root / "project-context"  # Rigor OS contents at the repository root
    return root / "rigor-os" / "project-context"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--base-url", help="Production origin, recorded for the agent (e.g. https://example.com)")
    ap.add_argument("--check", action="store_true", help="Exit 1 if an indexable page lacks title/description")
    ap.add_argument("--stdout", action="store_true", help="Print JSON instead of writing files")
    args = ap.parse_args(argv)

    root = args.root.resolve()
    data = build(root)
    data["base_url"] = args.base_url
    if args.stdout:
        print(json.dumps(data, indent=2))
    else:
        out = (args.out_dir or default_out_dir(root)).resolve()
        out.mkdir(parents=True, exist_ok=True)
        (out / "SEO_CONTEXT.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        md = out / "SEO_CONTEXT.md"
        marker = "<!-- agent-notes -->"
        keep = (
            read(md).split(marker, 1)[1]
            if md.exists() and marker in read(md)
            else "\n_The SEO agent writes below this line; reruns keep it._\n"
        )
        md.write_text(to_markdown(data) + "\n" + marker + keep, encoding="utf-8")
        print(
            f"Wrote {out / 'SEO_CONTEXT.json'} and {md} — {len(data['pages'])} files, "
            f"{sum(1 for p in data['pages'] if p['issues'])} with issues, {len(data['site_issues'])} site gaps"
        )

    if args.check:
        bad = [
            p
            for p in data["pages"]
            if p["indexable"]
            and any(i.startswith(("missing-title", "missing-description")) and "inherits" not in i for i in p["issues"])
        ]
        for p in bad:
            print(f"SEOGate: {p['file']} ({p['route']}): {', '.join(p['issues'])}", file=sys.stderr)
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
