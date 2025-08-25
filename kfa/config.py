import os, yaml
from dotenv import load_dotenv

def load_config(path: str = 'config.yaml'):
    load_dotenv()
    cfg = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f) or {}
    # Env overrides
    cfg.setdefault('models', {})
    g = os.getenv('KFA_GLOBAL_MODEL')
    s = os.getenv('KFA_STYLE_MODEL')
    if g: cfg['models']['global_model'] = g
    if s: cfg['models']['style_model'] = s
    
    # Set default models if not provided
    cfg['models'].setdefault('global_model', 'gpt-4')
    cfg['models'].setdefault('style_model', 'gpt-4o-mini')
    # Defaults
    cfg.setdefault('params', {'temperature': 0.2, 'max_output_tokens': 1500})
    cfg.setdefault('chunking', {'strategy': 'tokens','chunk_tokens':2000,'overlap_tokens':200,'prefer_sentence_boundary':True})
    cfg.setdefault('io', {'input_format':'auto','export_md':True,'export_docx':False,'export_csv':True})
    cfg.setdefault('provider', 'openai')
    return cfg
