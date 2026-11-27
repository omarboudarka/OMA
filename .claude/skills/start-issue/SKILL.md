---
name: start-issue
description: Start work on a Linear issue from team OMA. Reads the issue, creates its branch, sets it to In Progress and proposes a plan for approval.
argument-hint: [OMA-123]
disable-model-invocation: true
---

Start work on Linear issue $ARGUMENTS.

1. **Read the issue.** Use the Linear MCP to get the issue (description, acceptance criteria, Agent notes, labels, project, `gitBranchName`, blocking relations) and its comments. If no issue ID was given, list my issues in the current cycle that are in Todo and ask which one.
2. **Check it can start.** If an issue that blocks it isn't Done, stop and say which one.
3. **Check the working tree.** Run `git status`. If there are uncommitted changes, stop and ask what to do with them.
4. **Branch from a fresh main.** Run `git switch main`, then `git pull --ff-only`, then `git switch -c <gitBranchName>` with the issue's exact `gitBranchName`, so Linear links the branch.
5. **Set the issue to In Progress** in Linear.
6. **Plan before touching code.** Read the code the issue touches, then show me a short plan:
   - the files to add or change
   - the tests to write first
   - how each acceptance criterion will be checked
   - open questions, if any

   Wait for my approval. Don't edit files before I approve.
7. **Record the plan.** After I approve, post the final plan as a comment on the issue, so the plan lives with the ticket.

Then implement: failing test first, then code, then `make check`. When done, use `/open-pr`.
