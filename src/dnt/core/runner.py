from typing import List, Optional
from dnt.core.utils import dict_drop_key
from dnt.core.base import BaseSource, BaseDestination, Message
from dnt.core.messages import MsgGrp
from dnt.core.config import Config

class Runner:
    """
    A runner class to orchestrate the whole process.
    """
    def __init__(self, config: Config) -> None:
        """
        Initialize the runner with a config object.

        Args:
            config (Config): The config of the runner

        Returns:
            None
        """
        self.config: Config = config

    def run_single_job(self, job_name: str) -> None:
        """
        Run a specific job according to the given name.

        Args:
            job_name (str): The name of the job to be run

        Returns:
            None
        """
        if job_name not in self.config.jobs:
            raise ValueError(f"The job `{job_name}` is not found")
        job_config = self.config.jobs[job_name]
        
        # Get messages
        results: List[Message] = []
        for _src_config in job_config["get_messages"]:
            source_name = _src_config["service"]
            if source_name not in self.config.sources:
                raise ValueError(f"The source `{source_name}` is not found")
            _data_service: BaseSource = self.config.sources[source_name]
            _result: List[Message] = _data_service.get_messages(
                **dict_drop_key(_src_config, "service")
            )
            results.extend(_result)

        # Send messages
        subject = job_name
        for msg_grp_nm in job_config["send_messages"]:
            if msg_grp_nm in self.config.message_groups:
                # send to a group
                msg_grp_cfg = self.config.message_groups[msg_grp_nm]
                msg_grp = MsgGrp(msg_grp_nm, msg_grp_cfg, self.config.formatters, self.config.filterers)
                delivery: List = msg_grp.deliver_msg(results, subject)
                
                for (dest_name, kwargs) in delivery:
                    if dest_name not in self.config.destinations:
                        raise ValueError(f"The destination `{dest_name}` is not found")
                    _dest_service: BaseDestination = self.config.destinations[dest_name]
                    _dest_service.emit(**kwargs)
                        
            elif msg_grp_nm in self.config.destinations:
                # send to a single destination
                if msg_grp_nm not in self.config.destinations:
                    raise ValueError(f"The destination `{msg_grp_nm}` is not found")
                _dest_service: BaseDestination = self.config.destinations[msg_grp_nm]
                _dest_service.emit(msg_ls=results, subject=subject)

            else:
                raise ValueError(f"The destination `{msg_grp_nm}` is not found, should either be a destination or a message group")

    def run_all(self, jobs: Optional[List]=None) -> None:
        """
        Run a list of jobs.

        Args:
            jobs (list): A list of job names to be run, if None, will run all jobs

        Returns:
            None
        """
        if jobs is None:
            for job_name in self.config.jobs:
                self.run_single_job(job_name)
        else:            
            for job_name in jobs:
                self.run_single_job(job_name)
                