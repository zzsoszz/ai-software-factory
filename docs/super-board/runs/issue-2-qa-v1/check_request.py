"""Run from the repository root; checks issue #2's submission artifacts."""
from pathlib import Path
import re
import yaml

template = Path('.github/ISSUE_TEMPLATE/request.md').read_text()
_, frontmatter, body = template.split('---', 2)
metadata = yaml.safe_load(frontmatter)
assert all(isinstance(metadata[key], str) and metadata[key].strip()
           for key in ('name', 'about', 'title'))
assert metadata['labels'] == 'feature'
print('AC1 PASS: valid YAML frontmatter, nonempty name/about/title, feature label')
for section in ('Problem', 'Context', 'Fix', 'Acceptance Criteria', 'Verification', 'Risk', 'Blocked by'):
    assert f'## {section}\n' in body, section
criteria = body.split('## Acceptance Criteria\n')[1].split('\n## ')[0]
assert len(re.findall(r'^- \[ \] ', criteria, re.M)) >= 2
assert body.rstrip().endswith('- None.')
verification = body.split('## Verification\n')[1].split('\n## ')[0]
assert all(prompt in verification for prompt in ('验证命令或步骤', '预期结果', '证据位置'))
print('AC2 PASS: standard sections, checkbox criteria, independent verification, None dependency')
readme = Path('README.md').read_text()
assert 'https://github.com/zzsoszz/ai-software-factory/issues/new?template=request.md' in readme
assert 'https://github.com/users/zzsoszz/projects/1' in readme
assert all(text in readme for text in ('feature', 'Verification', 'Ready', '- None.'))
for path in re.findall(r'\]\(([^):]+\.md)\)', readme):
    assert Path(path).is_file(), path
print('AC3 PASS: request URL, board URL, submission instructions and local Markdown links')
