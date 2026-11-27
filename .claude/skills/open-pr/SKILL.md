---
name: open-pr
description: Finish the current OMA issue branch. Runs the checks, commits, pushes and opens a pull request linked to the Linear issue.
disable-model-invocation: true
---

Open a pull request for the current branch.

1. **Find the issue.** Read the issue ID from the branch name (`oma-<n>`). If there is none, ask me which issue this is for. Get the issue from Linear to see its acceptance criteria.
2. **Run the checks.** Run `make check` if the Makefile has it. If it fails, fix it. If you can't, stop and tell me what fails. Never open a PR on failing checks.
3. **Review the diff.** Read `git status` and `git diff main...HEAD`. Make sure nothing below is included:
   - an `.env` file other than `.env.example`
   - course material (lecture notes, exercise sheets, solutions)
   - large generated files or local caches
4. **Commit what's left** with a typed message: `type: summary (OMA-<n>)`, where type is `feat`, `fix`, `eval`, `chore`, `docs` or `refactor`.
5. **Push the branch:** `git push -u origin HEAD`.
6. **Open the PR** with `gh pr create --base main`, titled `type: summary (OMA-<n>)`. Fill the body from `.github/pull_request_template.md`. Its first line is:
   - `Closes OMA-<n>` when every acceptance criterion is met
   - `Part of OMA-<n>` when work is left; then list what's left under "Risks"
7. **Update Linear.** Tick the acceptance criteria this PR meets in the issue description. Then give me the PR link.
