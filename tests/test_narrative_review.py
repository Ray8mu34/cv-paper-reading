"""Workflow contracts; these tests do not grade the quality of an explanation."""
import json

import pytest
from bs4 import BeautifulSoup

from astro_xray.reader_review import pending_reader_review, validate_reader_review
from astro_xray.report import build_html, render_markdown, render_notes, validate_analysis
from test_pipeline import run


@pytest.fixture
def narrative(ready):
    ready['schema_version'] = '1.2'
    ready['reader'] = dict(
        overview='A teaching derivation links a measured light curve to lens alignment.',
        throughline='PRIVATE_THREAD: The light curve measures changing magnification. '
                    'Alignment sets the magnification formula; evaluating it predicts the curve. '
                    'Its limiting behavior checks the calculation, under the point-source assumptions.',
        connections=[dict(section_id=s['id'], needs='An alignment measurement needs an interpretation.',
                          adds='Connect the alignment, magnification and observation under stated assumptions.')
                     for s in ready['sections']],
        roadmap=[dict(section='§1', title='Teaching source', argument='Defines the analytic problem',
                      focus='The magnification expression', source_id='local', page=1)],
        focus=[dict(section_id='derivation', question='How does alignment determine magnification?',
                    why='Connects the measurable quantity to the formula.')])
    return ready


def save_review(data, workspace, *, md_only=False):
    record = pending_reader_review(data, workspace, md_only=md_only)
    # Synthetic structural fixture, not a real independent reader verdict.
    record.update(reviewer='self', test_mode='author-reconstruction', verdict='pass',
                  retelling='Synthetic self-check fixture: alignment sets the magnification; '
                            'the formula predicts a curve and limits constrain the interpretation.',
                  rationale='Synthetic review record used only to exercise binding and gap checks.')
    path = workspace/'validation/reader-review.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(record), encoding='utf-8')
    return record, path


def build(data, workspace, *, md_only=False):
    analysis = workspace/'analysis.json'
    analysis.write_text(json.dumps(data), encoding='utf-8')
    result = run('build_report.py', '--analysis', analysis, *(['--md-only'] if md_only else []))
    assert result.returncode == 0, result.stderr
    return analysis


def test_new_draft_contains_the_actual_planning_fields(tmp_path):
    result = run('new_analysis.py', 'local.pdf', '--out', tmp_path)
    assert result.returncode == 0, result.stderr
    draft = json.loads((tmp_path/'analysis.json').read_text(encoding='utf-8'))
    assert draft['schema_version'] == '1.3'
    assert draft['reader']['throughline'] == ''
    assert draft['reader']['connections'] == []
    validate_analysis(draft)
    assert run('build_report.py', '--analysis', tmp_path/'analysis.json').returncode != 0


@pytest.mark.parametrize('mutation', ['missing-thread', 'missing-link', 'wrong-order', 'appendix-link'])
def test_deep_delivery_needs_an_ordered_complete_connection_plan(narrative, mutation):
    if mutation == 'missing-thread':
        narrative['reader']['throughline'] = ' '
    elif mutation == 'missing-link':
        narrative['reader']['connections'].pop()
    elif mutation == 'wrong-order':
        narrative['reader']['connections'].reverse()
    else:
        narrative['sections'][0]['audience'] = 'appendix'
    with pytest.raises(ValueError):
        validate_analysis(narrative, publish=True)


def test_quick_only_needs_the_supported_overview(narrative):
    narrative['mode'] = 'quick'
    narrative['coverage'].update(level='abstract', teaching_only=False)
    narrative['reader'].update(throughline='', connections=[], roadmap=[])
    validate_analysis(narrative, publish=True)


def test_roadmap_follows_prose_and_plan_stays_internal(narrative):
    narrative['sections'][-1]['audience'] = 'appendix'
    narrative['reader']['connections'].pop()
    md = render_markdown(narrative)
    assert md.index('## 原文结构导览') > md.index('<!-- astro-appendix-end -->')
    assert 'PRIVATE_THREAD' not in md and 'PRIVATE_THREAD' in render_notes(narrative)
    page = BeautifulSoup(build_html(md, analysis=narrative), 'html.parser')
    section = page.find(id='section-method')
    assert section and section.find_parent('details') is None
    assert page.find(id='section-review').find_parent('details')
    headings = [h.get_text() for h in page.find_all('h2')]
    assert headings.index('原文结构导览') > headings.index('review')


