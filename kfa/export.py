import csv, pathlib

def export_markdown(md_text: str, path: str):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(md_text, encoding='utf-8')

def export_csv(outputs, path: str):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['chunk_id','tags','diagnosis_1line'])
        for o in outputs:
            # naive extraction: first line of [DIAGNOSIS]
            diag_line = ''
            for line in o['kfa'].splitlines():
                if line.strip().startswith('[DIAGNOSIS]'):
                    diag_line = line.strip()
                    break
            w.writerow([o['id'], '', diag_line])
