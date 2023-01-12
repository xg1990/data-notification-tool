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


def build_service(service_config: Dict, service_name: str, service_type: str):
    class_name = service_config.get("class_name", service_name)
    print(class_name)

    if service_type == "source":
        base_cls = BaseSource 
    elif service_type == "destination":
        base_cls = BaseDestination
    elif service_type == "formatter":
        base_cls = BaseFormatter
    elif service_type == "filterer":
        base_cls == BaseFilterer
    else:
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
    def __init__(self, filename: str) -> None:
        self._config = EnvYAML(filename, strict=False)
        self.sources: Dict[str, BaseSource] = {}
        self.destinations: Dict[str, BaseDestination] = {}
        self.formatters: Dict[str, BaseFormatter] = {}
        self.filterers: Dict[str, BaseFilterer] = {}

        self.message_groups: Dict[str, Dict] = self._config["message_groups"]
        self.jobs: Dict[str, Dict] = self._config["jobs"]
        self._set_up_services()

    def _set_up_services(self):
        if "custom_modules" in self._config:
            for _path in self._config["custom_modules"]:
                sys.path.append(_path)    

        for source_name, source_config in self._config["sources"].items():
            self.sources[source_name] = build_service(source_config, source_name, service_type="source")

        for dest_name, dest_config in self._config["destinations"].items():
            self.destinations[dest_name] = build_service(dest_config, dest_name, service_type="destination")

        # Load filterers & formatters
        raw_cfg = self._config.export()
        fmt_ls = get_components("formatter", raw_cfg)
        flt_ls = get_components("filterer", raw_cfg)
        for fmt in fmt_ls:
            self.formatters[fmt] = build_service({}, fmt, "formatter")

        print(fmt_ls)
        print(flt_ls)
        print(pydoc.locate('formatter.TimeStringFormatter'))
        print(pydoc.locate('TimeStringFormatter'))



    def get_services_from_group(
        self, 
        group_name: str, 
        **kwargs
    ) -> List[Tuple[BaseDestination, Dict]]:
        group: List[Any] = self._config["message_groups"][group_name]
        return [
            (self.destinations[item["dest"]], dict_drop_key(item, "service"))
            for item in group
        ]

    def validate(self) -> bool:
        assert "sources" in self._config
        assert "destinations" in self._config
        assert "message_groups" in self._config
        assert "jobs" in self._config
        return True