def test_prepare_never_auto_passes_or_overwrites(narrative, tmp_path):
    analysis = build(narrative, tmp_path)
    assert run('prepare_reader_review.py', '--analysis', analysis).returncode == 0
    review_path = tmp_path/'validation/reader-review.json'
    original = review_path.read_bytes()
    assert json.loads(original)['verdict'] == 'pending'
    assert run('prepare_reader_review.py', '--analysis', analysis).returncode != 0
    assert review_path.read_bytes() == original
    with pytest.raises(ValueError, match='pending'):
        validate_reader_review(narrative, tmp_path)


@pytest.mark.parametrize('mutation', ['open-mainline', 'empty-retelling', 'guided', 'false-independence', 'unexplained-repair'])
def test_manual_review_cannot_pass_with_incomplete_evidence(narrative, tmp_path, mutation):
    build(narrative, tmp_path)
    record, path = save_review(narrative, tmp_path)
    if mutation == 'empty-retelling':
        record['retelling'] = ' '
    elif mutation == 'guided':
        record.update(reviewer='independent', test_mode='guided-check')
    elif mutation == 'false-independence':
        record.update(reviewer='self', test_mode='unprompted-reader')
    else:
        record['findings'] = [dict(location='derivation', missing_connection='No relation to the observation',
                                  impact='mainline', status='open', repair='')]
        if mutation == 'unexplained-repair':
            record['findings'][0]['status'] = 'resolved'
    path.write_text(json.dumps(record), encoding='utf-8')
    with pytest.raises(ValueError):
        validate_reader_review(narrative, tmp_path)


def test_record_pass_then_prose_and_html_changes_invalidate_it(narrative, tmp_path):
    analysis = build(narrative, tmp_path)
    save_review(narrative, tmp_path)
    command = ('--analysis', analysis, '--require-artifacts', '--require-reader-review')
    assert run('validate_skill.py', *command).returncode == 0
    html = tmp_path/'report.html'
    html.write_text(html.read_text(encoding='utf-8') + '\n<!-- changed -->', encoding='utf-8')
    with pytest.raises(ValueError, match='stale'):
        validate_reader_review(narrative, tmp_path)
    build(narrative, tmp_path)
    narrative['sections'][0]['markdown'] += '\nA newly explained dependency.'
    build(narrative, tmp_path)
    assert run('validate_skill.py', *command).returncode != 0


def test_markdown_only_checks_review_and_linked_resources(narrative, tmp_path):
    figure = tmp_path/'figure.png'
    figure.write_bytes(b'synthetic fixture asset, not a scientific figure')
    narrative['visuals'] = [dict(id='figure', kind='image', section_id='method', placement='include',
                                question='What changes?', why='Locate the change', alternative='Text',
                                caption='Synthetic fixture', basis='schematic', image='figure.png')]
    narrative['sections'][1]['markdown'] += '\n\n<!-- astro-visual:figure -->'
    analysis = build(narrative, tmp_path, md_only=True)
    save_review(narrative, tmp_path, md_only=True)
    assert not (tmp_path/'report.html').exists()
    result = run('validate_skill.py', '--analysis', analysis, '--require-artifacts', '--require-reader-review', '--md-only')
    assert result.returncode == 0, result.stderr
    figure.write_bytes(b'changed fixture asset')
    with pytest.raises(ValueError, match='stale'):
        validate_reader_review(narrative, tmp_path, md_only=True)


def test_local_gaps_can_remain_and_mainline_repairs_are_recorded(narrative, tmp_path):
    build(narrative, tmp_path)
    record, path = save_review(narrative, tmp_path)
    record['findings'] = [
        dict(location='method', missing_connection='Previously omitted the measured input',
             impact='mainline', status='resolved', repair='Synthetic fixture: added the input relation and rechecked the path.'),
        dict(location='review', missing_connection='An optional implementation detail remains unspecified',
             impact='local', status='open', repair='')]
    path.write_text(json.dumps(record), encoding='utf-8')
    validate_reader_review(narrative, tmp_path)
