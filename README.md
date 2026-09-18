# My AI Assets

A collection of prompt templates and reusable skills for working with Claude and other LLMs.

## Overview

This repository holds two kinds of AI assets:

- **Prompts** (`prompts/`) - copy-paste prompt templates that guide a model through a specific analytical or educational task using a proven framework.
- **Skills** (`skills/`) - reusable [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that a coding agent or assistant loads to change how it works on a task.

## Prompts

### 1. Academic Paper Analysis (Feynman Technique)
**Location:** `prompts/understand-academic-paper/`

Analyzes academic papers using the Feynman Technique to break down complex research into understandable concepts. The prompt guides through:
- Core concept identification in simple language
- Teaching methodology as if explaining to a 12-year-old
- Gap identification in understanding
- Simplification and reorganization
- Critical analysis and technical deep-dive

The folder includes a `template.txt`, a `generate_prompts.py` helper that builds per-paper prompts from `urls.txt`, and worked examples with their results (e.g. why language models hallucinate, model collapse, parallel thinking, the nature of the firm).

### 2. Stock Portfolio Analysis (Aswath Damodaran Framework)
**Location:** `prompts/stock-portfolio-damodaran/`

Analyzes stocks and portfolios using Professor Aswath Damodaran's valuation principles and investment philosophy. Covers:
- Intrinsic value calculations
- Risk assessment and cost of capital
- Story vs. numbers reconciliation
- Market pricing analysis
- Margin of safety evaluation

Only `template.txt` is tracked. Personal portfolio inputs and results stay local (see `.gitignore`).

## Skills

### writing
**Location:** `skills/writing/`

Rewrites prose so people will actually read it. Applies Orwell's six rules and strips the common LLM tells: passive voice, dead metaphors, -ly padding, and machine-made sentence shapes. Use it for essays, emails, reports, blog posts, and other general prose.

### poster-making
**Location:** `skills/poster-making/`

Turns a repository into a printable two-sided A4 poster: a self-contained HTML file, two 300 DPI PNGs, and a print-ready PDF. It mines the README, the docs, and an optional slide deck for content, then builds a dense panel infographic with inlined fonts, a QR code it proves scans, and a chart drawn as inline SVG rather than screenshotted. Use it for conference posters, handouts, and one-pagers.

To use a skill with Claude Code or the Claude apps, place its folder where your agent loads skills (for Claude Code, under `.claude/skills/`).

## Using a prompt

1. Open the prompt template folder.
2. Copy `template.txt`.
3. Replace the placeholders (URLs, stock symbols, and so on) with your inputs.
4. Paste the filled prompt into Claude, Perplexity, or your assistant of choice.
5. Save the output next to the template if you want to keep it.

## Prompt design principles

Each prompt template follows these principles:

1. **Structured framework** - uses an established method (Feynman Technique, Damodaran's valuation approach).
2. **Step-by-step guidance** - breaks a hard analysis into manageable steps.
3. **Multiple perspectives** - looks at the subject from more than one angle.
4. **Clarity focus** - values understanding over surface coverage.
5. **Actionable output** - produces practical, usable results.

## Contributing

Suggestions for new prompts or skills are welcome. A new prompt should:
- Solve a specific need.
- Use a proven framework or method.
- Include clear instructions and expected output.
- Provide an example.

## License

MIT-0 License. These assets are shared for educational and analytical use with no restrictions. Adapt, modify, and distribute them for any purpose.

## Notes

- These prompts work best with current Claude models but adapt to other LLMs.
- Result quality depends on the model and its training data.
- **Use at your own risk.** These assets are for educational purposes only.
- Verify critical analysis, especially for investment decisions.
- Models can hallucinate or give wrong answers. Consult qualified professionals for financial, academic, or other specialized advice.
