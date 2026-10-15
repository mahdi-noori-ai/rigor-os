# SEO Context — agent section template

Paste below `<!-- agent-notes -->` in `project-context/SEO_CONTEXT.md` and fill. Mark anything not backed
by evidence as *(hypothesis)*.

## Positioning

- One sentence:
- Audiences (3–5):
- Differentiators (provable):
- Brand/entity names and `sameAs` profiles (GitHub, LinkedIn, X, YouTube, Play Store, Wikipedia/Wikidata):

## Locales

| Locale | URL pattern | Direction | hreflang |
|--------|-------------|-----------|----------|
| en | / | ltr | en, x-default |

## Route specs

| Route | Intent | Primary query | Secondary / questions | Title (≤60) | Description (70–160) | H1 | Canonical | JSON-LD | Links in → out |
|-------|--------|---------------|-----------------------|-------------|----------------------|----|-----------|---------|----------------|
| / | navigational/commercial | | | | | | | Organization, WebSite | |

## Structured data snippets

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#org", "name": "Example", "url": "https://example.com",
      "logo": "https://example.com/logo.png", "sameAs": ["https://github.com/example"] },
    { "@type": "WebSite", "@id": "https://example.com/#website", "url": "https://example.com", "name": "Example",
      "publisher": { "@id": "https://example.com/#org" } }
  ]
}
```

## Site files

- robots.txt — allow/deny per crawler (Googlebot, Bingbot, GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended …) **as decided by the owner**; `Sitemap:` line
- sitemap — source of truth (framework route / generator), included sections, `lastmod` source
- llms.txt — see `templates/llms.txt`
- Manifest / icons / OG image route

## Channels

| Channel | Applies? | Action | Owner |
|---------|----------|--------|-------|
| Google Search + Search Console | | | |
| Bing + Webmaster Tools + IndexNow | | | |
| AI answer engines | | answer-first copy, entities, llms.txt | |
| Play Store ASO | | title 30 · short 80 · screenshots | |
| GitHub / package registries | | description, topics, keywords | |
| YouTube / video | | | |
| Social previews | | OG/Twitter validated | |

## Measurement

- Target queries to watch:
- Dashboards: Search Console, Bing WMT, CWV (CrUX / RUM)
- Review cadence:

## Implementation checklist (for the Orchestrator)

- [ ] file → change
