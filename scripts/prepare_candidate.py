"""Bundle exact-commit RC4 artifacts and evidence after all candidate checks pass."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'candidate')
    args = parser.parse_args()
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if args.commit != head:
        raise SystemExit('Requested candidate commit must equal the checked-out HEAD')
    subprocess.run(['git','diff','--exit-code','--','src','pyproject.toml','SKILL.md',
                    'capabilities.json','release-plan.json'],cwd=ROOT,check=True)
    plan = json.loads((ROOT/'release-plan.json').read_text())
    evidence = json.loads((ROOT/'reports/accuracy.json').read_text())
    if plan['tag'] != 'v0.1.0-rc.4' or not evidence.get('candidate_ready'):
        raise SystemExit('RC4 authorization and passing candidate evidence are required')
    if evidence.get('candidate_tag') != plan['tag']:
        raise SystemExit('Evidence is for a different candidate')
    dest = args.output.resolve()
    dest.mkdir(parents=True,exist_ok=True)
    if list(dest.iterdir()):
        raise SystemExit('Candidate output directory must be empty; existing artifacts preserved')
    wheels = list((ROOT/'dist').glob('*0.1.0rc4*.whl'))
    sources = list((ROOT/'dist').glob('*0.1.0rc4*.tar.gz'))
    if len(wheels) != 1 or len(sources) != 1:
        raise SystemExit('Expected exactly one RC4 wheel and source distribution')
    with zipfile.ZipFile(wheels[0]) as archive:
        assert 'arabic_calligraphy/grid.py' in archive.namelist()
        records = json.loads((ROOT/'src/arabic_calligraphy/data/fonts.json').read_text())
        assert sum(name.endswith('.ttf') for name in archive.namelist()) == len(records)
        assert all(any(name.endswith('/fonts/'+record['file']) for name in archive.namelist()) for record in records)
        for notice in ['OFL-and-notices.txt','Layla-OFL.txt','Layla-FONTLOG.txt','Layla-Authors','Layla-SOURCE.md']:
            assert any(name.endswith('/fonts/'+notice) for name in archive.namelist()), notice
    with tarfile.open(sources[0], 'r:gz') as archive:
        for suffix in ('/examples/square-kufic/allah-study.json',
                       '/examples/square-kufic/readme-rosette.json',
                       '/examples/gallery/readme-square-kufic.png',
                       '/scripts/generate_readme_hero.py'):
            assert any(name.endswith(suffix) for name in archive.getnames()), suffix
    for path in wheels+sources:
        shutil.copy2(path,dest/path.name)
    subprocess.run(['git','archive','--format=tar.gz','--prefix=arabic-calligraphy-skill/',
                    f'--output={dest / "arabic-calligraphy-skill-source.tar.gz"}',head],
                   cwd=ROOT,check=True)
    subprocess.run(['git','archive','--format=zip','--prefix=arabic-calligraphy-skill/',
                    f'--output={dest / "arabic-calligraphy-skill-rc4.zip"}',head],
                   cwd=ROOT,check=True)
    with zipfile.ZipFile(dest/'gallery.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((ROOT/'examples/gallery').iterdir()):
            if path.is_file():
                archive.write(path,path.name)
    with zipfile.ZipFile(dest/'square-kufic-study.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((ROOT/'examples/square-kufic').iterdir()):
            if path.is_file():
                archive.write(path,path.name)
    for name in ('accuracy.json','font-licenses.json'):
        shutil.copy2(ROOT/'reports'/name,dest/name)
    shutil.copy2(ROOT/'docs/releases/v0.1.0-rc.4.md',dest/'release-notes.md')
    manifest = dict(tag=plan['tag'],python_version=plan['python_version'],commit=head,
                    channel=plan['channel'],known_issues=plan['known_issues'],
                    tests_passed=evidence['passed'],stable_release_ready=False,
                    next_candidate_plan='docs/next-candidate.md')
    (dest/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    sums = ''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n'
                   for path in sorted(dest.iterdir()) if path.is_file())
    (dest/'SHA256SUMS').write_text(sums)
    print(f'Prepared {len(list(dest.iterdir()))} assets for {plan["tag"]} at {head}')


if __name__ == '__main__':
    main()
