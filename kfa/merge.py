import re
from typing import List, Dict

def merge_chunks(outputs: List[Dict]):
    # Very simple merge: concatenate with section headers; a real version would dedupe tags and craft bridges
    lines = ["# Keynote KFA Report\n"]
    for item in outputs:
        lines.append(f"\n## Scene {item['id']}\n")
        lines.append("> " + item['text'].replace("\n", "\n> ") + "\n\n")
        lines.append(item['kfa'] + "\n")
    return "".join(lines)
