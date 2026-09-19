---
name: explainer
description: Build a self-contained HTML explainer for a technical topic - what it is, how it works, what it cannot do, and what to build with it. Teaches in dependency order, defines every term before using it, and ships one page with inline SVG diagrams, runnable code and dated sources. Use for explainers, primers, briefings, onboarding pages, course handouts and teaching material.
license: MIT-0
metadata:
  author: aarora79
  version: "1.3"
---

# Explainer

Write the page a smart colleague needs to understand a thing they have never met, and to start building with it the same afternoon.

The output is one HTML file: no build step, no second file, no server. A reader opens it, scrolls once, and knows what the thing is, how it works, where it breaks, and what to try first.

## Two skills, not one

Write every sentence under the `writing` skill in this repo (`skills/writing/`). Load it before you draft. It governs the prose: Orwell's six rules, the ban lists, the sentence-shape tells, the revision pass.

This skill adds what teaching needs on top: the order ideas arrive in, the rule that no term appears before its definition, and the habits that turn an assertion into an explanation. It also names which of the writing skill's compression rules bend when the reader is learning the subject rather than catching up on it.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Topic | yes | A model, a protocol, a library, a paper, a system in your own codebase. |
| Audience | no | Default: an engineer who is strong elsewhere and new here. |
| Code language | no | Default: the language the reader will use it from. Pick one and stay in it. |
| Output path | no | Default `explainers/<topic>-explainer.html` in the repo you are working in. |

## Step 0 - ask three questions, then commit

Ask once, in one call, before any research: **depth** (deep walkthrough, skimmable brief, or teaching material), **code language**, and **where the file lands**. Take the default and say which you took if the user is away. Do not ask again later.

## Step 1 - research before you open the file

Opening the page first anchors you on layout while you still have nothing true to put in it.

- Read the primary source. The vendor's own docs, the RFC, the paper, the SDK README, the repo.
- Read the thing itself when you can reach it. A record shape you sampled from a real file beats a record shape you remember. A number you measured beats a number you were told.
- Find the open reproduction. Somebody rebuilding a closed thing on open parts usually explains the mechanism better than its own launch post.
- Date every number and name its owner. `70-500 ms, vendor figure, September 2026` is honest. `fast` is not.
- Keep the URL of everything you use. The page ends with a source list and it is not optional.

## Step 2 - the teaching contract

This is the part that separates an explainer from a summary. Hold all of it.

1. **The first sentence names the thing in plain words.** No history, no category taxonomy, no acronym, no "in recent years". A reader who knows nothing should parse it.
2. **No term before its definition.** Build a term ledger first: every word the target reader may not hold. Each one gets a definition in the sentence where it first appears, in six words or fewer, or it gets cut. Then use it freely for the rest of the page - repeating the definition insults the reader who took it the first time.
3. **One new idea per section, in dependency order.** Never forward-reference. If section 4 needs an idea from section 6, the sections are in the wrong order.
4. **Anchor every abstraction to something the reader already holds.** A shape they can picture, a number they can hold, a tool they have used. "One prefill, then every question scored against it" beats "parallel non-autoregressive inference".
5. **Show a worked example with real values before the reference material.** Concrete first, general second. The API table means something once they have seen one call return one answer.
6. **Say what it cannot do, with the same weight as what it can.** A section on the failure modes, not a footnote. A reader who hits the limit you skipped stops trusting the rest.
7. **Explain the mechanism or say you do not know.** Restating the marketing in your own words is worse than silence, because it reads as understanding.
8. **Numbers over adjectives, always.** `$2.52 for ten thousand decision points` teaches. `cheap` does not.
9. **A reader who stops after any section has gained something whole.** No section exists only to set up the next one.
10. **Cut the words that punish the reader**: simply, just, obviously, of course, as you know, clearly, trivially, it goes without saying, everyone knows. Each one tells the reader who did not know that they should have.

**ELI5 means the order concepts arrive in, not baby talk.** Do not water the engineering down, do not round the numbers off, and do not swap the exact term for a vague one. Define `idempotent` and then use `idempotent`.

### Explain, do not assert

A summary states what is true. An explainer shows why it is true and why the reader should care. The difference is visible sentence by sentence. Read a paragraph and mark each sentence **A** for assertion or **E** for explanation. A paragraph of all A's is a summary wearing an explainer's heading, and it is the failure this skill exists to prevent.

Eight habits produce the E sentences:

