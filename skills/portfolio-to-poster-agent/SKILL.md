---
name: portfolio-to-poster-agent
description: Turn any portfolio or website URL into poster ideas and social content — read the site, understand the brand, and generate 5 poster concepts, 3 ready-to-post captions and a 7-day content plan. Use when the user shares a portfolio, agency or business website and asks for poster ideas, social content or a content plan for it. Works with the user's own API key (Gemini, Groq or any OpenAI-compatible provider) — the skill never supplies a key.
license: MIT
metadata:
  author: Md Ayub Mondol / VisualFizz
  language: English
---

# Portfolio-to-Poster Agent

Paste a portfolio or website URL. The agent reads the site, understands the brand, and turns it into ready-to-design poster concepts and social content — no auto-posting, idea generation only.

## When to use this skill

- The user shares a portfolio, agency or business website and asks for poster ideas, social captions or a content plan.
- The user says "make posters from this site", "content ideas for this brand", or "analyse this portfolio".
- Never for auto-posting, auto-commenting, or logging into anyone's social accounts. Idea generation only — platform rules.

## The workflow

1. **Get the site's text.** Fetch the URL through a public reader (e.g. `https://r.jina.ai/<url>` returns the page as markdown). Clean it: drop navigation, image-only lines and link-only lines, keep the first ~6000 characters of real copy. If the reader fails (site blocks readers, rate limit, JS-only site), ask the user to paste the site's text manually — never invent site content.
2. **Get the key — BYOK.** The user pastes THEIR OWN API key into the one config spot and picks a provider: Gemini, Groq, or any OpenAI-compatible API. The key is stored only in the user's browser (localStorage) and sent only to the provider they chose. There is no server. The skill never supplies, stores or logs a key. For testing, use a test key or the project's own CLI setup — never ship a key in code.
3. **Analyse with the model.** Send the system prompt below with the site text. Ask for STRICT JSON only — no markdown fences, no commentary. Validate the shape: exactly 5 concepts, exactly 3 captions, exactly 7 week-plan days. If the model returns bad JSON or too few items, retry once, then report the failure honestly.
4. **Render the kit.** Show a brand snapshot (name, what they do, services, audience, tone), then the 5 poster concepts, the 3 captions and the 7-day plan, each with a copy button. Keep the site URL visible as the source.

## System prompt (use verbatim)

> You are the Portfolio-to-Poster Agent. You read a portfolio or business website and turn it into ready-to-design poster concepts and social content.
>
> RULES
> - Use ONLY facts found in the website text below. Never invent services, clients, prices, awards, locations or numbers the site does not state. If a fact is missing, say so in that field instead of guessing.
> - Every poster concept must be genuinely different from the others: pick a different layout pattern for each one. Never repeat the same headline idea twice.
> - Poster design DNA: the headline is the hero (oversized, extra-bold, stacked over 2-3 lines; one accent word may be serif/italic/outline, never more than one). Tight palette: 2-3 colors maximum per poster. Pick ONE pattern per concept: (1) oversized condensed headline over a duotone photo, (2) floating glossy 3D icon chips, (3) cinematic dark with neon glow, (4) editorial minimal on cream, (5) gradient mesh, (6) cutout portrait + sticker badges, (7) tilted diagonal composition with grain. Real brand colors for any logo. Footer on every poster: the brand's own website.
> - Captions: simple and professional. Short sentences, plain words. NO engagement-bait questions, no fluffy words, no unnecessary names.
> - Social images are 4:5 portrait; thumbnails 1:1 square.
>
> OUTPUT — STRICT JSON ONLY, exactly this shape: brand {name, whatTheyDo, services[], audience, tone, website}; posterConcepts[5] {title, headline, pattern, layout, colors[hex], visual, why}; captions[3] {text, hashtags[]}; weekPlan[7] {day, idea, format}.

## Provider call shapes

- **Gemini:** `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}` with `{system_instruction:{parts:[{text:SYSTEM}]}, contents:[{parts:[{text:USER}]}]}`. Default model: `gemini-2.5-flash`.
- **Groq / OpenAI-compatible:** `POST {base}/chat/completions` with `Authorization: Bearer {key}` and `{model, messages:[{role:"system",content:SYSTEM},{role:"user",content:USER}], temperature:0.7}`. Groq base: `https://api.groq.com/openai/v1`, default model `llama-3.3-70b-versatile`. OpenAI-compatible: the user supplies the base URL and model.

## What NOT to do

- Never invent facts about the brand — every claim must trace to the site text.
- Never auto-post, auto-comment, or log into social accounts.
- Never put an API key in code, a repo, a log or a screenshot.
- Never promise the reader works for every site — JS-heavy and reader-blocking sites need the manual-paste fallback.
- Never repeat the same poster template across concepts — each concept uses a different pattern.
- Never use engagement-bait in captions ("comment below", "how did you like it?").
