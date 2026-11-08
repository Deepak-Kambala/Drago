# Contributing to Drago

Thank you for your interest in improving Drago! We welcome bug fixes, new features, and improvements to the evolution engine.

---

## Contribution Workflow

To keep code contributions separate from your personal profile assets:

### 1. Create a Feature Branch
Always create a separate branch for your code changes instead of working on your `main` branch:

```bash
git checkout -b fix/my-feature-or-bugfix
```

### 2. Make Your Code Changes
Edit code in `drago/` or documentation in `docs/` or `README.md`.

Do **not** commit personal generated assets (`assets/dragon.gif`, `assets/dragon-status.svg`, `assets/drago-state.json`) to your feature branch.

If personal assets were modified locally while testing:
```bash
git checkout origin/main -- assets/dragon.gif assets/dragon-status.svg assets/drago-state.json
```

### 3. Run the Test Suite
Ensure all unit tests pass:

```bash
python3 -m unittest discover tests
```

### 4. Submit Your Pull Request
Push your branch to your fork and submit a Pull Request against `Deepak-Kambala/Drago:main`.

Automated CI will run unit tests and ensure no generated assets are included in the PR.
