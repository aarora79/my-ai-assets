---
name: writing
description: Write prose people will actually read. Use for any prose you produce - essays, articles, emails, letters, reports, blog posts, newsletters, social posts, cover letters, talks, and summaries. Applies Orwell's six rules and strips the LLM tells - passive voice, dead metaphors, and -ly padding.
license: Apache-2.0
metadata:
  author: aarora79
  version: "1.0"
---

# Writing Skill

If you want people to read your stuff, follow Orwell's rules.

LLMs are not your friends. They write in passive voice, mix figures of speech that do not fit together, and pad every sentence with -ly words. Cut all of it.

## Orwell's rules

1. Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
2. Never use a long word where a short one will do.
3. If it is possible to cut a word out, always cut it out.
4. Never use the passive where you can use the active.
5. Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
6. Break any of these rules sooner than say anything outright barbarous.

Rule 6 outranks the other five. A stiff sentence that obeys rules 1-5 is worse than a plain one that breaks one of them.

## How to apply each rule

### 1. No stock figures of speech

Kill any phrase you have read a hundred times. If two images sit in one sentence, they will clash and the reader sees nothing.

Ban list, not exhaustive: game changer, at the end of the day, low-hanging fruit, moving the needle, paradigm shift, deep dive, unlock value, seamless, robust, journey, landscape, ecosystem (unless you mean living things), leverage as a verb, delve, tapestry, testament to, navigate the complexities.

Use a plain statement, or invent an image that fits the thing you are describing.

- Bad: This book is a game changer that unlocks seamless value across the whole reading landscape.
- Good: This book changed how I take notes. I now write one sentence per page as I read.

### 2. Short words

Prefer the short word every time: use not utilize, help not facilitate, start not commence, about not approximately, use not leverage, get not obtain, show not demonstrate, need not necessitate, before not prior to, after not subsequent to, so not accordingly, most not the majority of, buy not purchase, end not terminate.

### 3. Cut words

Delete every word that carries no weight. Common padding: in order to, the fact that, it should be noted that, it is important to note, as previously mentioned, in terms of, with respect to, a number of, at this point in time, basically, essentially, actually, really, very, quite, simply, just.

Delete throat-clearing openers. Start with the fact.

- Bad: It is important to note that, in terms of cost, the smaller car basically saves quite a lot.
- Good: The smaller car saves $2,000 a year in fuel.

Aim to cut a first draft by a third. Then read it again and cut more.

### 4. Active voice

Name the actor, then the verb. Passive voice hides who did what, and hidden actors are how blame and bad decisions escape notice.

- Bad: The application was reviewed by the committee and a decision was reached.
- Good: The committee reviewed the application and decided to fund it.

Hunt for is/are/was/were/been/being next to a past participle. Also hunt "there is", "there are", and "it is" - each one usually buries the real subject.

Keep the passive only when the actor is unknown or truly beside the point: "The house was built in 1910."

### 5. Everyday English

Say the thing in words a competent reader knows. Drop the Latin and the jargon: use for example not e.g., that is not i.e., by itself not per se, the opposite not vice versa, so far not to date, roughly not circa.

Keep the exact word when it is the precise name of the thing. A `mortgage`, a `biopsy`, an `easement`, and `compound interest` earn their place. `synergy`, `holistic`, and `operationalize` do not.

Write out an acronym on first use, then use it.

### 6. Sound like a person

Read the sentence aloud. If no one would say it, rewrite it. Break any rule above rather than write something ugly, stilted, or unclear.

## Extra rules for LLM prose

- Cut -ly adverbs. Pick a stronger verb instead. `significantly increased` -> `doubled`. `carefully considered` -> `weighed`.
- No "not only X but also Y". No "X isn't just Y - it's Z". No em-dash reveal at the end of a sentence.
- No lists of three when two facts will do.
- No summary paragraph that repeats what you just said.
- No praise of the reader, the topic, or yourself. No "great question", no "powerful and flexible".
- One idea per sentence. Short sentences beat long ones with semicolons.
- Concrete over abstract: exact numbers, names, dates, places.
- Say what happened and what it means. Skip the vision.
- Do not hedge twice. "may possibly" -> "may". Pick one level of certainty and own it.
- Use present tense for how a thing works, past tense for what happened.
- Never open with "In today's fast-paced world" or any variant.

## Sentence-shape tells

Word-level fixes are not enough. LLMs lean on a handful of sentence shapes that read as machine-made even when every word is plain. Kill these.

- No antithesis. Do not pair "X, but Y" or "not X, rather Y" for rhythm. Say the one thing you mean.
  - Bad: The move is not a risk, it is a plan.
  - Good: The move is a calculated bet.
- No corrective negation. Do not define a thing by first saying what it is not.
  - Bad: This isn't about money, it's about time.
  - Good: I did it to get my evenings back.
- No contrasting pairs or negative parallelism. Drop the "not just X, but Y" and "less A, more B" frames.
  - Bad: We didn't shrink the team, we focused it.
  - Good: We cut the team from twelve to four and shipped faster.
- No negative anaphora. Do not open three sentences in a row with "No..." or "Never..." for effect. (This list is a list, not prose.)
- No setup/payoff or landing sentences. Do not build a sentence whose only job is to tee up the next one, and do not end a paragraph on a short punchy line meant to resonate.
  - Bad: There was one thing left to decide. The price.
  - Good: The last thing to decide was the price.
- No parataxis for drama. Do not stack short clauses to build rhythm ("She read it. She signed it. She left.").
- No parallel sentence structures within a paragraph. If two sentences share the same skeleton, rewrite one.
- No paragraph pinning. Do not top and tail a paragraph with the same idea to frame it.
- No summary beats. Do not restate the point you just made in different words.
- No stacked noun phrases. Break "a customer-focused value-creation engagement model" into words that do work.
- No nominalization. Turn the noun back into its verb: "reach a decision" -> "decide", "conduct an investigation" -> "investigate", "provide support for" -> "support".
- Vary sentence length on purpose, not on a pattern. Mix short and long so the rhythm is unpredictable. Do not alternate long-short-long-short.

## Revision pass

Run this on every draft before you ship it:

1. Read it aloud. Fix anything you stumble on.
2. Search for is/are/was/were + participle. Flip each to active or justify it.
3. Search for `ly ` and delete or replace each hit.
4. Delete every phrase from the ban lists above.
5. Cut the first sentence of each paragraph if the second one already says it.
6. Scan for the sentence-shape tells above: antithesis, corrective negation, contrasting pairs, setup/payoff, parallel structure, stacked nouns. Rewrite each into a plain statement.
7. Count words. Cut a third.
8. Check every claim against something real - a source, a number, a date.
9. Apply rule 6 last: read once more and undo anything that now sounds wrong.

## Example

Before:

> It should be noted that a significant number of improvements have been implemented in this initiative, which fundamentally transforms the customer experience landscape by leveraging a robust new engagement framework that seamlessly facilitates communication at scale.

After:

> We changed how we answer customers. A person now replies within an hour, and repeat complaints dropped by a third.

45 words to 20. Named the actor. Gave the numbers.
