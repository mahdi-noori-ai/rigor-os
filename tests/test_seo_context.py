import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import seo_context  # noqa: E402


def write(base: Path, rel: str, text: str) -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_next_site(root: Path) -> None:
    write(
        root,
        "package.json",
        json.dumps(
            {
                "name": "acme-analytics",
                "description": "Privacy-first product analytics for small teams.",
                "keywords": ["analytics", "privacy"],
                "dependencies": {"next": "16.0.0", "react": "19.0.0"},
            }
        ),
    )
    write(
        root,
        "app/layout.tsx",
        """
export const metadata = {
  metadataBase: new URL("https://acme.example"),
  title: { default: "Acme Analytics", template: "%s | Acme" },
  description: "Privacy-first product analytics for small teams that want answers without cookies or bloat.",
  openGraph: { images: ["/og.png"] },
}
export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>
}
""",
    )
    write(
        root,
        "app/page.tsx",
        """
export const metadata = {
  title: "Privacy-first product analytics",
  description: "Cookie-free product analytics with funnels, retention, and dashboards your whole team can read.",
}
export default function Home() {
  return (<main>
    <h1>Product analytics without cookies</h1>
    <h2>Funnels</h2>
    <img src="/hero.png" />
    <a href="/pricing">Pricing</a>
    <script type="application/ld+json">{JSON.stringify({"@context": "https://schema.org", "@type": "SoftwareApplication"})}</script>
  </main>)
}
""",
    )
    write(
        root,
        "app/(marketing)/pricing/page.tsx",
        """
export default function Pricing() { return <main><h1>Pricing</h1><p>Simple plans.</p></main> }
""",
    )
    write(
        root,
        "app/blog/[slug]/page.tsx",
        """
export async function generateMetadata({ params }) { return { title: params.slug } }
export default function Post() { return <article><h1>Post</h1></article> }
""",
    )
    write(root, "app/api/health/route.ts", "export function GET() {}")
    write(root, "public/robots.txt", "User-agent: *\nAllow: /\n")
    write(root, "node_modules/x/index.html", "<title>ignored</title>")


def test_next_app_router_inventory(tmp_path):
    make_next_site(tmp_path)
    data = seo_context.build(tmp_path)
    routes = {(p["route"], p["kind"]): p for p in data["pages"]}

    assert "nextjs-app" in data["frameworks"]
    assert ("/", "layout") in routes and ("/", "page") in routes
    assert ("/pricing", "page") in routes, "route groups must be stripped"
    assert routes[("/blog/[slug]", "page")]["dynamic"] is True
    assert routes[("/blog/[slug]", "page")]["generates_metadata"] is True
    assert not any("node_modules" in p["file"] for p in data["pages"])

    home = routes[("/", "page")]
    assert home["title"] == "Privacy-first product analytics"
    assert home["h1"] == ["Product analytics without cookies"]
    assert "SoftwareApplication" in home["jsonld_types"]
    assert home["images_missing_alt"] == 1
    assert "/pricing" in home["internal_links"]

    layout = routes[("/", "layout")]
    assert layout["title_template"] == "%s | Acme"
    assert layout["lang"] == "en"

    pricing = routes[("/pricing", "page")]
    assert any(i.startswith("missing-title") for i in pricing["issues"])

    assert data["site"]["robots_txt"] == "public/robots.txt"
    assert data["site"]["product"]["name"] == "acme-analytics"
    assert any("sitemap" in i for i in data["site_issues"])
    assert any("llms.txt" in i for i in data["site_issues"])


def test_html_django_and_markdown(tmp_path):
    write(
        tmp_path,
        "index.html",
        """<!doctype html><html lang="fa"><head>
<title>Shop</title><meta name="description" content="Short">
<link rel="canonical" href="https://shop.example/">
<meta property="og:title" content="Shop"></head><body><h1>Shop</h1><h1>Again</h1></body></html>""",
    )
    write(
        tmp_path,
        "templates/base.html",
        "<html lang='en'>{% block title %}Base{% endblock %}{% block content %}{% endblock %}</html>",
    )
    write(tmp_path, "templates/product.html", "{% extends 'base.html' %}{% block title %}Product{% endblock %}")
    write(
        tmp_path,
        "docs/guide/install.md",
        "---\ntitle: Install guide\ndescription: How to install the thing on Linux, macOS and Windows in under five minutes, step by step.\n---\n# Install\n\n## Linux\n",
    )
    data = seo_context.build(tmp_path)
    by_file = {p["file"]: p for p in data["pages"]}

    home = by_file["index.html"]
    assert home["route"] == "/" and home["lang"] == "fa"
    assert home["canonical"] == "https://shop.example/"
    assert home["og"]["og:title"] == "Shop"
    assert "multiple-h1 (2)" in home["issues"]
    assert any(i.startswith("description-length") for i in home["issues"])

    assert by_file["templates/base.html"]["kind"] == "layout"
    assert by_file["templates/product.html"]["title"] == "Product"

    doc = by_file["docs/guide/install.md"]
    assert doc["route"] == "/docs/guide/install" and doc["title"] == "Install guide"
    assert doc["h2"] == ["Linux"]


def test_cli_writes_files_and_keeps_agent_notes(tmp_path):
    make_next_site(tmp_path)
    out = tmp_path / "ctx"
    assert seo_context.main(["--root", str(tmp_path), "--out-dir", str(out)]) == 0
    md = out / "SEO_CONTEXT.md"
    md.write_text(md.read_text() + "\nKeyword cluster: cookie-free analytics\n")
    seo_context.main(["--root", str(tmp_path), "--out-dir", str(out)])
    assert "Keyword cluster: cookie-free analytics" in md.read_text()
    assert json.loads((out / "SEO_CONTEXT.json").read_text())["pages"]


def test_check_mode_fails_on_missing_metadata(tmp_path):
    write(tmp_path, "about.html", "<html><body><h1>About</h1></body></html>")
    assert seo_context.main(["--root", str(tmp_path), "--stdout", "--check"]) == 1
    write(
        tmp_path, "about.html", "<html><head><title>About us</title><meta name='description' content='x'></head></html>"
    )
    assert seo_context.main(["--root", str(tmp_path), "--stdout", "--check"]) == 0
