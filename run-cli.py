#!/usr/bin/env python3
"""Run the Portfolio-to-Poster agent prompt through gemini-text CLI (test path).
Usage: run-cli.py <site-clean.txt> <url> <out.json>
Saves raw output + validated JSON. Exits non-zero on failure."""
import json, os, re, subprocess, sys

CLI = os.path.expanduser("~/workspace/custom-connectors/custom.legacy-gemini/bin/gemini-text")
ENV = dict(os.environ, PYTHONPATH="/opt/muse/skills/custom-connector-setup/bin")

def main():
    site_file, url, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(os.path.expanduser("~/workspace/portfolio-poster-agent/prompt-system.txt")) as f:
        system = f.read()
    with open(site_file) as f:
        site_text = f.read()
    user = ("Website URL: " + url + "\n\nWebsite content:\n" + site_text
            + "\n\nGenerate the poster concepts, captions and week plan in the JSON format from the system prompt.")
    proc = subprocess.run([CLI, "--prompt", user, "--system", system],
                          capture_output=True, text=True, timeout=300, env=ENV)
    if proc.returncode != 0:
        print("CLI FAILED:", proc.stderr[:500], file=sys.stderr)
        sys.exit(1)
    raw = proc.stdout
    with open(out_path + ".raw.txt", "w") as f:
        f.write(raw)
    cleaned = re.sub(r"```json\s*", "", raw).replace("```", "").strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        print("NO JSON IN OUTPUT", file=sys.stderr)
        print(raw[:1000], file=sys.stderr)
        sys.exit(2)
    data = json.loads(cleaned[start:end + 1])
    # validate shape
    assert data["brand"]["name"], "missing brand name"
    assert len(data["posterConcepts"]) == 5, f"concepts={len(data['posterConcepts'])}"
    assert len(data["captions"]) == 3, f"captions={len(data['captions'])}"
    assert len(data["weekPlan"]) == 7, f"week={len(data['weekPlan'])}"
    for c in data["posterConcepts"]:
        assert c["headline"] and c["colors"] and c["layout"] and c["visual"], "concept missing fields"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"OK: {out_path} — brand={data['brand']['name']!r}, concepts=5, captions=3, week=7")

if __name__ == "__main__":
    main()
