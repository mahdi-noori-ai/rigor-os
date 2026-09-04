# Skill: Mobile Security

```
Name: mobile-security
Domain: mobile / security
Purpose: Protect Android apps/games: storage, transport, auth, tampering surfaces
Trigger: Auth on mobile, tokens, secure storage, IAP, root detection hooks, deep links, WebView
Do Not Trigger: Pure visual polish
```

## Checks

- [ ] Secrets not in APK (no prod API keys in source; use backend for privileged ops)
- [ ] Tokens in EncryptedSharedPreferences / Keystore patterns the project uses — not plain SharedPreferences for secrets
- [ ] HTTPS only; cleartext disabled unless debug-only and documented
- [ ] Deep links / App Links validated; no open redirects into privileged screens
- [ ] WebView: JS bridge locked down if used
- [ ] Backup rules: exclude sensitive files if needed (`android:allowBackup` policy)
- [ ] Debug menus / cheats stripped or gated in release
- [ ] IAP verification server-side
- [ ] Logging: no tokens/PII in Logcat for release

## Games

- Obfuscation (R8/ProGuard / IL2CPP) as project standard — not a substitute for server authority
- Detect rooted/emulator only if product requires — don't break legit users without reason

## Related

`appsec-review`, `security-gate`, `mobile-backend-api`
