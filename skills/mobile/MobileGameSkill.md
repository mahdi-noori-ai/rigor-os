# Skill: Mobile Game (Android)

```
Name: mobile-game
Domain: mobile / game
Purpose: Ship playable Android game features with stable loops, fair client/server rules, and performant frames
Trigger: Mobile game, Unity/Godot/native game feature, HUD, levels, score, economy, IAP, matchmaking client
Do Not Trigger: Pure CRUD admin web; non-game Android utility with no gameplay
```

## Non-negotiables

1. **Gameplay authority:** Never trust the client alone for score, currency, inventory, match outcome, or IAP entitlement — validate on backend when the game has a server.
2. Match existing engine/project structure (Unity scenes/assemblies, Godot scenes, custom engine folders).
3. Target frame budget: avoid hitching; profile before “optimizing.”
4. Separate **game simulation** from **UI/HUD** and from **network**.
5. Offline / poor network: queue or degrade gracefully; never corrupt local save silently.
6. Build must run on a real or emulator Android target used by the project.

## Engine-agnostic layout

```
gameplay/     # rules, entities, systems
ui-hud/       # menus, HUD, not core sim
services/     # ads, analytics, IAP wrappers
network/      # API, realtime, auth
data/         # saves, configs, remote config
```

### Unity overlay notes

- Prefer ScriptableObjects / existing service locators as the project does.
- Addressables/AssetBundles: follow existing load patterns; don't sync-load huge assets on main thread.
- IL2CPP/minification: keep link.xml / preserve as siblings do.

### Godot overlay notes

- Scenes + autoloads as existing project; avoid global singletons explosion.
- Export presets for Android already in repo — don't invent a second pipeline.

## Client ↔ backend for games

| Concern | Client | Server |
|---------|--------|--------|
| Score / leaderboard | Submit attempt | Validate, rate-limit, anti-cheat heuristics |
| Soft currency | Optimistic UI ok | Authoritative balance |
| IAP | Store receipt | Verify with Play Billing / store API |
| Match result | Report | Recompute or signed state |
| Config | Cache | Versioned remote config |

Load `mobile-backend-api` when adding or changing these endpoints.

## Performance checklist

- Draw calls / overdraw (especially UI canvases)
- GC spikes (allocations in Update/process)
- Texture/audio size and compression
- Battery: wake locks, unnecessary sensors, high poll rates
- Load times: splash vs async load

## Anti-patterns

- Authority on client for economy
- Giant Update() doing networking + physics + UI
- Unbounded local logs in release
- Hardcoding cheat-friendly debug menus in release builds
- Ignoring interrupted purchases / pending IAP

## Related

`android-app`, `mobile-backend-api`, `mobile-security`, `mobile-release`, `performance`
