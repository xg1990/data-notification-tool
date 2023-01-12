from typing import Dict, List


CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

_lvl_to_name = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOTSET",
}

_name_to_lvl = {
    "CRITICAL": CRITICAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}

def lvl_to_num(level):
    """
    Convert level to number if needed.
    """
    if isinstance(level, (float, int)):
        return level
    else:
        try:
            return _name_to_lvl[level.upper()]
        except KeyError:
            raise ValueError(f"Unknown level: {level}")

def dict_drop_key(input: Dict, key: str) -> Dict:
    return {k: v for k, v in input.items() if k != key}

def get_all_key_values(key: str, source_dict: Dict):
    """
    Get all the values from a dict with a specific same key.
    """
    if hasattr(source_dict, "items"): 
        for k, v in source_dict.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in get_all_key_values(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in get_all_key_values(key, d):
                        yield result

def get_components(comp_name: str, config_dict: Dict) -> List[str]:
    """
    Get a deduplicated list of specific components from the config.
    """
    res_ls = []
    for i in get_all_key_values(comp_name, config_dict):
        if isinstance(i, list):
            res_ls.extend(i)
        else:
            res_ls.append(i)
    return list(set(res_ls))
