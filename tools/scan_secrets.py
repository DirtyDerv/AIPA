#!/usr/bin/env python3
import re, pathlib
root=pathlib.Path().resolve()
patterns=[
 re.compile(r"[MN][A-Za-z0-9_-]{23}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27}"),
 re.compile(r"bot_[A-Za-z0-9-_]{20,}"),
 re.compile(r"ghp_[A-Za-z0-9_]{36}"),
 re.compile(r"gho_[A-Za-z0-9_]{36}"),
 re.compile(r"AKIA[0-9A-Z]{16}"),
 re.compile(r"-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----[\s\S]+?-----END ([A-Z ]+ )?PRIVATE KEY-----"),
]
flagged=set()
for p in root.rglob('*'):
    try:
        if p.is_file() and '.git' not in p.parts:
            txt=p.read_text(encoding='utf-8', errors='ignore')
            for pat in patterns:
                if pat.search(txt):
                    flagged.add(str(p.relative_to(root)))
    except Exception:
        pass
out = root / 'scan_report.txt'
with open(out,'w',encoding='utf-8') as f:
    if not flagged:
        f.write('NO_MATCHES\n')
    else:
        for s in sorted(flagged):
            f.write(s+'\n')
print('Scan complete. Results in', out)
