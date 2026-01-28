---
applyTo: "app/**/*.dart"
excludeAgent: "code-review"
---

## App (Flutter/Dart) instructions

- **Localization is required**: all user-facing strings must use `context.l10n.*` (no hardcoded strings).
- If you modify ARB files in `app/lib/l10n/`, regenerate:

```bash
cd app
flutter gen-l10n
```

- Follow existing Provider/state-management patterns used in the app.
- Be mindful of background operation requirements (features should work when app is backgrounded when applicable).

### How to verify

If you changed app code, run:

```bash
cd app
./test.sh
```

