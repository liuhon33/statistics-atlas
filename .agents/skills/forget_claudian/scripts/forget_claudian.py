"""List or permanently delete earlier Claudian chats that used the Claude provider.

Preview (deletes nothing):
    python forget_claudian.py --keep <id> [--keep <id> ...]
Delete:
    python forget_claudian.py --keep <id> ... --yes --all
    python forget_claudian.py --keep <id> ... --yes --select <conv-id> [<conv-id> ...]

<id> may be a Claudian conversation id (conv-...) or a Claude session id (UUID).

For each chosen chat it removes exactly these, and nothing else:
  - Claudian's record:  <vault>/.claudian/sessions/devices/*/<conv-id>.meta.json
  - the transcript:     <claude-dir>/projects/*/<session-id>.jsonl
  - its folder:         <claude-dir>/projects/*/<session-id>/   (subagents, tool results)
  - edit backups:       <claude-dir>/file-history/<session-id>/
  - session env:        <claude-dir>/session-env/<session-id>/
<claude-dir> is $CLAUDE_CONFIG_DIR or ~/.claude.

It skips: kept chats; chats whose Claude process is still running (open in a tab);
chats active in the last few minutes; and any transcript not written by the
Agent SDK (entrypoint "sdk-ts"), so Claude desktop and Claude Code CLI sessions
are never touched. Codex chats are never considered.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
CONV_RE = re.compile(r"^conv-[A-Za-z0-9-]+$")
RECENT_SECONDS = 180


def claude_dir() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env) if env else Path.home() / ".claude"


def pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        # Never use os.kill on Windows: it terminates the process.
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return True  # cannot tell: treat as running
            return code.value == 259  # STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def running_session_ids(cdir: Path) -> set[str]:
    running = set()
    for f in (cdir / "sessions").glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        sid, pid = data.get("sessionId"), data.get("pid")
        if isinstance(sid, str) and isinstance(pid, int) and pid_alive(pid):
            running.add(sid)
    return running


def transcript_entrypoint(path: Path) -> str | None:
    pattern = re.compile(r'"entrypoint"\s*:\s*"([^"]*)"')
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = pattern.search(line)
                if m:
                    return m.group(1)
    except OSError:
        return None
    return None


def size_of(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n} B"


def collect(vault: Path, cdir: Path) -> list[dict]:
    chats = []
    for meta_path in sorted(vault.glob(".claudian/sessions/devices/*/conv-*.meta.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if meta.get("providerId") != "claude":
            continue
        conv = meta.get("id") or meta_path.name[: -len(".meta.json")]
        sid = (meta.get("providerState") or {}).get("providerSessionId") or meta.get("sessionId")
        chat = {
            "conv": conv,
            "sid": sid if isinstance(sid, str) else None,
            "title": str(meta.get("title") or "(untitled)"),
            "last": meta.get("lastActivityAt") or meta.get("createdAt") or 0,
            "meta": meta_path,
            "targets": [meta_path],
            "skip": None,
        }
        if not CONV_RE.match(str(conv)):
            chat["skip"] = "unrecognised conversation id"
        elif chat["sid"] and UUID_RE.match(chat["sid"]):
            sid = chat["sid"]
            transcripts = list((cdir / "projects").glob(f"*/{sid}.jsonl"))
            for t in transcripts:
                chat["targets"].append(t)
                folder = t.with_suffix("")
                if folder.is_dir():
                    chat["targets"].append(folder)
            for extra in (cdir / "file-history" / sid, cdir / "session-env" / sid):
                if extra.is_dir():
                    chat["targets"].append(extra)
            chat["transcripts"] = transcripts
        elif chat["sid"]:
            chat["skip"] = "unrecognised Claude session id"
        chats.append(chat)
    chats.sort(key=lambda c: c["last"], reverse=True)
    return chats


def decide_skips(chats: list[dict], keep: set[str], running: set[str]) -> None:
    now = time.time()
    for c in chats:
        if c["skip"]:
            continue
        if c["conv"] in keep or (c["sid"] and c["sid"] in keep):
            c["skip"] = "kept (current or named chat)"
            continue
        if c["sid"] and c["sid"] in running:
            c["skip"] = "still open in a running Claude process; close its Claudian tab first"
            continue
        for t in c.get("transcripts", []):
            ep = transcript_entrypoint(t)
            if ep != "sdk-ts":
                c["skip"] = f"transcript not written by Claudian/Agent SDK (entrypoint {ep!r})"
                break
            if now - t.stat().st_mtime < RECENT_SECONDS:
                c["skip"] = "active in the last few minutes"
                break


def remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    default_vault = Path(__file__).resolve().parents[4]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", type=Path, default=default_vault, help="vault root (default: inferred)")
    ap.add_argument("--keep", action="append", default=[], help="conversation or session id to keep")
    ap.add_argument("--all", action="store_true", help="delete every listed chat that is not skipped")
    ap.add_argument("--select", nargs="+", default=[], help="conversation ids to delete")
    ap.add_argument("--yes", action="store_true", help="actually delete (otherwise preview only)")
    args = ap.parse_args()

    vault = args.vault.resolve()
    if not (vault / ".claudian").is_dir():
        print(f"No .claudian folder in {vault}; nothing to do.")
        return 1
    cdir = claude_dir()
    chats = collect(vault, cdir)
    decide_skips(chats, set(args.keep), running_session_ids(cdir))

    if args.yes and not (args.all or args.select):
        print("Refusing to delete: give --all or --select <conv-id> ...")
        return 2
    if args.all and args.select:
        print("Give either --all or --select, not both.")
        return 2
    known = {c["conv"] for c in chats}
    unknown = [s for s in args.select if s not in known]
    if unknown:
        print("Unknown conversation id(s): " + ", ".join(unknown))
        return 2

    if not chats:
        print("No Claudian chats with the Claude provider were found.")
        return 0

    chosen = [c for c in chats if args.all or c["conv"] in args.select]
    mode = "DELETE" if args.yes else "PREVIEW (nothing deleted)"
    print(f"{mode}: Claudian Claude chats in {vault}\n")
    deleted = freed = 0
    for i, c in enumerate(chats, 1):
        when = datetime.fromtimestamp(c["last"] / 1000).strftime("%Y-%m-%d %H:%M") if c["last"] else "?"
        size = sum(size_of(t) for t in c["targets"] if t.exists())
        print(f"[{i}] {c['title']}")
        print(f"    {c['conv']}  session {c['sid'] or '-'}  last active {when}  {human(size)}")
        if c["skip"]:
            print(f"    SKIP: {c['skip']}")
            print()
            continue
        if not args.yes:
            for t in c["targets"]:
                print(f"    would remove: {t}")
        elif c in chosen:
            for t in c["targets"]:
                remove(t)
                print(f"    removed: {t}")
            deleted += 1
            freed += size
        else:
            print("    kept (not selected)")
        print()
    if args.yes:
        print(f"Deleted {deleted} chat(s), {human(freed)} freed. Reload Obsidian so Claudian's history list updates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
