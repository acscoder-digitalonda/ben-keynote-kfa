import re

def naive_sentence_split(text: str):
    return re.split(r'(?<=[.!?])\s+', text)

def simple_token_estimate(s: str):
    return max(1, len(s) // 4)  # ~4 chars/token heuristic

def chunk_text(text: str, chunk_tokens=2000, overlap_tokens=200, prefer_sentence_boundary=True):
    sentences = naive_sentence_split(text)
    chunks, cur, cur_tokens = [], [], 0
    for sent in sentences:
        t = simple_token_estimate(sent)
        if cur_tokens + t > chunk_tokens:
            chunks.append(" ".join(cur).strip())
            # build overlap
            overlap = []
            ot = 0
            for s in reversed(cur):
                st = simple_token_estimate(s)
                if ot + st > overlap_tokens: break
                overlap.append(s)
                ot += st
            cur = list(reversed(overlap))
            cur_tokens = sum(simple_token_estimate(s) for s in cur)
        cur.append(sent)
        cur_tokens += t
    if cur:
        chunks.append(" ".join(cur).strip())
    return chunks
