import argparse, pathlib, os
from .config import load_config
from .providers.openai_provider import OpenAIProvider
from .chunking import chunk_text
from .scenemap import build_scene_map, parse_scene_map, cut_by_scenes
from .critique import critique_chunk
from .export import export_markdown, export_csv
from .merge import merge_chunks

def run(input_path: str, cfg: dict):
    # Read input
    from .reader import read_input
    text = read_input(input_path, cfg['io'].get('input_format','auto'))

    provider = OpenAIProvider()

    # Global pass (optional)
    if cfg['chunking']['strategy'] == 'scene_map':
        sm_md = build_scene_map(provider, cfg['models']['global_model'], text)
        scenes = parse_scene_map(sm_md)
        chunks = cut_by_scenes(text, scenes)
    else:
        chunks = chunk_text(
            text,
            cfg['chunking']['chunk_tokens'],
            cfg['chunking']['overlap_tokens'],
            cfg['chunking']['prefer_sentence_boundary'],
        )

    # Style pass
    outputs = []
    for i, ch in enumerate(chunks):
        out = critique_chunk(
            provider,
            cfg['models']['style_model'],
            ch,
            temperature=cfg['params']['temperature'],
            max_output_tokens=cfg['params']['max_output_tokens']
        )
        outputs.append({'id': i, 'text': ch, 'kfa': out})

    # Merge & export
    md = merge_chunks(outputs)
    export_markdown(md, 'out/keynote_kfa.md')
    if cfg['io']['export_csv']:
        export_csv(outputs, 'out/keynote_kfa_notes.csv')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='Path to keynote text/markdown/docx (as text)')
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()
    cfg = load_config(args.config)
    run(args.input, cfg)
