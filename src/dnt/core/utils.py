from typing import Dict, List, Union, Generator


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

def lvl_to_num(level: Union[float, int, str]) -> Union[float, int]:
    """
    Convert notification level to number if needed.

    Args:
        level (float/int/str): level of the notification

    Returns:
        The notification level as a number
    """
    if isinstance(level, (float, int)):
        return level
    else:
        try:
            return _name_to_lvl[level.upper()]
        except KeyError:
            raise ValueError(f"Unknown level: {level}")

def dict_drop_key(dic: Dict, key: str) -> Dict:
    """
    Generate a dictionary without a specific key.

    Args:
        dic (dict): The dict to parse
        key (str): The key to remove
    
    Returns:
        A dict without the key
    """
    return {k: v for k, v in dic.items() if k != key}

def get_all_key_values(source_dict: Dict, key: str) -> Generator:
    """
    Get all the values from a dict with a specific same key.
    
    Args:
        source_dict (dict): The dict to get values from
        key (str): The key to search for

    Returns:
        A generator with all the values that belong to the key
    """
    if hasattr(source_dict, "items"): 
        for k, v in source_dict.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in get_all_key_values(v, key):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in get_all_key_values(d, key):
                        yield result

def get_components(config_dict: Dict, comp_name: str) -> List[str]:
    """
    Get a deduplicated list of specific components from the config.
    
    Args:
        config_dict (dict): The config dict to get components from
        comp_name (str): The component name to get
        
    Returns:
        A deduplicated list of the specified components
    """
    res_ls = []
    for i in get_all_key_values(config_dict, comp_name):
        if isinstance(i, list):
            res_ls.extend(i)
        else:
            res_ls.append(i)
    return list(set(res_ls))
