#!/usr/bin/env python3

import logging
import re
from pathlib import Path
from typing import List
from urllib.parse import urlparse

# Configure logging with basicConfig
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    # Define log message format
    format="%(asctime)s,p%(process)s,{%(filename)s:%(lineno)d},%(levelname)s,%(message)s",
)

logger = logging.getLogger(__name__)


def _clean_folder_name(url: str) -> str:
    """Clean URL to create a valid folder name."""
    parsed = urlparse(url)

    # Get the path part and remove file extension
    path_part = parsed.path.strip('/')
    if path_part:
        # Remove file extensions like .pdf, .html
        path_part = re.sub(r'\.(pdf|html?|php)$', '', path_part)
        # Replace slashes and other problematic characters
        folder_name = re.sub(r'[/\\:*?"<>|]', '-', path_part)
        # Remove version suffixes like v2, v3
        folder_name = re.sub(r'v\d+$', '', folder_name)
        # Clean up multiple dashes
        folder_name = re.sub(r'-+', '-', folder_name).strip('-')
    else:
        # If no path, use domain name
        folder_name = parsed.netloc.replace('.', '-')

    # Ensure folder name is not empty and not too long
    if not folder_name or len(folder_name) < 3:
        folder_name = f"paper-{hash(url) % 10000}"

    # Limit length to avoid filesystem issues
    if len(folder_name) > 100:
        folder_name = folder_name[:100]

    return folder_name


def _read_template() -> str:
    """Read the template file."""
    template_path = Path(__file__).parent / "template.txt"

    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def _hydrate_template(
    template: str,
    url: str
) -> str:
    """Replace placeholder in template with actual URL."""
    return template.replace("INSERT_YOUR_PAPER_URL_HERE", url)


def _create_prompt_folder(
    base_dir: Path,
    url: str,
    template: str
) -> None:
    """Create folder and prompt file for a single URL."""
    folder_name = _clean_folder_name(url)
    folder_path = base_dir / folder_name

    # Create folder if it doesn't exist
    folder_path.mkdir(exist_ok=True)

    # Generate hydrated prompt
    hydrated_prompt = _hydrate_template(template, url)

    # Write prompt file
    prompt_file = folder_path / f"example-{folder_name}.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(hydrated_prompt)

    logger.info(f"Created prompt for {url} in folder: {folder_name}")


def _read_urls_from_file(file_path: Path) -> List[str]:
    """Read URLs from file, one per line."""
    if not file_path.exists():
        raise FileNotFoundError(f"URL file not found: {file_path}")

    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                urls.append(line)
                logger.debug(f"Read URL from line {line_num}: {line}")

    logger.info(f"Read {len(urls)} URLs from {file_path}")
    return urls


def generate_prompts_from_file(
    urls_file: str,
    base_directory: str = None
) -> None:
    """Generate prompt folders from a file containing URLs.

    Args:
        urls_file: Path to file containing URLs (one per line)
        base_directory: Base directory for creating folders (defaults to script directory)
    """
    if base_directory is None:
        base_directory = Path(__file__).parent
    else:
        base_directory = Path(base_directory)

    urls_file_path = Path(urls_file)

    # Read template
    template = _read_template()
    logger.info("Template loaded successfully")

    # Read URLs
    urls = _read_urls_from_file(urls_file_path)

    # Create prompt folders
    for url in urls:
        try:
            _create_prompt_folder(base_directory, url, template)
        except Exception as e:
            logger.error(f"Failed to create prompt for {url}: {e}")

    logger.info(f"Completed processing {len(urls)} URLs")


def main():
    """Main function for command line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate academic paper analysis prompts from a list of URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
    # Create prompts from urls.example.txt in current directory
    python generate_prompts.py urls.example.txt

    # Specify custom output directory
    python generate_prompts.py urls.example.txt --output-dir /path/to/output

URL file format:
    One URL per line, empty lines and lines starting with # are ignored.
"""
    )

    parser.add_argument(
        "urls_file",
        help="Path to file containing URLs (one per line)"
    )

    parser.add_argument(
        "--output-dir",
        help="Output directory for generated folders (default: script directory)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        generate_prompts_from_file(args.urls_file, args.output_dir)
        logger.info("Successfully generated all prompts")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise


if __name__ == "__main__":
    main()