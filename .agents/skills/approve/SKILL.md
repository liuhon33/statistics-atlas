---
name: approve
description: Finalize learning notes or backbone edits after the user has reviewed the drafts in Obsidian, validate the vault, and commit exactly that work. Use only when the user says "approve" or explicitly asks to commit reviewed work.
---

# approve: finalize and commit reviewed work

Only the user's own words in chat authorize this command.

1. **Scope.** Work out exactly what is approved: what the user names, or else the files reported by the commands run since the last commit (for example a digest and the `connect` run that followed it), checked against `git status`.
   - In a new session, use `git status`, notes with `status: draft` and the recent `_system/Log.md` entries, and confirm the list with the user.
   - Leave out unrelated changes, such as `.obsidian/`, `.claudian/` and other pending drafts, unless the user includes them.
   - A file in scope may also hold other pending work: the shared record files (`_system/Log.md`, `Catalog.md`, `catalog.json`, `Digest Checkpoints.md`, `Build status.md`, `Review Queue.md`), or a note that `connect` linked while it was still an uncommitted draft. If so, say so and ask whether to commit it together or wait.
2. **Last edits.** First apply any changes the user gave with the approval.
3. **Finalize.**
   - For each new learning note, change `status: draft` to `active` and set `updated` to today, and mirror the status in `_system/catalog.json`. Keep `verification` honest: editorial approval is neither verification nor mastery.
   - Resolve the review-queue items the user's review settled; real gaps stay.
   - Add a Log entry, `approve | <title>`, quoting the user's approval words.
4. **Validate.** Run `python _system/tools/validate.py .` and `python _system/tools/test_validate.py`, plus `test-model.cjs` if the backbone structure changed. If anything new fails, stop and report.
5. **Commit.** Stage the scoped files by explicit path, never with `git add -A` or `git add .`. Make one commit per approved piece of work, with a message like `Digest <title>`, `Extend <title>`, `Connect <title>`, `Enrich <page>` or `Add backbone node <title>`, a short body listing the files and checks, and your harness's attribution trailer. Never amend, push, or skip hooks.
6. **Report** the commit hash, the files committed, and anything left uncommitted. After committing a new or extended learning note, offer `connect` for it.
