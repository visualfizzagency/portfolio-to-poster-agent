# Portfolio-to-Poster Agent

Paste any portfolio or website URL. The agent reads the site, understands the brand, and generates **5 poster concepts, 3 ready-to-post captions and a 7-day content plan**.

Free forever. **Bring your own API key** — Gemini, Groq, or any OpenAI-compatible provider. No server, no sign-up, no auto-posting.

[![☕ Support Me](https://img.shields.io/badge/%E2%98%95_Support_Me-FFDD00?style=for-the-badge)](https://www.supportkori.com/hellomdayub)

## Try it

Open `index.html` in a browser (or `python3 -m http.server` in this folder). No key? Press **"Preview with sample output"** to see a real generated kit for `mdayubmondol.com`.

## How it works

1. Paste your API key once (Step 1) — it stays in **your browser only** (localStorage), sent only to the provider you chose.
2. Paste a portfolio/website URL (Step 2) and press Generate.
3. The agent reads the site (free public reader `r.jina.ai`, or paste the text manually if the site blocks readers), analyses it with your provider, and shows your poster kit. Copy anything.

## The skill

`skills/portfolio-to-poster-agent/SKILL.md` — the same workflow as an [Agent Skills](https://agentskills.io) skill for Claude Code, Cursor, Copilot and Gemini CLI.

## Files

- `index.html` — the whole demo (one file, no build step)
- `sample-output.json` — real generated output for mdayubmondol.com
- `prompt-system.txt` — the exact instruction sent to the AI
- `WORKFLOW.md` — step-by-step workflow with screenshots (read before approving)
- `TEST-LOG.md` — test results and honest gaps

## Privacy

Your API key is yours. It lives in your browser, goes only to the provider you select, and is never stored in this repo, in logs, or on any server. There is no server.

## Licence

MIT — Md Ayub Mondol / VisualFizz.
