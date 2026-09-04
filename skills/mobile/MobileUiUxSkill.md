# Skill: Mobile UI / UX (Android & game HUD)

```
Name: mobile-ui-ux
Domain: mobile
Purpose: Touch-first, clear, non-robotic mobile UI — apps and game menus/HUD
Trigger: Android screens, Compose UI, game menus, HUD, dialogs, onboarding
Do Not Trigger: Backend-only; desktop web-only
```

## Non-negotiables

1. Reuse theme/components (Material 3 / project design system / game UI kit).
2. Touch targets large enough; primary actions thumb-reachable on phones.
3. Loading / empty / error / offline states.
4. System bars, cutouts, keyboard insets handled as siblings do.
5. Game HUD: readability over decoration; don't obscure critical gameplay.
6. Support system font scale reasonably (apps); games document if bitmap fonts are fixed.

## App UI

- Navigation consistent with platform (back stack, predictive back if project uses it).
- Forms: validation, IME actions, scroll to first error.
- Destructive actions: confirm.
- Dark theme: follow existing day/night setup.

## Game menus / HUD

- Pause / resume / reconnect flows explicit.
- Settings: audio, language, account, legal — don't bury quit/logout.
- Tutorial/FTUE: skippable if product allows; don't trap users.
- Safe areas on notched devices.

## Anti-patterns

- Desktop web layout squeezed onto phone
- Tiny icons with no hit padding
- Modal spam on every error
- Inconsistent button styles across scenes

## Related

`android-app`, `mobile-game`, `ui-design-quality` (visual craft), `accessibility` (where applicable)
