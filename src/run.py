import argparse
import json

from src.config.settings import Settings
from src.providers.factory import build_provider
from src.scrapper import Cleaner, Extractor, Fetcher


def parse_fields(pairs: list[str]) -> dict[str, str]:
    """
    Turns CLI args like title="product title" into {"title": "product title"}.
    If no description given, falls back to using the field name as its own description.
    """
    fields = {}
    for pair in pairs:
        name, _, desc = pair.partition("=")
        fields[name] = desc or name
    return fields


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-powered structure-agnostic scraper")
    parser.add_argument("url")
    parser.add_argument("fields", nargs="+", help='field="description", e.g. title="product title"')
    parser.add_argument("--render", action="store_true", help="force headless browser rendering")
    args = parser.parse_args()

    # Fail fast, before touching network or the AI provider, if config is missing.
    Settings.validate()

    fetcher = Fetcher()
    cleaner = Cleaner()
    
    assert Settings.AI_PROVIDER
    assert Settings.ANTHROPIC_API_KEY
    provider = build_provider(Settings.AI_PROVIDER, Settings.ANTHROPIC_API_KEY)
    extractor = Extractor(provider)

    print(f"[fetch] {args.url}")
    html, rendered = fetcher.fetch(args.url, cleaner, force_render=args.render)
    print(f"[fetch] rendered={rendered} raw_len={len(html)}")

    cleaned = cleaner.clean_html(html)
    print(f"[clean] cleaned_len={len(cleaned)}")

    fields = parse_fields(args.fields)
    print("[extract] calling model...")
    result = extractor.extract(cleaned, fields)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
