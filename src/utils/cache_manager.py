import hashlib
import json

_prompt_cache = {}

def get_cache_key(data: dict) -> str:
    """
    Gera uma chave de cache MD5 a partir de um dicionário de dados.
    """
    return hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

def get_from_cache(cache_key: str):
    """
    Recupera um item do cache.
    """
    return _prompt_cache.get(cache_key)

def set_to_cache(cache_key: str, value):
    """
    Adiciona um item ao cache.
    """
    _prompt_cache[cache_key] = value