# Skill: Frontend UI Quality

```
Name: frontend-ui-quality
Domain: frontend
Purpose: Production-quality UI behavior — components, states, responsive, API integration
Trigger: React/Next/TSX/JSX/CSS UI work
Do Not Trigger: Backend-only, infra-only
```

## Non-negotiables

1. Reuse existing components and tokens.
2. Never complete at a single desktop width.
3. Implement loading, empty, error, disabled, and success states.
4. Integrate the real API — no fake placeholders left in production paths.
5. Handle races (ignore stale responses / abort controllers) as siblings do.

## Component architecture

- Clear boundaries: page vs feature vs primitive.
- Colocate styles/tests as the repo does.
- Lift state only as far as needed.

## Responsive

Mobile / tablet / desktop. No horizontal scroll unless design requires it. Touch targets ≥ 44px when the design system says so.

## Forms & async

- Validate on submit (and as the project does on blur).
- Map server field errors to inputs.
- Disable double-submit.

## Performance (basic)

- Don't fetch waterfalls if sibling screens batch.
- Images: explicit size, modern format, lazy below fold, priority for the LCP image.
- Budget: LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1 on mobile.

## Public pages (SEO)

Public, indexable routes need server-rendered title/description/canonical/OG and one H1 — run `seo-context` (`skills/seo/SEOContextSkill.md`) and `SEOGate`.

## Anti-patterns

- `div` soup instead of semantic elements
- Ignoring 401/403
- Copy-pasting a third button style
- "Looks fine on my canvas" as done
