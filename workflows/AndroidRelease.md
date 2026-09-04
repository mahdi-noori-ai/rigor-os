# Android Release Workflow

```
Version bump → Release build → Smoke on device
    → Mapping file stored → Store upload / track
    → Backend min version if needed → Staged rollout
```

Follow `skills/mobile/MobileReleaseSkill.md` and `workflows/DeploymentRelease.md` for backend deploy coordination.

Never commit keystores. Prefer Play App Signing + CI secrets.
