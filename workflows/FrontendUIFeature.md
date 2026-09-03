# Frontend / UI Feature Workflow

Never consider UI complete because it "looks okay" at one desktop width.

## Flow

```
Find sibling screens / design tokens
    → Information hierarchy and flow
    → Implement with existing components
    → States: loading, empty, error, success, disabled
    → Responsive: mobile, tablet, desktop
    → Accessibility: keyboard, labels, contrast
    → Integrate real API (not placeholders)
    → Visual consistency check
```

## Non-Negotiables

1. Reuse existing design system / component library. Do not invent a second button style.
2. Professional visual quality — spacing, type scale, alignment. Reject default "AI slop" (generic cards, rainbow gradients, inconsistent padding).
3. Forms: client validation + server error mapping.
4. Destructive actions: confirmation.
5. Focus management for dialogs.

## Skills

- `frontend-ui-quality`
- `ui-design-quality`
- `accessibility`
- `contract-integrity` if new API

## Verification

- 375px, 768px, 1280px (or project breakpoints)
- Keyboard-only path through the feature
- Empty and error states visible
