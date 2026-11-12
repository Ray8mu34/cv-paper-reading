"""Create a pending manual review bound to the built report; never overwrite a review."""
import argparse
import json
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from astro_xray.reader_review import pending_reader_review
from astro_xray.report import read_json, safe_artifact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analysis', type=Path, required=True)
    parser.add_argument('--md-only', action='store_true', help='Review a Markdown-only delivery')
    args = parser.parse_args()
    data = read_json(args.analysis)
    review = pending_reader_review(data, args.analysis.parent, md_only=args.md_only)
    destination = safe_artifact(args.analysis.parent, 'validation/reader-review.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as stream:
        json.dump(review, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    print(f'Pending manual review: {destination}; read references/narrative-workflow.md before filling')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, jsonschema.ValidationError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
