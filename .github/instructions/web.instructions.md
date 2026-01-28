---
applyTo: "web/**/*.{ts,tsx,js,jsx}"
excludeAgent: "code-review"
---

## Web (Next.js/TypeScript) instructions

- Prefer existing patterns in `web/frontend/` and `web/personas-open-source/` rather than introducing new frameworks or tooling.
- Keep changes scoped to the relevant web subproject (frontend vs personas).

### How to verify (match CI)

From `.github/workflows/lint.yml`:

```bash
cd web/frontend
npm ci
npm run lint
npm run lint:format -- --check
```

```bash
cd web/personas-open-source
npm ci --legacy-peer-deps
npm run lint
```

