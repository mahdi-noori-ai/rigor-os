# SEO Gate

Applies when a change adds or alters a **public, indexable** route, layout, or template. Skip for
auth-only screens, internal tools, and API-only work.

## Deterministic (must pass)

```bash
python3 rigor-os/tools/seo_context.py --check
```

Fails when an indexable page has neither its own nor a generated (`generateMetadata`) title/description.

## Checklist

### Every indexable route
- [ ] Unique `<title>` (≤ ~60 chars) and meta description (70–160) rendered **server-side**
- [ ] Exactly one H1 that matches the page intent
- [ ] Canonical URL (absolute, self-referencing unless deliberately consolidated)
- [ ] Open Graph + Twitter card with a real 1200×630 image
- [ ] Images: `alt`, explicit dimensions, modern format, lazy below the fold
- [ ] Internal links to and from at least one related route

### Site level (once per site)
- [ ] `<html lang>` (and `dir="rtl"` for fa/ar/he)
- [ ] `robots.txt` with `Sitemap:` line; AI-crawler policy is an explicit owner decision
- [ ] XML sitemap of canonical, 200-status, indexable URLs with `lastmod`
- [ ] JSON-LD `Organization` + `WebSite`; page-type schema only where content matches
- [ ] `hreflang` + `x-default` for multi-locale sites
- [ ] `llms.txt` (optional) listing the pages answer engines should read first
- [ ] Staging/preview deployments are `noindex` (header or meta) — production is not

### Performance & UX (Core Web Vitals, field data where available)
- [ ] LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1 on mobile

## Evidence

Attach the SEO evidence block from `workflows/SEOContextGeneration.md`. A missing title/description on
an indexable route, `noindex` leaking to production, or invalid JSON-LD **blocks DONE**.
