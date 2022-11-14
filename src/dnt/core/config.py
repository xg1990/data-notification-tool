import sys
from typing import Any, Dict, List, Tuple

from envyaml import EnvYAML

from dnt.core.service import ServiceBase, build_service
from dnt.core.utils import dict_drop_key


class Config(object):
    def __init__(self, filename: str) -> None:
        self._config = EnvYAML(filename, strict=False)
        self.jobs: Dict[str, Dict] = self._config["jobs"]
        self.services: Dict[str, ServiceBase] = {}
        self._set_up_services()

    def _set_up_services(self):
        if "custom_modules" in self._config:
            for _path in self._config["custom_modules"]:
                sys.path.append(_path)

        for service_name, service_config in self._config["services"].items():
            self.services[service_name] = build_service(service_config, service_name)

    def get_services_from_group(
        self, group_name: str, **kwargs
    ) -> List[Tuple[ServiceBase, Dict]]:
        group: List[Any] = self._config["message_groups"][group_name]
        return [
            (self.services[item["service"]], dict_drop_key(item, "service"))
            for item in group
        ]

    def validate(self) -> bool:
        assert "message_groups" in self._config
        return True
