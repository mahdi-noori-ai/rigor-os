---
name: seo-context
description: Generate SEO context from layouts and pages — metadata, JSON-LD, Open Graph, sitemap, robots, llms.txt, and plans for Google, Bing, AI answer engines, app stores, and GitHub/registries. Use for public pages, landing/docs/blog work, launches, social previews, or any SEO request. Skip for auth-only or internal apps.
---

# SEO context

1. Run `python3 rigor-os/tools/seo_context.py` → `rigor-os/project-context/SEO_CONTEXT.{json,md}`.
2. Follow `rigor-os/workflows/SEOContextGeneration.md` and `rigor-os/skills/seo/SEOContextSkill.md`.
3. For launches or many routes, delegate to the **seo-strategist** agent (`rigor-os/agents/seo-strategist/SEOStrategistSpec.md`).
4. Implement in the framework's native metadata mechanism; mirror sibling pages.
5. Gate: `python3 rigor-os/tools/seo_context.py --check` + `rigor-os/quality-gates/SEOGate.md`.

Never invent search volumes, reviews, or ratings. Mark unverified keyword ideas as *hypothesis*.
