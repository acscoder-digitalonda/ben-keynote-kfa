from .prompts import SYSTEM, CRITIQUE_USER

def critique_chunk(provider, model, snippet: str, temperature=0.2, max_output_tokens=1500):
    msg = [
        {"role":"system","content": SYSTEM},
        {"role":"user","content": CRITIQUE_USER.format(snippet=snippet)},
    ]
    out = provider.respond(msg, model=model, temperature=temperature, max_output_tokens=max_output_tokens)
    return out
