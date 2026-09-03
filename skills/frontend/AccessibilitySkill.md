# Skill: Accessibility

```
Name: accessibility
Domain: frontend
Purpose: WCAG 2.1 AA practical checks for generated UI
Trigger: New interactive UI, forms, dialogs, navigation
Do Not Trigger: Non-UI changes
```

## Checks

- Semantic HTML: `button`, `nav`, `main`, headings in order
- Labels bound to inputs (`htmlFor` / `aria-labelledby`)
- Keyboard: all actions reachable; visible focus; Escape closes dialogs; focus trap in modals
- Images: meaningful `alt` or empty alt if decorative
- Contrast: text vs background (existing tokens usually OK — don't introduce light-gray on white)
- Don't rely on color alone for errors
- `aria-live` for async errors when the project already uses it

## Do not

- Sprinkle `aria-*` on everything
- `div onClick` as a button
- Remove focus outlines
