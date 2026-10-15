# Skill: SEO Context Generation

```
Name: seo-context
Domain: growth / web
Purpose: Turn the product's layouts, pages, and copy into a complete, evidence-based SEO context —
         metadata, structured data, crawl files, and a plan for every search surface the product publishes to
Trigger: Public pages, landing/marketing/docs/blog work, new routes or layouts, launches, "SEO", "rank",
         "metadata", "Open Graph", "schema", "sitemap", "AI Overviews / answer engines", app store listing,
         README/registry discoverability
Do Not Trigger: Internal admin/dashboards behind auth, API-only services, T0 copy fixes on noindex pages
```

## Non-negotiables

1. **Extract before you write.** Run `tools/seo_context.py` first; every recommendation cites a route or file from `SEO_CONTEXT.json`.
2. **People-first content.** Google's own guidance: AI Overviews / AI Mode need no special markup — a page must be indexable and snippet-eligible. So fundamentals first; "GEO tricks" never replace useful content.
3. **Truthful metadata.** Titles, descriptions, and structured data describe what is actually on the page. No fake reviews, ratings, FAQs, or prices in JSON-LD.
4. **One owner per signal.** Metadata lives in the framework's mechanism (Next.js `metadata`/`generateMetadata`, Astro layout props, Django `{% block %}`), not hand-pasted `<meta>` in many files.
5. **Deterministic gate.** `seo_context.py --check` must pass for indexable routes before DONE (see `quality-gates/SEOGate.md`).
6. **Measure.** Ship with a way to observe impact (Search Console, Bing Webmaster Tools, Core Web Vitals field data) — otherwise it is opinion.

## Sources of search traffic (cover what applies)

| Surface | What the context must specify |
|---------|-------------------------------|
| Google / Bing web search | Indexability, canonical, title ≤ ~60 chars, description 70–160, one H1, internal links, sitemap, robots |
| AI answer engines (Google AI Overviews & AI Mode, Bing Copilot, ChatGPT search, Perplexity, Claude) | Answer-first sections, clear entities, cited facts with dates, FAQ-style H2s that mirror real questions, `llms.txt` (optional, low cost), crawler policy per bot in `robots.txt` |
| Rich results | JSON-LD: `Organization`, `WebSite` (+ `SearchAction` if site search), `BreadcrumbList`, `Product`/`SoftwareApplication`/`Offer`, `Article`/`BlogPosting`, `FAQPage`/`HowTo` only where the content truly is that, `VideoObject`, `Event`, `LocalBusiness` |
| Social / link previews | Open Graph (`og:title`, `og:description`, `og:image` 1200×630, `og:type`, `og:url`), Twitter/X card |
| Image & video search | Descriptive filenames, `alt`, width/height, `VideoObject`, captions/transcripts |
| International | `hreflang` + `x-default`, `<html lang>`, locale-specific URLs, RTL where needed (fa/ar/he) |
| Local | `LocalBusiness` schema, NAP consistency, Google Business Profile |
| App stores (Android/Play) | ASO: title (30), short description (80), full description keywords, screenshots captions, deep links / App Links `assetlinks.json` |
| Developer surfaces | GitHub repo description + topics, README first paragraph, package registry keywords (npm/PyPI/crates), docs site, Context7 (`context7.json`) |
| Discovery speed | XML sitemap with `lastmod`, IndexNow key for Bing/Yandex, Search Console sitemap submission |

## Procedure

1. **Inventory** — `python3 rigor-os/tools/seo_context.py [--base-url https://…]` → `project-context/SEO_CONTEXT.{json,md}`.
2. **Understand the product** — read `PROJECT_CONTEXT.md`, README, pricing/landing copy; write the one-sentence positioning and the 3–5 audiences.
3. **Intent & keyword clusters** — per indexable route: primary intent (informational / commercial / transactional / navigational), one primary query, 3–8 secondary/long-tail and question queries. Use only evidence you have (product copy, seed terms, user-provided data, Search Console exports); label anything else *hypothesis*.
4. **Entity map** — organization, product(s), people, places, concepts → schema.org types and `sameAs` profiles.
5. **Per-route spec** — title, description, H1, canonical, OG/Twitter, JSON-LD type, internal links in/out. Use `templates/SEOContext.md`.
6. **Site files** — `robots.txt` (with sitemap line and AI-crawler policy the owner chose), `sitemap.xml` or framework route, `llms.txt`, web manifest, favicon/icons, OG image route.
7. **Implement** in the framework's native mechanism, mirroring sibling pages (Principle 1). Keep JSON-LD generated from the same data the page renders.
8. **Verify** — rerun `seo_context.py --check`; build and fetch the rendered HTML (`curl -s localhost:…/route | grep -i '<title\|og:\|ld+json'`) because client-only metadata is invisible to many crawlers; validate JSON-LD (Rich Results Test / schema.org validator when online); Lighthouse SEO + Core Web Vitals (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1).
9. **Record** decisions under the `<!-- agent-notes -->` marker in `SEO_CONTEXT.md` (reruns preserve it).

## Framework notes

- **Next.js App Router**: root `layout.tsx` sets `metadataBase`, `title.template`, default description, `openGraph`; pages export `metadata` or `generateMetadata`; `app/sitemap.ts`, `app/robots.ts`, `app/opengraph-image.tsx`. Server-render metadata — never set titles in `useEffect`.
- **Vite/React SPA**: metadata rendered client-side is weak for crawlers and link unfurlers. Prerender marketing routes (or move them to an SSR/SSG framework) before polishing tags.
- **Astro / SvelteKit / Nuxt**: put SEO props in the shared layout; pages pass title/description.
- **Django**: base template blocks `{% block title %}`, `{% block meta_description %}`, canonical via `request.build_absolute_uri`; `django.contrib.sitemaps`.
- **Docs (Markdown)**: front-matter `title`/`description` on every page; first paragraph answers the page's question.

## Anti-patterns

- Keyword stuffing, doorway pages, auto-generated thin pages per keyword
- Same title/description on every route; titles set only in a client effect
- `FAQPage`/`Review` markup for content that is not on the page
- Blocking CSS/JS or the whole site in `robots.txt` on staging config that ships to prod
- `noindex` + canonical to another URL on the same page (conflicting signals)
- Shipping a sitemap that lists redirects, 404s, or noindexed URLs

## Output

- `project-context/SEO_CONTEXT.md` (inventory + agent notes) and `SEO_CONTEXT.json`
- Code changes for metadata, JSON-LD, crawl files
- SEOGate evidence block (see gate)

## Related

`agents/seo-strategist/SEOStrategistSpec.md`, `workflows/SEOContextGeneration.md`, `quality-gates/SEOGate.md`, `templates/SEOContext.md`, `frontend-ui-quality`, `performance`, `accessibility`, `mobile-release` (ASO)
