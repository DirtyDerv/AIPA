#!/usr/bin/env python3
import re, sys, pathlib

FILES = [
    'CREDENTIAL_BACKUP_20251103_134353.md',
    'bot/discord_bot_simple.py',
    'docs/WORKLOG_COMPLETE.md',
    'tools/test_discord_connection.py',
]

patterns = [
    re.compile(r"([MN][A-Za-z0-9_-]{23})\.([A-Za-z0-9_-]{6})\.([A-Za-z0-9_-]{27})"),
    re.compile(r"(ghp_[A-Za-z0-9_]{36})"),
    re.compile(r"(bot_[A-Za-z0-9-_]{20,})"),
]

root = pathlib.Path().resolve()

def mask(s):
    if len(s) <= 10:
        return '<REDACTED>'
    return s[:4] + '...' + s[-4:]

for f in FILES:
    p = root / f
    if not p.exists():
        print(f'MISSING: {f}')
        continue
    print(f'--- {f} ---')
    for i,line in enumerate(p.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
        out=line
        found=False
        for pat in patterns:
            m=pat.search(line)
            if m:
                found=True
                for grp in m.groups():
                    out=out.replace(grp, mask(grp))
        if found:
            print(f'{i}: {out}')