1. **Every claim that matters gets a because.** "Jev returns typed answers" is an assertion. "Jev returns typed answers, so the parse step and the retry that guards it both disappear from your code" explains.
2. **Lead with the problem, then the thing.** The reader should feel the pain a paragraph before they meet the fix. A reader who has not felt the problem has no place to put the solution.
3. **Answer the question the reader is about to ask.** Read the draft as somebody who does not already agree. Wherever they would say "wait, why" or "so what", the answer belongs in the next sentence, not three sections later.
4. **Say the hard idea twice: once in the domain's words, once in ordinary ones.** This is the one place repetition earns its keep. "Calibrated" and "when it says 0.9 it is right about nine times in ten" are the same sentence for two different readers.
5. **Give the mechanism an analogy, then say where the analogy breaks.** An analogy nobody bounds turns into a wrong mental model that the reader keeps for years.
6. **Walk one example end to end before you generalize.** Real values, in order, with the intermediate state shown. The general rule lands once the reader has watched it happen once.
7. **Length follows difficulty, not importance.** Three sentences for the idea they will trip over, one for the idea they will not. A section that is important and obvious stays short.
8. **Never flag significance.** "This matters more than it looks" is an assertion about importance, which is the weakest assertion there is: the reader has no way to check it and no reason to believe it. Replace the flag with the consequence — what breaks, what it costs, what you no longer have to write. If you cannot name the consequence, the sentence was decoration and it goes.

### Which writing-skill rules bend here

The `writing` skill is built for compression, and compression fights teaching. These are the only rules that move, and they move this far and no further:

| Rule in `writing` | In an explainer |
|---|---|
| Cut a first draft by a third | Cut the padding, keep the explanation. Word count follows difficulty. |
| No summary paragraph that repeats what you just said | Holds at the end of the page. After a hard mechanism, one short "what just happened" line is a checkpoint, not a summary. |
| No lists of three when two facts will do | Relaxed when the three are real: three question types are three. |
| No setup or payoff sentences | Holds for rhythm. A sentence that poses the reader's actual question is the question, not a setup. |
| One idea per sentence | Holds, and matters more here. It is what makes a long explanation readable. |
| Concrete over abstract, numbers over adjectives | Holds without exception. |
| No passive, no ban-list phrases, no -ly padding, no antithesis, no corrective negation | Holds without exception. |

## Step 3 - the shape that works

Not every explainer needs every section. It needs them in this order.

| Section | Job |
|---|---|
| Title and standfirst | Name the thing and the payoff in two sentences. The standfirst says what the page covers. |
| Number strip | Three or four figures that set the scale, each with its source and date under it. |
| What it is | Plain words, then the vendor's own line if they have a good one. |
| How it works | At most three design choices, each a bolded lead and a short paragraph. This is where the first diagram goes. |
| The primitives or the API | The reference material, after the reader has seen one worked call. |
| Patterns | What people do with it that holds up. Code for each. |
| What it gets wrong | The limits, the failure modes, the number the vendor scored themselves. |
| Prior art | Repos and projects worth reading, with one line each on why. |
| Build ideas | The section the reader came for. Ground each in something they already own. |
| Twenty minutes to first answer | Install, key, one script, one check they can run. |
| Sources | Every URL, plus anything you sampled from a local file, with the date. |

**Sources go last, every time.** Link inline where a claim needs its source, and keep the
full list at the end so the page closes on its evidence. A reader who wants to check you
should find everything in one place without scrolling back through the argument.

## Step 4 - diagrams

A picture earns its place when it shows a mechanism, a flow, or a before and after. It earns nothing when it decorates.

- Draw inline SVG with a `viewBox` and `width: 100%`. No image files, no chart library.
- Paint with the page's CSS variables (`fill: var(--ink)`, `stroke: var(--accent)`), so one diagram works in light and dark.
- Label every box. A shape with no words is a shape.
- The caption says what to notice, not what the picture contains.
- Three to five diagrams across a long page. Past that they stop being landmarks.

## Step 5 - the page

Typography that Google's own documentation would recognise, measured rather than eyeballed.

```css
:root {
  --measure: 64ch;              /* ~72 characters a line, inside the 50-75 band */
  --wide: 960px;                /* figures, tables and code break out to here */
  --sans: Inter, Roboto, -apple-system, "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", "Roboto Mono", ui-monospace, Menlo, Consolas, monospace;

  --bg: #ffffff;  --panel: #f8f9fa;  --ink: #202124;  --ink-2: #3c4043;
  --ink-3: #5f6368;  --rule: #dadce0;  --accent: #1a73e8;  --accent-2: #b06000;
  --code-bg: #f1f3f4;
}
/* dark: --bg #202124, --panel #292a2d, --ink #e8eaed, --ink-3 #9aa0a6,
   --rule #3c4043, --accent #8ab4f8, --accent-2 #fdd663, --code-bg #282a2e */
```

| Element | Size |
|---|---|
| Body | 18px / 1.7 |
| H1 | `clamp(32px, 4.6vw, 42px)` / 1.16 |
| H2 / H3 / H4 | 28 / 21 / 17px |
| Code block | 14.5px / 1.65 |
| Table | 16px, `font-variant-numeric: tabular-nums` |
| Caption, byline | 14.5px |

Hold the prose to the measure and let the wide things break out of it:

```css
.wrap { display: grid; grid-template-columns: 1fr min(var(--measure), 100%) 1fr; }
.wrap > * { grid-column: 2; }
.wrap > figure, .wrap > table, .wrap > pre { grid-column: 1 / -1;
  width: min(100%, var(--wide)); justify-self: center; }
```

Seven rules for the file itself:

