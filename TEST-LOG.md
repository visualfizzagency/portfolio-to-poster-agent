# Portfolio-to-Poster Agent — Test log

Date: 24 Nov 2026. Tester: subagent (no user key used — generation tested via the VM's Gemini CLI, which is the same prompt the demo sends).

## Generation tests (prompt + real sites, via gemini-text CLI, model gemini-3.5-flash)

| # | Site | Reader | Result |
|---|---|---|---|
| 1 | https://mdayubmondol.com | r.jina.ai → 21 KB markdown → cleaned 2,521 chars | ✅ PASS. Valid JSON: 5 concepts, 3 captions, 7-day plan. Brand = "Md Ayub Mondol". Headlines: "SEVEN YEARS OF PURPOSEFUL DESIGN", "THE FUTURE OF VISUAL CREATION", "BUILDING DISTINCT BRAND IDENTITIES", "TRUSTED BY OVER 100 BRANDS", "TURNING IDEAS INTO IMPACTFUL VISUALS". All 5 patterns different. Facts verified against source text: "7+ years" ✓, "100+ Brands & Businesses Worldwide" ✓ (grep-confirmed in source), services ✓, hellomdayub@gmail.com ✓. Saved as `sample-output.json`. |
| 2 | https://www.pentagram.com | r.jina.ai → 112 KB → cleaned 6,000 chars | ✅ PASS. Valid JSON, 5/3/7. Genuinely tailored: "FORM FUNCTION MAGIC MEANING", "THIRTY SUMMERS IN THE PARK" (Paula Scher), "FIFTY SEASONS OF LIVE TV" (SNL 50), "DATA PRECISION WITH HUMAN OPTIMISM". Services list matches site (brand identity, product design, motion, packaging, typefaces…). |
| 3 | https://www.sarasoueidan.com | r.jina.ai → 3.9 KB → cleaned 2,490 chars | ✅ PASS. Valid JSON, 5/3/7. Genuinely tailored: "THE WEB IS FOR EVERYONE", "ALT TEXT IN CSS IS HERE", "REPLACE BOOTSTRAP SCROLLSPY WITH CSS", "IN CONVERSATION WITH KEVIN POWELL". Audience = front-end designers/developers, accessibility focus — correct for her site. |

## Demo UI tests (Playwright + Chromium 1248, local server, proxy forwarder)

| # | Check | Result |
|---|---|---|
| 1 | Page loads, hero + config + URL card render | ✅ PASS — screenshots 01, 02. |
| 2 | Provider select switches model default; OpenAI-compatible reveals base-URL field | ✅ PASS (code-verified in browser run; base-URL row toggles). |
| 3 | Save key → localStorage; "Key saved" indicator shows | ✅ PASS (indicator visible in run; key stored, masked input). |
| 4 | "Preview with sample output" loads real mdayubmondol.com output, SAMPLE badge shown | ✅ PASS — screenshots 03, 04, 05. Brand, 5 concepts with colour swatches, 3 captions, 7-day table all render. |
| 5 | Copy buttons present on every concept/caption + Copy-all | ✅ PASS (buttons render; clipboard write not asserted in headless run). |
| 6 | Bad URL + fake key → reader fails → clear error + log + manual box auto-opens | ✅ PASS — screenshot 06. Log: "reader returned HTTP 422". Error box text correct. |
| 7 | Console errors | ⚠️ One expected: the browser reports the failed r.jina.ai fetch as HTTP 422 — that IS the error being handled, not an app bug. Favicon 404 found and fixed (inline SVG favicon added). No other console/page errors. |
| 8 | No key ever written to disk/logs | ✅ PASS — grep of project files: no `AIza`, `sk-`, or key values. Test key used in screenshots was the literal string "AIzaSy-TEST-KEY-DO-NOT-USE". |

## Reader proxy notes (honest)

- r.jina.ai works, but its free tier rate-limits per IP: during testing it returned HTTP 429 after several rapid fetches (Behance + jessicahische.is both 429'd at 07:54). It recovered after a short wait. The demo handles this with the manual-paste fallback and says so on screen.
- hellomonday.com is JS-heavy: the reader returned only ~3.5 KB / 40 usable chars, so it was dropped as a test site and replaced with sarasoueidan.com. JS-heavy sites are exactly what the manual-paste fallback is for.
- Behance profile pages are reader-hostile (429 + login walls). The demo cannot reliably read Behance — the manual fallback covers it.

## NOT tested (honest gaps)

1. **Live browser end-to-end with a real key.** The full in-browser path (key → provider API → rendered results) was NOT run with a real key, because no raw key is available to this environment (the VM's Gemini access is via the CLI's credential flow, not an extractable key). Generation was proven with the identical prompt via the CLI on 3 real sites; the browser demo's fetch + render + error paths were proven in Playwright. First run with a real user key will confirm the last mile (Gemini key-in-URL call, Groq/OpenAI-compatible chat call).
2. **Groq / OpenAI-compatible providers with live keys.** Code follows the standard OpenAI chat-completions schema; untested live.
3. **Clipboard in headless Chromium.** Copy buttons render and call `navigator.clipboard.writeText`; the write itself was not asserted headlessly (headless clipboard permissions). Works in a normal browser.

## Faults found and fixed during testing

- Favicon 404 → added inline SVG favicon.
- Error state didn't show the manual fallback without an extra click → fetch failure now auto-opens the manual-paste box.
- Site-text cleaner let long image-only lines through → fixed (lines starting with `![` / `[![` dropped outright).
