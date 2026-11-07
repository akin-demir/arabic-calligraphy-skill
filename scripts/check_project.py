"""Repository, Python syntax, whitespace, skill and capability lint checks."""
import ast
import json
from pathlib import Path
import re
import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    for path in ROOT.rglob('*'):
        if any((p.startswith('.') and p != '.github') or p in ('build','dist','__pycache__') for p in path.relative_to(ROOT).parts):
            continue
        if path.suffix in ('.py','.md','.toml','.yml','.json') and path.is_file():
            text = path.read_text()
            if not text.endswith('\n') or any(line.rstrip() != line for line in text.splitlines()):
                errors.append(f'{path.relative_to(ROOT)}: trailing whitespace or missing final newline')
            if path.suffix == '.py':
                ast.parse(text,filename=str(path))
            if path.suffix == '.json':
                json.loads(text)
            if path.suffix == '.yml':
                yaml.safe_load(text)
    tomllib.loads((ROOT/'pyproject.toml').read_text())
    front = yaml.safe_load((ROOT/'SKILL.md').read_text().split('---',2)[1])
    name = front['name']
    assert name == 'arabic-calligraphy-skill'
    assert len(name) <= 64 and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name)
    assert 0 < len(front['description']) <= 1024
    assert len(front.get('compatibility','')) <= 500
    assert all(isinstance(k,str) and isinstance(v,str) for k,v in front.get('metadata',{}).items())
    assert len((ROOT/'SKILL.md').read_text().splitlines()) < 500
    entries = json.loads((ROOT/'capabilities.json').read_text())['styles']
    assert len(entries) == len({e['id'] for e in entries}) == 20
    for entry in entries:
        assert (ROOT/'references/styles'/f"{entry['id']}.md").is_file()
        if entry['expert_authenticity_reviewed']:
            assert entry['review_evidence'] and (ROOT/entry['review_evidence']).is_file()
        if entry['status'] == 'Verified':
            assert entry['technical_verified'] and entry['expert_authenticity_reviewed']
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Python syntax, whitespace, JSON/YAML/TOML, skill metadata and registry lint passed')


if __name__ == '__main__':
    main()
