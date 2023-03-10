import os
import sys
from envyaml import EnvYAML
from typing import Any, Dict, List, Tuple, Type
from dnt.core.base import (
    BaseSource, 
    BaseDestination, 
    BaseFormatter,
    BaseFilterer
)
from dnt.core.utils import dict_drop_key, get_components
import pydoc


# The services and related base classes
SERVICE_TYPE_DIC = {
    "source": BaseSource,
    "destination": BaseDestination,
    "formatter": BaseFormatter,
    "filterer": BaseFilterer,
}


def build_service(service_config: Dict, service_name: str, service_type: str):
    """
    Load a service class by name and type and generate an instance.

    Args:
        service_config (dict): The config of the service
        service_name (str): The name of the service
        service_type (str): The type of the service (should be one 'source', 'destination', 
        'formatter', 'filterer')

    Returns:
        An instance of the service
    """
    class_name = service_config.get("class_name", service_name)

    try:
        base_cls = SERVICE_TYPE_DIC[service_type]
    except KeyError:
        raise ValueError(f"Unknown service type: {service_type}")

    _cls: Type[base_cls] = pydoc.locate(class_name)
    if _cls is None:
        _cls: Type[base_cls] = pydoc.locate(f"dnt.services.{service_type}.{class_name}")
        if _cls is None:
            raise ValueError(f"The {service_type} Class `{class_name}` is not found")

    if service_type in ("source", "destination"):
        return _cls(name=service_name, **dict_drop_key(service_config, "class_name"))
    else:
        return _cls()

class Config:
    """
    A class to load the config file and store the configs for different services.
    """
    def __init__(self, filename: str) -> None:
        """
        Initialize with a config file path.

        Args:
            filename (str): The path of the config file

        Returns:
            None
        """
        self._filename = filename
        self._config = EnvYAML(filename, strict=False)
        self.sources: Dict[str, BaseSource] = {}
        self.destinations: Dict[str, BaseDestination] = {}
        self.formatters: Dict[str, BaseFormatter] = {}
        self.filterers: Dict[str, BaseFilterer] = {}

        self.message_groups: Dict[str, Dict] = self._config["message_groups"]
        self.jobs: Dict[str, Dict] = self._config["jobs"]
        self._set_up_services()

    def _set_up_services(self) -> None:
        """
        Load services (including sources, destinations, formatters & filterers) according to the config file.

        Args:
            None
        
        Returns:
            None
        """
        if "custom_modules" in self._config:
            for _path in self._config["custom_modules"]:
                abs_path = os.path.abspath(
                    os.path.join(
                        os.path.dirname(self._filename),
                        _path
                    )
                )
                sys.path.append(abs_path)    

        # Load sources & destinations
        for source_name, source_config in self._config["sources"].items():
            self.sources[source_name] = build_service(source_config, source_name, service_type="source")

        for dest_name, dest_config in self._config["destinations"].items():
            self.destinations[dest_name] = build_service(dest_config, dest_name, service_type="destination")

        # Load formatters & filterers
        raw_cfg = self._config.export()
        fmt_ls = get_components(raw_cfg, "formatter")
        
        for fmt in fmt_ls:
            self.formatters[fmt] = build_service({}, fmt, "formatter")

        flt_ls = get_components(raw_cfg, "filterer")
        for flt in flt_ls:
            self.filterers[flt] = build_service({}, flt, "filterer")

    def validate(self) -> bool:
        """
        Validate the config file (if mandatory keys exist).

        Args:
            None

        Returns:
            True if the config file is valid
        """
        assert "sources" in self._config
        assert "destinations" in self._config
        assert "message_groups" in self._config
        assert "jobs" in self._config
        return True
