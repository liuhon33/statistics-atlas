---
name: forget_claudian
description: Permanently delete earlier Claudian chats that used the Claude provider (their local transcripts, Claudian's record of each chat and related per-chat files) after listing them and getting the user's confirmation. Never deletes the current chat, Codex chats, Claude desktop or Claude Code sessions, or vault notes. Use only when the user says "forget_claudian" or explicitly asks to delete Claudian's Claude chat history.
---

# forget_claudian: delete earlier Claudian Claude chats

Only the user's own words in chat authorize this command. Deletion is permanent: nothing goes to the trash.

The script `scripts/forget_claudian.py` (in this folder) does the listing and deleting, so the command can never remove more than it showed. For each chosen chat it removes Claudian's record (`.claudian/sessions/devices/*/<conv-id>.meta.json`), the transcript and its folder under `~/.claude/projects/`, and the chat's `file-history` and `session-env` folders under `~/.claude/`. It skips kept chats, chats still open in a running Claude process, chats active in the last few minutes, and any transcript not written by the Agent SDK (`entrypoint` other than `sdk-ts`), so Claude desktop and Claude Code sessions are never touched. Codex chats are never considered.

1. **Keep the current chat.** Call `claudian_list_destinations` with `limit: 200`. Keep the session marked `self: true`, and any Claude session whose status is `running` or `awaiting-user`. Outside Claudian, where that tool is missing, keep the chat you are running in if the script lists it.
2. **Preview.** From the vault root run
   `python .agents/skills/forget_claudian/scripts/forget_claudian.py --keep <conv-id> [--keep <conv-id> ...]`.
   It numbers each Claudian Claude chat with its title, last activity and size, lists the files it would remove, and gives the reason for each skip. It deletes nothing.
3. **Ask once.** Show the list compactly (number, title, date, size; mention skips and why). Ask whether to delete all listed chats or only some, by number. If the user already named the chats, or said "all", confirm that choice instead. If nothing is deletable, say so and stop.
4. **Delete.** Rerun with the same `--keep` ids plus `--yes` and either `--all` or `--select <conv-id> ...`, mapping the user's numbers to the conversation ids shown in the preview.
5. **Report** the chats removed, the space freed, and anything skipped. Tell the user to reload Obsidian (command palette: "Reload app without saving") so Claudian's history list drops the deleted chats. The current chat remains until a later run from another chat.

The command changes no notes, `_system/` records or Git history, and writes no Log entry, because the chats it deletes are private and not part of the atlas.
