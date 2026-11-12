"""Bind a manual comprehension review to delivered files; never score prose."""
from __future__ import annotations

import hashlib
from pathlib import Path

import jsonschema

from .report import ROOT, read_json, render_markdown, safe_artifact


def report_fingerprints(data, workspace, *, md_only=False):
    workspace = Path(workspace)
    md_path = safe_artifact(workspace, data['artifacts']['markdown'])
    if md_path.read_text(encoding='utf-8-sig') != render_markdown(data):
        raise ValueError('Build the current report before preparing or checking a reader review')
    kinds = ('markdown',) if md_only else ('markdown', 'html')
    fingerprints = {kind: hashlib.sha256(safe_artifact(workspace, data['artifacts'][kind]).read_bytes()).hexdigest()
                    for kind in kinds}
    resources = {}
    for visual in data.get('visuals', []):
        if visual['placement'] != 'include':
            continue
        for key in ('image', 'fragment', 'styles', 'script', 'data'):
            if visual.get(key):
                relative = visual[key]
                resources[relative] = hashlib.sha256(safe_artifact(workspace, relative).read_bytes()).hexdigest()
    if resources:
        fingerprints['resources'] = resources
    return fingerprints


def pending_reader_review(data, workspace, *, md_only=False):
    return dict(schema_version='1.0', artifacts=report_fingerprints(data, workspace, md_only=md_only),
                reviewer='unrecorded', test_mode='unrecorded', retelling='', findings=[],
                verdict='pending', rationale='')


def validate_reader_review(data, workspace, *, md_only=False, root=ROOT):
    review_path = safe_artifact(workspace, 'validation/reader-review.json')
    if not review_path.is_file():
        raise ValueError('Missing manual reader review: run scripts/prepare_reader_review.py after building')
    review = read_json(review_path)
    schema = read_json(Path(root) / 'schemas/reader-review.schema.json')
    jsonschema.Draft202012Validator(schema).validate(review)
    if review['artifacts'] != report_fingerprints(data, workspace, md_only=md_only):
        raise ValueError('Reader review is stale or covers different artifacts; review the current delivery')
    if review['verdict'] != 'pass' or not review['retelling'].strip() or not review['rationale'].strip():
        raise ValueError('Manual reader review is pending or requires revision; record the actual retelling and judgment')
    expected_mode = {'self': 'author-reconstruction', 'independent': 'unprompted-reader', 'user': 'unprompted-reader'}
    if review['test_mode'] != expected_mode.get(review['reviewer']):
        raise ValueError('Record self reconstruction or an unprompted reader pass; a guided check is supplementary')
    for finding in review['findings']:
        if finding['impact'] == 'mainline' and finding['status'] == 'open':
            raise ValueError('Unresolved mainline comprehension gap: ' + finding['location'])
        if finding['status'] == 'resolved' and not finding['repair'].strip():
            raise ValueError('A resolved finding needs the actual repair and recheck')
    return review
