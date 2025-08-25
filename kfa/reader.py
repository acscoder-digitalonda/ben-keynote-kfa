from pathlib import Path
from typing import Literal

def read_input(path: str, input_format: Literal['auto','txt','md','docx','srt']='auto') -> str:
    p = Path(path)
    if input_format == 'auto':
        ext = (p.suffix or '').lower().lstrip('.')
        if ext in ('md','markdown'):
            input_format = 'md'
        elif ext in ('txt','text','log'):
            input_format = 'txt'
        elif ext in ('docx',):
            input_format = 'docx'
        elif ext in ('srt',):
            input_format = 'srt'
        else:
            input_format = 'txt'  # safe fallback
    if input_format in ('txt','md'):
        return p.read_text(encoding='utf-8', errors='ignore')
    if input_format == 'docx':
        try:
            from docx import Document
        except Exception as e:
            raise RuntimeError('python-docx is required for .docx ingestion') from e
        doc = Document(str(p))
        paras = []
        for para in doc.paragraphs:
            text = para.text.strip('\n')
            if text:
                paras.append(text)
        return "\n\n".join(paras).strip()
    if input_format == 'srt':
        # very simple SRT to text: skip numeric indices and timestamps
        lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
        out = []
        for line in lines:
            s = line.strip()
            if not s: 
                out.append('')  # keep paragraph breaks
                continue
            if s.isdigit():
                continue
            if '-->' in s:
                continue
            out.append(s)
        # collapse multiple blank lines
        text = "\n".join(out)
        while '\n\n\n' in text:
            text = text.replace('\n\n\n','\n\n')
        return text.strip()
    raise ValueError(f'Unsupported input_format: {input_format}')