- **One file.** CSS inline in a `<style>` block, images as `data:` URIs, no JavaScript unless the page teaches something only interaction can teach.
- **Fonts.** A Google Fonts `<link>` plus the fallback stack above is enough for a page that lives online. For a page that has to work offline or behind a proxy, pull woff2 from npm (`npm pack @fontsource/inter @fontsource/jetbrains-mono`) and base64-inline them.
- **Both themes.** `prefers-color-scheme` with a `[data-theme]` override, and an explicit `background` on `body`.
- **Phone width.** 16px gutter, no horizontal page scroll, tables allowed to scroll inside their own box.
- **Print.** A small `@media print` block: 11pt body, `break-inside: avoid` on figures, code and tables.
- **Every code block carries a copy control.** A reader who wants to run your example should not have to select it by hand. A button in the top-right corner of each block, showing a clipboard icon and the word Copy, flipping to Copied for a second after a click. This is the page's only JavaScript: about thirty lines, no dependencies, `navigator.clipboard.writeText` with a hidden-textarea fallback for browsers that refuse it. With JavaScript off the code is still there and still selectable.
- **A table of contents** once the page passes six sections.

## Step 6 - verify before you ship

Run all of it. Every check has caught something real.

1. The `writing` skill's revision pass, on the prose with the code blocks stripped out.
2. **First-use check.** For each term in the ledger, find its first occurrence and confirm the definition sits in the same sentence.
3. **Measure.** Render the page and count characters a line. Outside 50-75, change `--measure`.
4. **Contrast.** Every text-on-background pair at 4.5:1 or better, in both themes.
5. **Code.** Parse every code block. A snippet that does not compile teaches the wrong thing.
6. **Render.** Screenshot light, dark and 390px wide, and look at them. Check that nothing overflows its container.
7. **Links.** Every URL in the source list resolves.
8. **Numbers.** Every figure on the page traces to a source in the list, with a date.
9. **Register.** Take three sections and mark every sentence A or E, as above. A section with no E sentences is a summary. Rewrite it before you ship.

```python
# the two checks worth automating first
import ast, re, pathlib
s = pathlib.Path(out).read_text()
for i, b in enumerate(re.findall(r'<pre><code>(.*?)</code></pre>', s, re.S)):
    code = b.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    if not code.strip().startswith(('pip ', 'npm ', 'export ')):
        ast.parse(code)                      # raises on the block that is wrong

prose = re.sub(r'<pre>.*?</pre>|<svg.*?</svg>|<[^>]+>', ' ', s, flags=re.S)
punishers = r'\b(simply|just|obviously|of course|as you know|clearly|trivially)\b'
print(set(m.group() for m in re.finditer(punishers, prose, re.I)))
```

```python
# measure and contrast, with playwright
pg.goto(f"file://{out}")
print(pg.evaluate("""() => {
  const p = [...document.querySelectorAll('p')].find(p => p.textContent.length > 300);
  const cs = getComputedStyle(p), c = document.createElement('span');
  c.textContent = 'abcdefghijklmnopqrstuvwxyz'; c.style.font = cs.font;
  document.body.appendChild(c);
  return Math.round(p.getBoundingClientRect().width / (c.getBoundingClientRect().width / 26));
}"""))
```

## Step 7 - read it once more, top to bottom

Every check so far looks at one sentence or one number. This one looks at the whole page,
and it is the last thing you do before shipping.

Read it as the reader would, start to finish, in one sitting. Three questions:

- **Does it flow?** Each section should follow from the one before it. A section you have
  to re-read to work out why it is there belongs somewhere else, or nowhere.
- **Does anything repeat?** By now you have written the same idea twice in two places
  without noticing. Keep the better one. A worked example that demonstrates a rule beats
  the sentence that stated it, so cut the sentence.
- **Has anything stopped earning its place?** A paragraph that was load-bearing in the
  first draft is often dead weight once the rest arrived. Cut it, even though it took an
  hour to write.

The test for every paragraph: the reader is giving you their attention and you asked for
it, so what are they getting back for this one?

Expect to cut. On the page this pass was written for, it removed a 33-line code block
that duplicated the worked example, four sentences that a later section said better, and
a caption that repeated the paragraph above it.

## Ship it

- Write to `explainers/<topic>-explainer.html`, beside the repo it explains when there is one.
- **Never add a version suffix to a shipped file.** A second draft overwrites the first.
- Say in one line what the page covers and where it landed. The reader opens it themselves.

## Stay inside the lines

- Do not open the HTML before the research is done.
- Do not use a term the page has not defined.
- Do not state a number without a date and an owner.
- Do not present a vendor's self-scored benchmark as measured fact.
- Do not write a section whose only job is to introduce the next one.
- Do not ship a section that is all assertion. A reader who did not already know the subject has to learn why, not only what.
- Do not stage the next sentence. No "now look at", no "here is the thing", no applause line at the end of a section.
- Do not tell the reader a fact is important. Show the consequence and let them decide.
- Do not ship without the final read-through. The draft you stop editing is not the draft that reads best.
- Do not add a diagram that repeats what the paragraph above it already said.
- Do not pad to length. A page that earns 1,200 words should be 1,200 words.
