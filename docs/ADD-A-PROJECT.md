# How to add a new project

1. **Copy, don't move.** Copy only source code into `Documents\GitHub\portfolio\<repo-name>` (lowercase-kebab). Leave out `.venv`, `build`, `dist`, `runs`, logs, databases, media, `.env`, Office/PDF files, and logos.
2. **Sanitize.** Replace staff names, emails, phone numbers, IP addresses, SIDs, hostnames, and Google/Slack/JotForm IDs with fictional or placeholder values. Never include client data.
3. **Scan.** `gitleaks dir . --redact` must report `no leaks found`. Then search for real names and `@kaseyosmanins.com` / `@allstate.com` — zero hits.
4. **Scaffold.** Add `README.md` (problem → solution → highlights → Mermaid diagram → stack → run → status), `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.pre-commit-config.yaml`, `.githooks/pre-commit`.
5. **Init + hook.** `git init -b main` → `git config core.hooksPath .githooks` → commit.
6. **Create private.** `gh repo create forrestswan3/<repo-name> --private --source . --push --description "..."`, then add topics with `gh repo edit --add-topic`.
7. **Register.** Add the project to `portfolio.json` (visibility `private`), commit, push. Copy the regenerated `PROFILE_README.md` into the profile repo.
8. **Go public (optional).** Only after review: `gh repo edit forrestswan3/<repo-name> --visibility public --accept-visibility-change-consequences`, set `visibility` to `public` in `portfolio.json`, push.
9. **Project page (optional).** Add a `detail` block (problem, solution, highlights, stack, diagram, notes) and `"page": "https://forrestswan3.github.io/<repo-name>/"` to the project in `portfolio.json`. If it has a browser demo, add `demo` + `preview`, save a 1440×900 screenshot to `assets/previews/<repo-name>.png` and to `docs/preview.png` in the project repo. Run `python scripts/build.py`, copy `pages/<repo-name>/index.html` to the project repo root, and enable Pages on that repo (`main`, `/`).
