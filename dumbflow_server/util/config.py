import os
from typing import Any, Dict, MutableMapping

import toml


def load_conf(path: str) -> MutableMapping[str, Any]:
    """Load (toml) config from file
    
    Arguments:
        path {str} -- conf file path
    
    Returns:
        Dict -- dict containing conf data
    """
    return toml.load(path)


def load_conf_from_env(var_name: str) -> MutableMapping[str, Any]:
    """Load conf from a file whose path resisdes in an environment variable.

    Arguments:
        var_name {str} -- environment variable name
    
    Returns:
        Dict -- dict containing conf data
    """
    return load_conf(os.environ[var_name])
