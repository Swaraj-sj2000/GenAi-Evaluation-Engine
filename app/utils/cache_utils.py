# app/utils/cache_utils.py
import hashlib

def make_cache_key(prompt: str, model_output: str) -> str:
    h = hashlib.md5(f"{prompt}:{model_output}".encode()).hexdigest()
    return f"score:{h}"