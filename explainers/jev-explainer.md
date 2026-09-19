# Jev: a model that decides instead of writing

TypeSafe AI shipped a model that answers typed questions in about a tenth of a second and never returns prose. This covers how it works, where it breaks, and a script you can run against your own files in the next twenty minutes.

*Written 19 September 2026 · all numbers dated and attributed · code samples in Python*

## Contents

- [What Jev is](#what-jev-is)
- [How it answers ten questions in the time an LLM writes one word](#how-it-answers-ten-questions-in-the-time-an-llm-writes-one-word)
- [One call, start to finish](#one-call-start-to-finish)
- [The three primitives](#the-three-primitives)
- [The request and the response](#the-request-and-the-response)
- [Five patterns that hold up](#five-patterns-that-hold-up)
- [What it gets wrong](#what-it-gets-wrong)
- [Repos worth reading](#repos-worth-reading)
- [Run it yourself](#run-it-yourself)

## What Jev is

Think about what your code asks a language model to do most of the day. Rarely "write me an essay". Far more often: is this ticket about billing? Is this diff risky? Should I read more of the file before I edit it? Each one is a decision with a small set of answers, and you know the answers before you ask: billing, technical or sales; risky or not.

Getting one of those answers takes more machinery than the question deserves. You write a prompt, the model writes a paragraph or a JSON blob back, and your code parses it, checks that the parse worked, and handles the case where it did not. You are asking a machine that produces text to make a choice, then turning the text back into the choice you wanted. The text in the middle is overhead, and you pay for it twice: in tokens, and in the seconds somebody spends waiting.

Jev deletes the middle. You hand it **state**, meaning whatever your program already holds: the ticket, the file, the last six turns of a conversation. With the state you send a list of questions, each one carrying its possible answers written out in advance. What comes back is the answers, with no sentence wrapped around them, nothing to parse and nothing to retry.

TypeSafe calls this a **System One model**, after Daniel Kahneman's name for fast, automatic thinking: the judgment you reach without deliberating, the way you read a face as angry before you could explain how you knew. Kahneman's System Two is the slow, effortful kind you use on long division or a legal argument. A frontier LLM does System Two work, and you can talk it into doing System One work badly. Jev does one of those jobs and refuses the other.

The company's own line for it: *"a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."* Take that as a promise about the call shape rather than a boast. You already know how to call a function, branch on what it returns and write a test for it. The API asks nothing else of you.

| Number | What it is |
| --- | --- |
| **70–500 ms** | End to end. Most calls land near 100 ms, per TypeSafe. |
| **$0.042** | Per million input tokens. Output tokens cost nothing. |
| **0%** | Malformed answers, by construction rather than by measurement. |
| **12.2×** | Cheaper than 13 separate calls, on a 53,777-character document. |

*Vendor figures from the TypeSafe launch post and docs, September 2026. Nobody outside the company has reproduced the latency yet.*

The time gap comes from the shape of the two calls. A frontier LLM asked to classify that ticket loads the prompt and then produces one token at a time, feeding each token it has written back in before it picks the next. That loop is what **autoregressive** means, and it explains why a long answer takes longer than a short one: the model runs itself once per token. TypeSafe measured those round trips at 3 to 329 seconds. Jev takes in the same state once and produces every answer at the same time, which is what makes a tenth of a second possible at all.

```text
  AUTOREGRESSIVE LLM                     JEV
  ==================                     ===

  state + prompt                         state + 13 questions
         |                                       |
         v                                       v
  +----------------------+     +--------------------------------+
  | one token, then the  |     | one prefill: the state read    |
  | next, then the next  |     | once; each question is scored  |
  |                      |     | against it, none sees another's|
  | [tok1]>[tok2]>[tok3] |     | answer                         |
  |        > ... last    |     +--------------------------------+
  |                      |        |        |        |        |
  | then: parse it,      |        v        v        v        v
  | validate the schema, |     +------+ +------+ +------+ +------+
  | retry when it comes  |     |choice| |score | |noul  | |noul  |
  | back malformed       |     |pick  | |rate  | |true? | |true? |
  +----------------------+     |one   | |it    | |      | |      |
         |                     +------+ +------+ +------+ +------+
         v                                   |
  {"category": "billing"}                    v
  3 - 329 s                    typed answers + probabilities
                               70 - 500 ms
```

*The shape of the two calls. Jev's three question types appear on the right: choice picks an option, score rates against a rubric, noul answers is this true. A thirteenth question there costs its own tokens and almost no extra time.*

## How it answers ten questions in the time an LLM writes one word

Three design choices produce that speed. Each one also costs something.

**The architecture is non-autoregressive.** Jev produces all of its outputs from a single pass instead of feeding each token back in, which is exactly the loop it removes. TypeSafe describes it as parallel sampling that is hardware-aware. Jev scores every question in a request against the same state, none of them sees another's answer, so the model works on all of them at once. TypeSafe says it found no batching penalty past normal sampling noise, which means a request carrying twelve questions costs the tokens of twelve and about the wall-clock of one. The price of that design is that questions cannot build on each other. If question B needs the answer to question A, you are making two calls, and the round trip you saved comes straight back.

**You fix the output space in advance.** You list the options before the call, so the model chooses among your strings rather than inventing one of its own, and it reports how the probability mass fell across them. This is why the 0% type-error rate is structural rather than measured: a malformed answer has nowhere to live, because no free-form text exists for it to live in. You will never write a retry for a broken parse again. You have learned nothing about whether the answer is *right*, and a confidently wrong answer arrives in the same well-formed shape as a correct one.

**Training targeted calibration**, which means the probability the model states matches how often that answer turns out right. TypeSafe trained Jev with Reinforcement Learning for Calibrated Decisions, which rewards that match rather than rewarding a helpful-sounding reply. In plain terms: take every answer the model marked 0.9, and about nine in ten of them should be correct. That property lets you put the number inside an `if` statement, and that claim is the one worth testing yourself, because every gate and threshold you build on Jev inherits it. The number you test is **confidence**, the share of the probability mass sitting on the answer the model picked.

> **THE OPEN REPRODUCTION TELLS YOU MORE THAN THE BLOG POST.**
>
> Jev itself is closed, so the mechanism above comes from what TypeSafe chooses to publish. The cheapest way to see how a call like this can work is to read somebody rebuilding it on parts you can inspect. [openjev-sglang](https://github.com/ekzhang/openjev-sglang) rebuilds the interface on open weights with a one-token readout: read the state once, append a per-question suffix, then take the model's own scores for the answer labels (its log-probabilities) and renormalize them over those labels alone. Labels are `A`–`Z` and verified single-token pairs such as `AA`, so every answer reads out in exactly one token. Jev may not work this way inside. openjev is still the cheapest way to get the same call shape on a model you host, and it runs on SGLang, an open-source inference server.

## One call, start to finish

A support ticket arrives. Three things have to happen to it: it goes to a team, somebody decides how urgently, and the billing system may need to cut a refund. Three decisions over one piece of text, and one call can carry all three.

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()

ticket = """I have been charged twice for order A-104. The second charge
hit this morning. I have emailed twice and nobody has replied.
Please refund the duplicate today."""

answers = client.system_one(
    model="jev-1.13.0",
    state={"ticket": ticket},
    questions={
        # Choice: pick exactly one of the options you list
        "team": Choice(
            instructions="Which team should handle this ticket",
            criteria={
                "billing":   "Charges, invoices, refunds",
                "technical": "Something is broken or behaving wrong",
                "sales":     "Pricing, plans, account changes",
            },
        ),
        # Score: place the ticket on a rubric you order yourself
        "anger": Score(
            instructions="How angry the customer sounds",
            criteria=[
                "Calm, stating facts",
                "Frustrated but civil",
                "Furious, threatening to leave",
            ],
        ),
        # Noul: one statement, answered as a probability
        "wants_refund": Noul(
            instructions="The customer is asking for money back",
        ),
    },
).answers
```

That is one request and one round trip, whatever the three questions happen to be. Printing what came back:

```python
answers["team"].choice           # "billing"
answers["team"].confidence       # 0.94
answers["team"].probabilities    # {"billing": 0.94, "technical": 0.04, "sales": 0.02}

answers["anger"].score           # 1.4
answers["wants_refund"].noul     # 0.97
```

*Illustrative values rather than a recorded run. The field shapes come from TypeSafe's SDK docs; the numbers are what a call like this returns.*

Read them one at a time, because each type answers a different kind of question about the same text.

- `team.choice` is one of the three strings you listed and cannot be anything else, so the next line of your code switches on it without a branch for surprises.
- `team.probabilities` shows where the rest of the mass went. At 0.94 against 0.04 and 0.02 the model was not torn. A ticket that came back 0.51 billing and 0.47 technical is the one you want a human to look at, and the distribution is the only place that shows up.
- `anger.score` is 1.4 on the three-level rubric you wrote, whose levels count 0, 1 and 2 in the order you listed them. It sits between "frustrated but civil" and "furious", which tells you more than either label alone. Scores landing between levels are normal, so treat the rubric as a ruler rather than three boxes.
- `wants_refund.noul` is 0.97, a probability rather than a yes. A noul carries no separate confidence field, because the number already is the confidence.

The code that acts on those answers is ordinary Python, and none of it parses anything.

```python
team = answers["team"]
if team.confidence < 0.6:
    queue_for_human(ticket)                  # the model is telling you it is unsure
else:
    assign(ticket, team.choice)

if answers["anger"].score > 1.2:
    mark_priority(ticket)                    # angry enough to jump the queue

if answers["wants_refund"].noul > 0.9:
    open_refund_case(ticket, amount="auto")  # money moves, so the bar is high
```

Three thresholds at three different heights, each written next to the action it guards. Sending money needs 0.9; putting a ticket in a queue needs 0.6; nothing needs a retry loop or a schema validator.

What it cost: the ticket runs about 60 tokens and the questions with their criteria maybe 120 more. At $0.042 per million input tokens, those 180 tokens come to $0.0000076, and the answers land in roughly a tenth of a second.

## The three primitives

Every question you can ask is one of three types, and the type you pick is a claim about the shape of the answer. Pick the wrong shape and you fight it later: a yes-or-no judgment forced into a five-option choice throws away the single number you wanted. Each answer carries its probability distribution and its confidence.

| Type | Asks | Returns |
| --- | --- | --- |
| `Noul` | Is this statement true of the state? | `.noul`, a probability from 0 to 1. No separate confidence field, because the number is the confidence. |
| `Choice` | Which of these options fits? Up to 255 of them. | `.choice`, `.probabilities` over every option, `.confidence`. |
| `Score` | Where on this ordered rubric does it sit? | `.score`, which lands between levels (1.035 is a real answer), `.probabilities`, `.confidence`. |

Two rules govern how you write the questions, and breaking the first causes most of the trouble. Keep each question atomic, so that it asks about exactly one thing. "Is this ticket urgent and about billing?" has no honest answer when the ticket is urgent and about something else; the model picks one half of your question for you and never says which half it picked. Ask the two questions separately. The second rule follows: when a judgment has several parts, keep the weighting in your own code rather than inside the wording of one question, where you can read it in a diff and change it without retraining anything.

## The request and the response

One endpoint does everything: `POST https://api.typesafe.ai/v1/systemone`. The body holds `state`, `model` and `questions`. The response holds `model`, `answers` keyed by the ids you chose for your questions, and `usage`. No session, no thread, no conversation history to manage, because nothing carries over from one call to the next. Every call is a function call with its arguments in front of it.

State can be a string, an object, or an array. Use an object. Named fields tell the model what each part of the state is, so `{"ticket": …, "customer_history": …}` reads differently from the same two blocks of text glued together, where the model has to guess where one ends. Named fields also let you diff one state against another once you start logging every call, which is what you will want the first hour an answer surprises you.

```text
  REQUEST                            RESPONSE
  =======                            ========

  model: "jev-latest"                answers.tier.choice        "high"
  state: { ... }                     answers.tier.confidence    0.91
    a string, an object, or          answers.tier.probabilities
    an array of text.                  high  ####################  .78
    No images.                         med   ####                  .18
                                       low   #                     .04
  questions: {
    tier:   Choice(criteria={..})    answers.risk.score         1.035
    risk:   Score(criteria=[..])     answers.urgent.noul        0.88
    urgent: Noul(instructions=..)
  }                                  usage.input_tokens         4,218
                                     usage.output_tokens        0
  ---------- ~100 ms ---------->

  Every question sees the same state. None sees another's answer.
```

*Log the whole distribution. A hundred 0.51 answers that all came out right tell you something stored labels cannot.*

## Five patterns that hold up

### 1. Fan out

Ask for everything you might want in one request, including the signals you do not need yet. TypeSafe batched 13 questions against a 53,777-character document and measured it at 12.2× cheaper and 10× faster than 13 separate calls. The reason is the state rather than the questions: sending 53,777 characters once and asking thirteen things beats sending it thirteen times. A fourteenth question costs its own tokens and close to no time.

### 2. Gate on confidence, and set a different gate per action

The cost of being wrong differs by action, so a single threshold set once for a whole system is wrong nearly everywhere it applies. Showing an account balance to the person who owns the account can run at 0.5, because a wrong answer costs a puzzled user and one more click. Moving money at 0.5 is indefensible. Put the bar where the consequence is, and write the number beside the action it guards rather than in a settings file three directories away.

```python
action = response.answers["intent"]

if action.confidence < 0.5:
    route_to_human(user_message)             # genuinely unsure

elif action.choice == "check_balance":
    show_balance(account_id)                 # read-only, low bar

elif action.choice == "approve_transfer":
    if action.confidence > 0.85:             # money moves, high bar
        approve_transfer(account_id)
    else:
        ask_user_to_confirm("Approve this transfer?")
```

```text
   0.0                    0.5                  0.85              1.0
    |======================|====================|=================|
             HUMAN                 CONFIRM              ACT

    below 0.5     the model is telling you it does not know
    0.5 to 0.85   one click from the user settles it
    above 0.85    act without asking

    The gate moves with the consequence: showing a balance can run at
    0.5, and moving money should not.
```

*The middle band is the interesting one. Log every call that lands there, and that log becomes the set you tune the thresholds against.*

### 3. Composite scoring

Split a judgment into dimensions, ask each one on its own, and weight them in code. Asking "how good is this candidate" in a single question hides the weighting inside the model, where you cannot see it, argue with it or change it. Three questions and three weights put the same judgment in front of you.

```python
composite = (
    0.40 * (response.answers["python_depth"].score / 4) +
    0.25 * (response.answers["team_leadership"].score / 4) +
    0.35 * (response.answers["system_design"].score / 4)
)
```

The weights then live in a diff, so changing how much system design counts takes a pull request rather than a prompt rewrite.

### 4. Cascade

Jev routes. Plain code handles the easy cases and a frontier model takes the rest. The expensive model then only sees the requests that need it, and in most systems those are a small share of the traffic. The routing decision costs a fraction of a cent and happens before anything expensive starts.

```python
if intent.confidence < 0.5:
    return route_to_human(message)

if intent.choice == "order_status":
    return lookup_order(message)             # pure code, no model
elif intent.choice == "complaint":
    if complexity.score > 1:
        return route_to_human(message)
    return handle_with_llm(message, SPECIALIST)
```

### 5. Retrieve, then judge

Filter in code first and send only the fields the question needs. Two things get worse as you pad the state. Accuracy falls, because the model is reading material with no bearing on what you asked. And you pay for every token of the padding, on every call, forever. A retrieval step that returns the five rows that matter beats one that returns fifty and hopes the model sorts it out.

## What it gets wrong

TypeSafe publishes its own failure modes, which is more than most model cards do. Almost every item below has the same workaround: do that part in Python, and ask Jev only for the judgment Python cannot make.

- **It cannot count.** Characters in a word, occurrences of a term, items in a list: all unreliable.
- **Date and number comparisons fail.** Which of two dates came first, how far apart they are, whether two hex colors are close. Do this in Python.
- **It reads literally.** Negations and scoping words land at face value, so *"this is not a refund request"* can score high on a refund question.
- **Padding costs accuracy.** State you did not need for the question drags the answer down.
- **User-controlled text steers it.** Content written to argue for its own classification moves the answer. Treat state built from user input the way you treat a prompt: untrusted.
- **No text, ever.** No explanations, no code, no summaries. It takes no images, audio or video.
- **Accuracy is 67.8% on TypeSafe's own benchmark**, scored against consensus labels from GPT-6 and Claude. TypeSafe ran that evaluation itself, so reproduce it on your own data before you commit to a gate.

>
> **PIN THE VERSION.** Both SDKs default to `jev-latest`. The moment you tune a threshold against measured behavior, pin the model (`"jev-1.13.0"`), or a silent upgrade will move your answers under a gate you calibrated last month.

## Repos worth reading

A few hundred projects appeared in the weeks after launch, and [cobanov/awesome-jev](https://github.com/cobanov/awesome-jev) tracks them. Most are wrappers. The ones below are worth an hour each, because they show a design decision you would otherwise have to make blind: where to put the threshold, what to do when the model is unsure, and how to keep a fast model from quietly taking over a slow model's job.

| Repo | What it does | Why read it |
| --- | --- | --- |
| [winnow](https://github.com/GhalebDweikat/winnow) | Splits Read/Bash/Grep output into 25-line blocks, asks Jev which blocks Claude Code needs, and replaces the rest with a three-line stub and a cache key. | The closest published thing to context pruning done with judgment. A hundred blocks come back in one call. Its defaults are conservative: `WINNOW_DROP=0.1`, and never hide a block showing an error. |
| [foreman](https://github.com/thruwire/foreman) | Watches a Codex worker with nine nouls per cycle: `meaningful_progress`, `worker_stuck`, `work_off_track`, `needs_human`, `ready_to_finish` and four more. | Supervision as a second loop that never touches the agent's tool choice. The policy is a table of thresholds (`needs_human` 0.80, `ready_to_finish` 0.85) and the actions are an enum. |
| [jev-guard](https://github.com/leepokai/jev-guard) | Scores tool-call risk across agents before the call runs. | The guardrail version of the same idea, one layer earlier than foreman. |
| [openjev-sglang](https://github.com/ekzhang/openjev-sglang) | Serves the same API from open weights on SGLang, via one-token logprob readout. | Self-hosting, and the clearest explanation of how a call like this can work. |
| [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) · [jevcal](https://github.com/abhixhek/jevcal) | Reproducible evaluation, and fitting confidence thresholds to your own data. | Use both before trusting a gate. jevcal turns the threshold from a guess into a measurement. |
| [typesafe-ai/skills](https://github.com/typesafe-ai/skills) | The official agent skill. `claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`. | Keeps the docs and cookbooks in front of the agent writing your Jev code. |
| [typesafe-snake](https://github.com/sorrycc/typesafe-snake) · [typesafe-mario](https://github.com/fhshaik/typesafe-mario) | One Choice per game tick. | Toys, and the fastest way to feel what a 100 ms decision loop buys you. |

LangChain shipped `langchain-typesafe` with two middlewares worth reading before you write your own: `ModelRouterMiddleware`, which picks a model per request from criteria you write, and `AutoModeMiddleware`, which blocks risky tool calls before they run.

## Run it yourself

One dependency, one environment variable, one file. The script below reads a README — from disk or from a GitHub URL — and asks Jev five questions about it in a single call, using all three question types. None of it is pseudocode: copy it, run it, and the numbers come back from your key rather than from this page.

```bash
pip install typesafe-sdk
export TYPESAFE_API_KEY="sk-..."
```

```python
"""readme_check.py - ask Jev five questions about a README.

    python readme_check.py                          # ./README.md
    python readme_check.py path/to/README.md        # any local file
    python readme_check.py https://github.com/psf/requests
"""
import pathlib, sys, urllib.request
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

def load(target):
    """Return (name, text) for a local path or an http(s) URL."""
    if not target.startswith(("http://", "https://")):
        path = pathlib.Path(target)
        if not path.exists():
            sys.exit(f"no file at {path}")
        return path.name, path.read_text(encoding="utf-8")

    url, parts = target, target.split("/")
    if "github.com" in url and "/blob/" in url:            # a file page
        url = url.replace("github.com", "raw.githubusercontent.com", 1).replace("/blob/", "/", 1)
    elif "github.com" in url and len(parts) == 5:          # a repo root
        url = f"https://raw.githubusercontent.com/{parts[3]}/{parts[4]}/HEAD/README.md"
    with urllib.request.urlopen(url, timeout=20) as response:
        return url.rsplit("/", 1)[-1], response.read().decode("utf-8", "replace")

name, text = load(sys.argv[1] if len(sys.argv) > 1 else "README.md")

answers = TypeSafeClient().system_one(
    model="jev-1.13.0",
    state={"filename": name, "readme": text[:40000]},
    questions={
        "audience": Choice(
            instructions="Who is this README written for",
            criteria={
                "user":        "Someone who wants to install and use the thing",
                "contributor": "Someone who wants to change the code",
                "evaluator":   "Someone deciding whether to adopt it",
            },
        ),
        "setup": Score(
            instructions="How complete the setup instructions are",
            criteria=[
                "No install or setup steps at all",
                "Steps exist but assume things they never state",
                "A reader could follow them start to finish",
            ],
        ),
        "has_example":   Noul(instructions="The document shows at least one worked example"),
        "explains_auth": Noul(instructions="The document explains how to authenticate"),
        "sounds_stale":  Noul(instructions="The document mentions versions or features that sound out of date"),
    },
).answers

print(name)
print(f"  written for     {answers['audience'].choice:12} ({answers['audience'].confidence:.2f})")
print(f"  setup steps     {answers['setup'].score:.1f} / 2")
print(f"  worked example  {answers['has_example'].noul:.2f}")
print(f"  auth explained  {answers['explains_auth'].noul:.2f}")
print(f"  sounds stale    {answers['sounds_stale'].noul:.2f}")

if answers["setup"].score < 1 or answers["has_example"].noul < 0.3:
    print("\n  -> worth a rewrite before anyone outside the team reads it")
```

`load()` takes a local path or a URL and works out which it has from the `http://` or `https://` prefix. A GitHub file page and a bare repo URL both get rewritten to their raw form, so `python readme_check.py https://github.com/psf/requests` reads that project's README without you hunting for the raw link. The fetch uses `urllib` from the standard library, which keeps the dependency count at one.

The state is a dict with named fields rather than one blob of text. The script truncates the README at 40,000 characters, because padding the state costs accuracy as well as money. The model is pinned, so the thresholds you tune today still mean the same thing next month.

Point it at twenty READMEs you already know well, and read the output against what is in the files. You are not testing whether Jev is clever. You are testing the one claim everything else on this page rests on: that when it says 0.9 it is right about nine times in ten, on your material rather than on TypeSafe's. Twenty documents cost a fraction of a cent and tell you more than any benchmark page can, because no benchmark page has seen your states.

Two experiments follow from there, both in the same file. Add a sixth question and watch the wall-clock barely move, which is fan-out doing its work in front of you. Then change the model back to `jev-latest` and re-run the same twenty files, which shows you what the pin is protecting.

## Sources

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — TypeSafe AI
- [TypeSafe documentation](https://docs.typesafe.ai/) — primitives, state, HTTP API, patterns
- [A deep look at Jev](https://flaviocopes.com/jev/) — Flavio Copes, on the architecture, latency and limits
- [How to use Jev](https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e) — practical patterns and failure modes
- [Building a harness with Jev](https://www.langchain.com/blog/building-a-harness-with-jev) — LangChain, on routing and guardrail middleware
- [cobanov/awesome-jev](https://github.com/cobanov/awesome-jev) — the project list
- [typesafe-sdk-python](https://github.com/typesafe-ai/typesafe-sdk-python) · [typesafe-sdk-js](https://github.com/typesafe-ai/typesafe-sdk-js) — official SDKs
- [InfoWorld](https://www.infoworld.com/article/4223468/typesafe-ais-new-models-work-with-machines-not-humans.html) · [heise](https://www.heise.de/en/news/AI-model-Jev-to-make-machines-decide-faster-11457071.html) — press coverage
