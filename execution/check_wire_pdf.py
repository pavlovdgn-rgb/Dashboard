"""Verify that the wire smoke-test PDF contains the entire report, not a clipped modal."""
import json
import re
from pathlib import Path
from pypdf import PdfReader

pdf_path = Path('.tmp/wire/demo-report.pdf')
reader = PdfReader(pdf_path)
text = '\n'.join(page.extract_text() for page in reader.pages)
missing = [f'{number:03d}' for number in range(1, 21) if not re.search(rf'\b{number:03d}\b', text)]
compact = re.sub(r'\s+', '', text)
assert not missing, f'Participants missing from printed report: {missing}'
assert 'Неполные' in compact, 'Last scenario column is clipped'
assert 'Сформироватьотчёт' not in compact, 'Interactive form leaked into the print surface'
result = {'pages': len(reader.pages), 'participants': 20, 'lastColumnPresent': True, 'errors': []}
Path('.tmp/wire/pdf-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
