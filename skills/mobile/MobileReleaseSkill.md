# Skill: Mobile Release (Android)

```
Name: mobile-release
Domain: mobile / release
Purpose: Safe Android build, sign, and store release
Trigger: Play Store upload, AAB/APK, signing, versionCode, release notes, store listing
Do Not Trigger: Local debug feature work with no release intent
```

## Checklist

- [ ] `versionCode` / `versionName` bumped correctly
- [ ] Release signing via CI secrets or local keystore **not** committed
- [ ] Min/target SDK intentional; breaking OS changes reviewed
- [ ] R8/ProGuard mapping archived for crash deobfuscation
- [ ] Release build installed and smoke-tested (login + one critical path)
- [ ] Backend `min_app_version` updated if forcing upgrade
- [ ] Changelog / Play release notes
- [ ] Privacy policy / data safety form still accurate if permissions changed
- [ ] Rollback plan: previous AAB track / staged rollout

## Anti-patterns

- Committing `keystore.jks` or passwords
- Shipping debuggable release
- Raising target SDK without testing
- Silent breaking API deploy without app gate

## Related

`deployment-release` workflow, `cicd`, `mobile-security`
