# Workflow: SEO Context Generation

**Tier:** T2 (T3 for launches, rebrands, multi-locale sites) · **Agent:** SEO Strategist (opt-in) · **Gate:** SEOGate

## When

- A public route, layout, or template is added or changed
- Launch / rebrand / pricing change / docs or blog launch
- User asks for SEO, metadata, social previews, schema, sitemap, AI search visibility, or store listing

## Steps

```
1. Extract      python3 rigor-os/tools/seo_context.py --base-url <prod origin>
2. Context      SEO Strategist reads SEO_CONTEXT.json + PROJECT_CONTEXT + copy → positioning, audiences
3. Clusters     intent + query clusters per indexable route (evidence or "hypothesis")
4. Spec         per-route metadata + JSON-LD + links  (templates/SEOContext.md)
5. Site files   robots · sitemap · llms.txt · hreflang · manifest · OG image
6. Channels     web · AI answer engines · rich results · social · app store · GitHub/registries · video
7. Implement    Orchestrator applies the spec in the framework's native metadata mechanism
8. Verify       seo_context.py --check · rendered-HTML fetch · JSON-LD validation · Lighthouse/CWV
9. Record       decisions under <!-- agent-notes --> in SEO_CONTEXT.md
```

## Handoff contract (Orchestrator → SEO Strategist)

```yaml
task: "SEO context for the new pricing and docs sections"
base_url: "https://example.com"
routes_changed: [/pricing, /docs/*]
audiences_known: ["small SaaS teams", "agencies"]
locales: [en, fa]
constraints: "No AI-crawler blocking decided yet — ask the owner"
evidence_files: [project-context/SEO_CONTEXT.json]
```

## Evidence block (attach before DONE)

```text
SEO:
  seo_context.py --check: PASS (14 indexable routes, 0 missing title/description)
  rendered HTML: /, /pricing, /docs/install show <title>, description, canonical, og:image, JSON-LD
  JSON-LD types: Organization, WebSite, SoftwareApplication, BreadcrumbList, FAQPage(/pricing)
  site files: robots.txt (+Sitemap), sitemap.xml (14 URLs, lastmod), llms.txt
  Lighthouse SEO: 100 · LCP 1.9s · INP 120ms · CLS 0.02 (lab)
```

## Skip conditions

Auth-only/internal apps; API-only changes; T0 copy edits on pages that already pass the gate.
