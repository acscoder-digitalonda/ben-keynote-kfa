from .prompts import SYSTEM, SCENEMAP_USER

def build_scene_map(provider, model, text: str):
    messages = [
        {"role":"system","content": SYSTEM},
        {"role":"user","content": SCENEMAP_USER + "\n\n" + text},
    ]
    return provider.respond(messages, model=model, temperature=0.2, max_output_tokens=2000)

def parse_scene_map(markdown: str):
    # Minimal parser: returns a list of scene labels (not spans)
    scenes = []
    for line in markdown.splitlines():
        if line.strip().startswith("-") and "[SCENES]" not in line:
            scenes.append(line.strip("- "))
    return scenes

def cut_by_scenes(text: str, scenes: list[str]):
    # Placeholder: fallback to a single chunk; your team can parse timestamps/markers later
    return [text]
