# Academic Paper Analysis Prompt Generator

> **Where the analyses live.** This folder holds the tooling only: the template, the
> generator and an example URL list. The ten paper analyses produced with it moved to
> [personal-knowledge-base/analyses/](https://github.com/aarora79/personal-knowledge-base/tree/main/analyses)
> on 2026-09-22, alongside the clipped sources and wiki articles for the same papers.
> The live reading queue moved there too, as `inbox.md`.

A Python tool that generates structured prompts for analyzing academic papers using the Feynman Technique. This tool reads a list of URLs and creates folders with hydrated analysis prompts for each paper.

## Prerequisites

- Python 3.11+
- uv package manager

## Installation

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# No additional dependencies needed - uses only Python standard library
```

## Usage

### Basic Usage

1. Create a file with URLs (one per line):
```
https://arxiv.org/pdf/2509.07604
https://www.nature.com/articles/s41586-024-07566-y.pdf
https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0335.1937.tb00002.x
```

2. Generate prompts:
```bash
uv run python generate_prompts.py urls.example.txt
```

### Advanced Usage

```bash
# Specify custom output directory
uv run python generate_prompts.py urls.example.txt --output-dir /path/to/output

# Enable debug logging
uv run python generate_prompts.py urls.example.txt --debug

# Show help
uv run python generate_prompts.py --help
```

### URL File Format

- One URL per line
- Empty lines are ignored
- Lines starting with `#` are treated as comments and ignored

Example `urls.example.txt`:
```
# AI/ML Papers
https://arxiv.org/pdf/2509.07604
https://arxiv.org/pdf/2509.08755

# Economics Papers
https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0335.1937.tb00002.x

# Nature Articles
https://www.nature.com/articles/s41586-024-07566-y.pdf
```

## Output Structure

For each URL, the tool creates:
- A folder named based on the URL path (cleaned for filesystem compatibility)
- A prompt file `example-{folder-name}.txt` containing the hydrated analysis template

Example output structure:
```
pdf-2509.07604/
├── example-pdf-2509.07604.txt

articles-s41586-024-07566-y/
├── example-articles-s41586-024-07566-y.txt

doi-10.1111-j.1468-0335.1937.tb00002.x/
├── example-doi-10.1111-j.1468-0335.1937.tb00002.x.txt
```

## Analysis Template Features

Each generated prompt includes:
- **Reading Time Estimation**: Estimates based on complexity and length
- **Feynman Technique Steps**:
  1. Core concept identification (simple language)
  2. Teaching explanation (12-year-old level)
  3. Gap identification (assumptions, unclear details)
  4. Simplification (summary, takeaways, analogies)
- **Critical Analysis**: Strengths, weaknesses, broader context
- **Technical Deep Dive**: Equations, results, validation methods

## Development Workflow

```bash
# Run all checks before committing
uv run ruff check --fix . && uv run ruff format . && uv run bandit -r . && uv run mypy generate_prompts.py
```

## Example Generated Prompt

Each prompt file contains a structured analysis template like:

```xml
<paper_analysis>
  <paper_url>https://arxiv.org/pdf/2509.07604</paper_url>

  <instructions>
    Please analyze this academic paper using the Feynman Technique...

    <reading_time_estimate>
      First, estimate the reading time for the original paper...
    </reading_time_estimate>

    <step_1_identify>
      Identify and explain the core concept...
    </step_1_identify>

    <!-- Additional structured sections -->
  </instructions>
</paper_analysis>
```

## Folder Naming Logic

The tool automatically generates clean folder names from URLs:
- Extracts the meaningful path component
- Removes file extensions (.pdf, .html)
- Replaces problematic characters with hyphens
- Removes version suffixes (v2, v3, etc.)
- Ensures valid filesystem names

Examples:
- `https://arxiv.org/pdf/2509.07604` → `pdf-2509.07604`
- `https://www.nature.com/articles/s41586-024-07566-y.pdf` → `articles-s41586-024-07566-y`
- `https://arxiv.org/html/2410.23242v2` → `html-2410.23242`

## Performance Notes

- Processing is fast for URL parsing and file generation
- Each operation typically completes in under a second
- No network requests are made during folder generation

## Troubleshooting

If you encounter issues:

1. **Permission errors**: Ensure write permissions in the output directory
2. **Invalid URLs**: Check that URLs are properly formatted in the input file
3. **Long folder names**: The tool automatically truncates names to 100 characters

## License

MIT License