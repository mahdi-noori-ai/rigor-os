---
name: mobile-game
description: Implement mobile game features on Android (Unity/Godot/native) with server-authoritative economy/score/IAP when online. Use for gameplay, HUD, levels, leaderboards, in-game purchases.
---

# Mobile game

Follow `${CLAUDE_PLUGIN_ROOT}/workflows/MobileGameFeature.md` and:

- `${CLAUDE_PLUGIN_ROOT}/skills/mobile/MobileGameSkill.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/mobile/MobileBackendApiSkill.md`
- Engine overlay under `${CLAUDE_PLUGIN_ROOT}/skills/mobile/overlays/`
- `${CLAUDE_PLUGIN_ROOT}/quality-gates/MobileGate.md`

Never trust the client alone for currency, score, or entitlements.
