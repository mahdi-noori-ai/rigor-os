# Skill: UI Design Quality

```
Name: ui-design-quality
Domain: frontend / UX
Purpose: Professional-looking interfaces — not generic AI/robot defaults
Trigger: New screens, redesigns, empty states, marketing-adjacent UI, dashboards, forms
Do Not Trigger: Invisible backend changes
```

## Goal

Interfaces should look designed by a product team: hierarchy, rhythm, restraint.

## Non-negotiables

1. **One visual system.** Spacing scale, type scale, radius, shadows from existing tokens or sibling screens.
2. **Hierarchy.** One primary action per view. Secondary actions quieter.
3. **Alignment.** Consistent inset (e.g. 16/24), baseline grid feel, no accidental 13px gaps mixed with 20px.
4. **Typography.** Limited sizes/weights. Readable line length. No decorative fonts unless already in the app.
5. **Color.** Use semantic tokens (text-muted, danger, success). Avoid rainbow gradients and neon unless brand already does.
6. **Density.** Tables and admin tools denser; marketing and onboarding more spacious — match product type.
7. **Affordances.** Buttons look clickable; links look like links; destructive is clearly destructive.
8. **Empty states.** Helpful copy + action, not a blank card.
9. **Motion.** Subtle or none. No bounce-in on every card.

## Reject (AI slop)

- Inter/Roboto + purple gradient hero + three equal feature cards with stock icons
- Inconsistent corner radii (4, 8, 12, 16 in one form)
- Placeholder gray boxes left in the layout
- Comic copy ("Oopsie! Something went wrong 😅") unless brand voice is that
- Icons from three different sets

## Procedure

1. Screenshot or read 2–3 existing polished screens.
2. List tokens: colors, type, space, radius.
3. Implement using those tokens only.
4. Check 375 / 768 / 1280.
5. Compare visually to siblings; adjust until it belongs in the same product.

## Related

`frontend-ui-quality`, `accessibility`
