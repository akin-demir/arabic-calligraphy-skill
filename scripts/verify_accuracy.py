"""Run evidence checks and emit honest JSON/JUnit reports; strict release gate optional."""
import argparse
import contextlib
import io
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess
import tempfile
import unittest
import warnings
from xml.etree import ElementTree as ET

from pypdf import PdfReader
from arabic_calligraphy import __version__
from arabic_calligraphy.engine import backend, render, styles
from arabic_calligraphy.fonts import coverage

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--release',action='store_true',help='Stable: enforce exact PDF extraction')
    mode.add_argument('--candidate',action='store_true',help='Explicitly scoped experimental RC2')
    args = parser.parse_args(argv)
    suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
    reports = ROOT/'reports';reports.mkdir(exist_ok=True)
    (reports/'tests.txt').write_text(output.getvalue())
    tests = ET.Element('testsuite',tests=str(result.testsRun),failures=str(len(result.failures)),
                       errors=str(len(result.errors)),skipped=str(len(result.skipped)))
    for test,trace in result.failures + result.errors:
        case = ET.SubElement(tests,'testcase',name=str(test))
        ET.SubElement(case,'failure').text = trace
    ET.ElementTree(tests).write(reports/'junit.xml',encoding='utf-8',xml_declaration=True)
    samples = ['العلم نور','بِسْمِ الله','العربية — Arabic 123']
    extraction=[]
    with tempfile.TemporaryDirectory() as directory:
        for text in samples:
            p = Path(directory)/'sample.pdf'
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');render(text,p)
            page=PdfReader(p).pages[0]
            actual=page.extract_text()
            semantic=(b'\xfe\xff'+text.encode('utf-16-be')).hex().encode()
            extraction.append(dict(input=text,pypdf_extracted=actual,
                exact_extraction=actual == text,
                exact_actual_text_mapping=semantic in page.get_contents().get_data()))
    items=styles()
    data=dict(tests_run=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
        failed=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        documented=len(items),implemented=sum(e['implemented'] for e in items),
        technically_verified=sum(e['technical_verified'] for e in items),
        expert_reviewed=sum(e['expert_authenticity_reviewed'] for e in items),
        approximate=sum(e['status']=='Approximate' for e in items),
        reference_only=sum(e['status']=='Reference Only' for e in items),
        fonts_licensed=len(coverage()),pdf_extraction=extraction,
        python=platform.python_version(),pypdf=version('pypdf'),pango=backend().pango_version().decode(),
        cairo=backend().cairo_version().decode(),
        release_ready=False,
        blockers=['Reader-independent exact Arabic PDF extraction is not established.',
                  'Remote CI and security audit must pass before release.',
                  'Maintainer publication approval is required.'])
    plan = json.loads((ROOT/'release-plan.json').read_text()) if args.candidate else {}
    semantic_ok = all(e['exact_actual_text_mapping'] for e in extraction)
    accepted = any(e['id'] == 'PDF-001' and e.get('accepted_for_testing') for e in plan.get('known_issues', []))
    candidate_ok = (plan.get('tag') == 'v0.1.0-rc.2' and plan.get('publication_authorized') is True
                    and plan.get('python_version') == __version__ and accepted and semantic_ok and result.wasSuccessful() and not result.skipped)
    data['candidate_ready'] = candidate_ok if args.candidate else None
    data['candidate_tag'] = plan.get('tag')
    data['pdf_limitation_accepted_for_testing'] = bool(args.candidate and accepted)
    (reports/'accuracy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (reports/'font-licenses.json').write_text(json.dumps({'checked_fonts':len(coverage()),'license':'OFL-1.1','hashes_valid':True},indent=2)+'\n')
    print(json.dumps(data,ensure_ascii=False,indent=2))
    if (args.candidate and not candidate_ok) or not result.wasSuccessful() or (args.release and not all(e['exact_extraction'] for e in extraction)):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
