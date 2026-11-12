"""Schema 1.3 source-order guardrails; synthetic documentation, no paper claims."""
import copy
import json

import pytest
from astro_xray.report import render_markdown, render_notes, validate_analysis
from test_pipeline import run


@pytest.fixture
def source_order(ready):
    data = copy.deepcopy(ready)
    data['schema_version'] = '1.3'
    data['reader'] = dict(
        overview='This teaching fixture explains a task, a design choice and its experimental test.',
        argument_route='§1 introduces the problem; §2 sets out challenges and a method; §3 tests it; §4 states its scope.',
        organization='paper-order', departure_reason='',
        throughline='Following the paper: §1 asks the question; §2 connects its design to prior limitations; '
                    '§3 tests the specific claim; §4 states the relevant conditions.',
        roadmap=[
            dict(section=sec, title=title, argument=argument, focus='Teaching fixture', source_id='local', page=i)
            for i, (sec, title, argument) in enumerate([
                ('§1','Motivation','Explains why the study is needed'),
                ('§2','Method','Uses a new construction to address the challenge'),
                ('§3','Evaluation','Tests the specific claim'),
                ('§4','Discussion','Explains limitations')], start=1)
        ],
        focus=[],
        connections=[dict(section_id=s['id'], needs='The prior section defines the next question.',
                          adds='This section answers that question and motivates the next.')
                     for s in data['sections']]
    )
    for sec, source in zip(data['sections'], [
        ['§1'], ['§2'], ['§2'], ['§3'], ['§4'], []
    ]):
        sec['source_sections'] = source
    return data


def test_original_route_precedes_sections_and_detailed_map_follows(source_order):
    validate_analysis(source_order, publish=True)
    md = render_markdown(source_order)
    assert md.index('## 论文论证路线') < md.index('## background')
    assert md.index('## 原文结构导览') > md.index('## review')
    assert md.index('## method') < md.index('## evidence')
    assert 'Following the paper' not in md
    notes = render_notes(source_order)
    assert 'Following the paper' in notes
    assert 'paper-order' in notes
    assert '- method: §2' in notes


@pytest.mark.parametrize('mutation, error', [
    ('missing-map', 'source_sections'),
    ('wrong-label', 'Unknown original-paper chapter'),
    ('missing-chapter', 'must all be covered'),
    ('backwards', 'chapter order'),
    ('independent-too-early', 'Independent commentary'),
    ('non-review-extra', 'clearly separate review'),
    ('missing-route', 'argument route'),
    ('missing-policy', 'organization'),
])
def test_invalid_source_mapping_is_rejected(source_order, mutation, error):
    data = copy.deepcopy(source_order)
    sections = data['sections']
    if mutation == 'missing-map':
        del sections[0]['source_sections']
    elif mutation == 'wrong-label':
        sections[1]['source_sections'] = ['§10']
    elif mutation == 'missing-chapter':
        sections[4]['source_sections'] = ['§3']
    elif mutation == 'backwards':
        sections[1]['source_sections'], sections[3]['source_sections'] = (
            sections[3]['source_sections'], sections[1]['source_sections'])
    elif mutation == 'independent-too-early':
        sections[1]['source_sections'] = []
        sections[1]['role'] = 'review'
    elif mutation == 'non-review-extra':
        sections[0]['source_sections'] = []
    elif mutation == 'missing-route':
        data['reader']['argument_route'] = ''
    elif mutation == 'missing-policy':
        del data['reader']['organization']
    with pytest.raises(ValueError, match=error):
        validate_analysis(data, publish=True)


def test_nonstandard_order_must_be_explicit_and_source_complete(source_order):
    source_order['sections'][1]['source_sections'] = ['§3']
    source_order['sections'][3]['source_sections'] = ['§2']
    source_order['reader']['organization'] = 'restructured'
    with pytest.raises(ValueError, match='explain a concrete departure'):
        validate_analysis(source_order, publish=True)
    source_order['reader']['departure_reason'] = 'An explicitly requested reader adaptation reverses two chapters.'
    validate_analysis(source_order, publish=True)


def test_quick_can_stay_at_abstract_level_without_claiming_chapters(source_order):
    data = copy.deepcopy(source_order)
    data['mode'] = 'quick'
    data['coverage'].update(level='abstract', teaching_only=False)
    data['reader'].update(argument_route='', roadmap=[], throughline='', connections=[], organization='paper-order')
    for section in data['sections']:
        section.pop('source_sections')
    validate_analysis(data, publish=True)


def test_new_draft_uses_new_source_fidelity_fields(tmp_path):
    result = run('new_analysis.py','teaching-source.pdf','--out',tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads((tmp_path/'analysis.json').read_text(encoding='utf-8'))
    assert data['schema_version'] == '1.3'
    assert data['reader']['organization'] == 'paper-order'
    assert data['reader']['argument_route'] == ''
    validate_analysis(data)
    with pytest.raises(ValueError):
        validate_analysis(data, publish=True)


def test_v121_does_not_require_duplicate_internal_narrative_plan(source_order):
    # The original chapter map + source_sections remain required, but a second
    # per-section needs/adds ledger should not delay ordinary 1.3 reports.
    data = copy.deepcopy(source_order)
    data['reader'].pop('throughline', None)
    data['reader'].pop('connections', None)
    validate_analysis(data, publish=True)
    report = render_markdown(data)
    assert '论文论证路线' in report and '原文结构导览' in report
    data['sections'][1]['source_sections'] = ['§4']
    with pytest.raises(ValueError, match='chapter order'):
        validate_analysis(data, publish=True)
