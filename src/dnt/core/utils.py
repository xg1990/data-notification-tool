from typing import Dict


def dict_drop_key(input: Dict, key: str) -> Dict:
    return {k: v for k, v in input.items() if k != key}
