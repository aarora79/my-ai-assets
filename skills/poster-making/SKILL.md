---
name: poster-making
description: Build a printable A4 front/back poster - HTML, two 300 DPI PNGs and a print-ready PDF - from a repo's README, docs and an optional slide deck. Use for conference posters, handouts and one-pagers.
license: MIT-0
metadata:
  author: aarora79
  version: "1.0"
---

# Poster making

Turn a repository into a two-sided A4 poster somebody can print, hold and scan. The house style is a dense panel infographic: thick ink borders, hard offset shadows, chunky display type, one chart drawn by hand rather than screenshotted.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Repo path | yes | Local path, or a path on the user's machine reached through the device shell. |
| Source HTML | no | A slide deck or exec brief in the repo. It usually holds the best-argued prose - mine it first. |
| Output directory | no | Default `<repo>/docs/poster/`. |
| Poster name | no | Default `<repo-slug>-poster`. **Never add a version suffix to a shipped file.** |

## Deliverables - always all four

```
<name>.html        self-contained: fonts + QR + chart inlined, no external requests
<name>-front.png   2481 x 3509 (A4 at 300 DPI)
<name>-back.png    2481 x 3509
<name>.pdf         2 pages, exactly 210 x 297 mm, zero margins
```

## Step 0 - ask two questions, then commit

Ask once, in one question call, before building: **palette** and **what the back carries**. Orientation defaults to portrait. If the user answers free-form or is away, pick the default, say which you picked, and keep moving. Do not ask again later.

## Step 1 - research before you touch the build harness

Read everything first. Opening the design before you have the facts anchors you on layout instead of content.

- `README.md` - the headline claims, install commands, canonical repo URL, licence.
- `docs/*.md` - results tables. Recompute per-unit figures yourself (`run cost / task count`) and **cross-check against the published numbers**. When a table and the README disagree, use the published figure and tell the user about the discrepancy.
- The source HTML deck. A deck with embedded images is mostly base64; strip it before reading:

```powershell
$h = Get-Content $deck -Raw
$h = [regex]::Replace($h,'data:image/[^")]+','IMG',[Text.RegularExpressions.RegexOptions]::Singleline)
$h = [regex]::Replace($h,'<(script|style).*?</\1>','',[Text.RegularExpressions.RegexOptions]::Singleline)
$h = [regex]::Replace($h,'<[^>]+>',"`n")
$h = [regex]::Replace($h,'(\r?\n\s*){2,}',"`n")
[System.Net.WebUtility]::HtmlDecode($h) | Set-Content $out -Encoding UTF8
```

Speaker notes in a deck are gold - they carry the argument in spoken register, which is what poster copy needs.

## Step 2 - build harness

Work in a scratch dir with four files: `chart.py` (SVG generator), `template.html` (placeholders `__FONTS__`, `__QR__`, `__CHART__`), `build.py` (inlines all three), `shot.py` (renders and measures).

**Fonts.** Google Fonts is blocked by the proxy. Pull woff2 from npm instead and base64-inline them so the page renders identically everywhere:

```bash
npm pack @fontsource/space-grotesk @fontsource/jetbrains-mono @fontsource/archivo
# use: space-grotesk 400/500/700, archivo 700/900, jetbrains-mono 400/700 (latin, no -ext)
```

**QR.** Generate it, then *prove it scans* by decoding it back:

```python
import qrcode, cv2
from qrcode.constants import ERROR_CORRECT_M
q = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=8, border=2)
q.add_data(URL); q.make(fit=True)
q.make_image(fill_color="#14181C", back_color="#FFFDF7").convert("RGB").save("qr.png")
assert cv2.QRCodeDetector().detectAndDecode(cv2.imread("qr.png"))[0] == URL
```

Never retype base64 from tool output - it truncates silently. Stage or read the bytes.

## Step 3 - the design system

Page geometry: `794 x 1123 px` (A4 at 96 DPI), `padding: 20px 28px 9px`, `gap: 8.5px`, `overflow: hidden`.

```css
:root{
  --paper:#FAF6EE; --card:#FFFDF7; --ink:#14181C;
  --teal:#0E7C7B;  --teal-d:#0A5453; --teal-w:#D9ECEA;
  --coral:#E4552F; --coral-w:#FBE2D8;
  --amber:#E9A82C; --amber-w:#FBEDD0;
  --muted:#6C7876;
}
```

Swap those five hues for any palette the user picks; keep the paper light and the ink near-black so it prints. Add a faint dot grid: `radial-gradient(var(--ink) .6px, transparent .6px)` at `16px`, `opacity:.045`.

**Type.** Archivo 900 uppercase for headings (h1 39px/-1.6px tracking, h2 16.5px), Space Grotesk for body (10.6px, `.fine` 8.4px), JetBrains Mono for labels, commands and data (7-9px, wide tracking, uppercase for eyebrows).

**Cards.** `background: var(--card); border: 2.4px solid var(--ink); border-radius: 11px; box-shadow: 4px 4px 0 var(--ink); padding: 9px 12px`. Nested boxes drop to 2.2px borders and no shadow. Every panel gets a numbered chip (`01`, `02`, ...) running continuously across both pages, and optionally a right-aligned mono `.tail` caveat.

## Step 4 - content architecture

**Front tells the story, back carries the evidence and the thing people install.**

Front: masthead (chips, two-line headline with a highlighter span, sub, QR) -> the counter-intuitive visual that makes the problem concrete -> a four-tile stat strip -> the conceptual frame -> the payoff -> method. Back: the chart as hero -> the deep-dive, given roughly half the page.

Rules that carry the most weight:

- **One idea per panel**, stated in the h2 as a claim, not a topic. "Does the harness matter? Yes." beats "Harness comparison".
- **Numbers get tiles, arguments get prose, comparisons get bars or tables.** Never a paragraph where a bar would do.
- **Split a how-it-works section by actor** - two lanes with a dashed divider, numbered steps in each, a dark handoff bar spanning both explaining why the boundary sits where it does. This reads far better than one long list.
- **Both pages carry the QR.** Front full size (~124px), back compact (~92px) in the header band.
- **Disclaimers go on both pages**, in a coral-bordered strip above the footer, when the work is sample code or benchmark numbers that could be mistaken for an official position. Say plainly: demonstration and learning only, not for production, review and harden before use, results reflect specific configurations, numbers are representative and not an official position - run your own tests. Push the same caution into the body copy: title panels "What one frontier told one buyer", tag the chart "one run, one dataset", and label illustrative graphics as drawn to make a point rather than measured.
- **No personal names or event names** unless the user asks for them.

## Step 5 - charts: draw them, don't screenshot them

A matplotlib PNG dropped into a hand-drawn poster looks pasted in. Regenerate the chart as inline SVG from the real numbers so line weights and type match the page. Log x-axis for cost, linear y for score, dashed staircase through the non-dominated set, circles for one hosting basis and squares for the other.

Label collisions are the whole difficulty. The ladder that works:

1. Frontier models get a two-line label (name + `score . $cost`) at `dy:-24`, anchored middle.
2. Everything else gets a one-line muted label, anchored left or right away from its neighbours.
3. A tight cluster of same-family models gets **short labels only** (`4-5`, `4-6`, `4-7`, `4-8`) plus one legend line expanding them. This is the single highest-leverage fix.
4. Leave ~30px of viewBox above the plot or the top label clips.
5. Put the legend in the emptiest quadrant, and keep its last line clear of the axis.
6. After every size change, re-render and **look at the image**. Collisions only appear visually.

## Step 6 - the fit loop

Both pages must be exactly 1123px. Measure, never eyeball:

```python
r = await pg.evaluate("""(id)=>{const e=document.getElementById(id);
  return {sh:e.scrollHeight, ch:e.clientHeight,
          over:[...e.querySelectorAll('*')].filter(n=>n.scrollHeight>n.clientHeight+2)
                 .map(n=>n.className+':'+n.scrollHeight+'/'+n.clientHeight).slice(0,8)};}""", pid)
