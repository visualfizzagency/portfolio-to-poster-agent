#!/usr/bin/env python3
"""Clean fetched site markdown (strip nav/image noise) and cap length."""
import re, sys

def clean(path, cap=6000):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # drop image-only lines outright (long imgix URLs pass length checks)
        if s.startswith("![") or s.startswith("[!["):
            continue
        # drop lines that are only links/images (nav, social, logo) — keep lines with real words
        stripped = re.sub(r"!\[.*?\]\(.*?\)", "", s)
        stripped = re.sub(r"\[.*?\]\(.*?\)", "", stripped)
        stripped = re.sub(r"[#>*\-\|\s]", "", stripped)
        if len(re.findall(r"[A-Za-z0-9]{2,}", stripped)) < 3:
            continue
        if s.lower() in ("site navigation", "social links", "search", "newsletter"):
            continue
        lines.append(line)
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out[:cap]

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
    cleaned = clean(src, cap)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"{dst}: {len(cleaned)} chars")
