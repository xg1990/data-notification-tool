from typing import List, Optional

from dnt.core.config import Config
from dnt.core.service import DataServiceBase, Messages, MessageServiceBase
from dnt.core.utils import dict_drop_key


class Runner:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def run_single_job(self, job_name: Optional[str] = None) -> None:
        if job_name not in self.config.jobs:
            raise ValueError(f"The job `{job_name}` is not found")
        job_config = self.config.jobs[job_name]
        results: List[Messages] = []
        for _msg_config in job_config["get_messages"]:
            service_name = _msg_config["service"]
            if service_name not in self.config.services:
                raise ValueError(f"The service `{service_name}` is not found")
            _data_service: DataServiceBase = self.config.services[service_name]  # type: ignore
            _result: Messages = _data_service.get_messages(
                **dict_drop_key(_msg_config, "service")
            )
            results.append(_result)
        for action_item in job_config["actions"]:
            if "group" in action_item:
                # executing an action group
                for _msg_service, kwargs in self.config.get_services_from_group(  # type: ignore
                    action_item["group"]
                ):
                    kwargs = kwargs | dict_drop_key(action_item, "group")
                    _msg_service.send_messages(results, **kwargs)
            elif "service" in action_item:
                # executing an single action
                _msg_service: MessageServiceBase = self.config.services[action_item["service"]]  # type: ignore
                _msg_service.send_messages(
                    results, **dict_drop_key(action_item, "service")
                )

    def run_all(self, jobs: List):
        if jobs == []:
            for job_name in self.config.jobs:
                self.run_single_job(job_name)
        else:            
            for job_name in jobs:
                self.run_single_job(job_name)