```

`sh > ch` means clipped. Trim in this order - least damage first:

1. Cut a sentence so a paragraph loses a whole line. Biggest win, costs the least.
2. Shrink the chart's plot height.
3. Shave 0.1-0.2px off `.fine` / `.d` font sizes and 0.02-0.04 off line-heights.
4. Card padding 10 -> 9, page gap 9 -> 8.5.
5. Page bottom padding.

`sh < ch` by more than ~40px means a hole. Fill it with a real panel, not whitespace - a method strip or a step-by-step usually earns its place.

## Step 7 - render

```python
pg = await b.new_page(viewport={'width':900,'height':1200}, device_scale_factor=3.125)  # 300 DPI
await pg.goto(SRC); await pg.wait_for_timeout(1800)   # let inlined fonts settle
for pid, fn in (('front', f'{N}-front.png'), ('back', f'{N}-back.png')):
    await (await pg.query_selector('#'+pid)).screenshot(path=str(OUT/fn))
await pg.emulate_media(media='print')
await pg.pdf(path=str(OUT/f'{N}.pdf'), format='A4', print_background=True,
             margin={'top':'0','bottom':'0','left':'0','right':'0'}, prefer_css_page_size=True)
```

The page needs a print block: `@page{size:A4;margin:0}` and `.page{page-break-after:always}`.

## Step 8 - verify before you hand anything over

Run all of these every time, and report the results:

- Both PNGs are `2481 x 3509`.
- **Both QRs decode out of the rendered PNGs** (crop the corner, `cv2.QRCodeDetector`) to the exact intended URL. A QR that was right in the source can still render too small to scan; keep the back one at 23mm or larger.
- PDF is 2 pages at `209.9 x 297.0 mm`.
- Both pages report `sh == ch`.
- Grep the HTML for banned strings - an old repo owner, a removed event name, a personal name, a dataset the user asked to drop, British spellings if the user writes US English. Report the counts as zeroes.
- Every number traces to a file in the repo.

## Step 9 - deliver

During review iterations, ship **HTML only** - it renders in a second and keeps the loop fast. Generate PNGs and the PDF once the user says it is right.

On final: send all four files, then write them into the output directory. Delete superseded drafts so only the four current files remain, and say plainly which ones you deleted, since those deletes are permanent.

Tell the user the print settings: duplex, long-edge binding, no scaling.

## Prose

Poster copy is the most-read prose in the repo per word. If the user has a writing skill, read it and apply it. Failing that: active voice, short words, cut a third, no stock metaphors, no "not just X but Y", no corrective negation, one idea per sentence, concrete numbers over adjectives.

## Gotchas

- Google Fonts blocked -> `@fontsource` from npm.
- Never retype base64 from tool output; stage or read the bytes.
- Changing chart height silently reopens label collisions - always re-look.
- `justify-content: space-between` on a footer with one child left-aligns it. Fine, but check.
- A `.tail` caveat that wraps pushes the h2 onto two lines; `white-space: nowrap` plus `flex: none` on it, and shorten the text.
- Recompute per-unit numbers rather than trusting a summary, then reconcile against what the repo publishes.
