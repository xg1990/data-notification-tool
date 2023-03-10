import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import pytest
from dnt.core.config import Config
from dnt.core.runner import Runner


def prep_data():
    """
    Prepare testing data into sqlite in memory.
    """
    conn = sqlite3.connect("test.db")
    df = pd.DataFrame(
        {
            "table_name": [
                "deparment_revenue",
                "department_info",
                "department_info_dev",
                "new_plan_2023",
            ],
            "details": [
                "All done",
                "Syntax error" ,
                "All done",
                "All done",
            ],
            "db": [
                "mysql",
                "mysql",
                "sqlserver",
                "sqlserver"
            ],
            "check_status": [
                "SUCCESS",
                "FAILED",
                "SUCCESS",
                "SUCCESS"
            ]
        }
    )
    df.to_sql(name="system_status", con=conn, if_exists="replace", index=False)


@pytest.mark.parametrize(
    "job_name, raise_error, expected_output",
    [
        (
            "test_single_dest", 
            False,
            (
                "Message from cls service:\nSubject: test_single_dest\n"
                "{'table_name': 'deparment_revenue', 'details': 'All done', 'db': 'mysql', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "{'table_name': 'department_info', 'details': 'Syntax error', 'db': 'mysql', 'check_status': 'FAILED', 'level': 'ERROR'}\n"
                "{'table_name': 'department_info_dev', 'details': 'All done', 'db': 'sqlserver', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "{'table_name': 'new_plan_2023', 'details': 'All done', 'db': 'sqlserver', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "\n\n"
            )
        ),
        (
            "blahblah", 
            True,
            None
        ),
        (
            "system_status_alert",
            False,
            (
                "Message from cls service:\nSubject: system_status_alert\n"
                "{'table_name': 'deparment_revenue', 'details': 'All done', 'db': 'mysql', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "{'table_name': 'department_info', 'details': 'Syntax error', 'db': 'mysql', 'check_status': 'FAILED', 'level': 'ERROR'}\n"
                "{'table_name': 'department_info_dev', 'details': 'All done', 'db': 'sqlserver', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "{'table_name': 'new_plan_2023', 'details': 'All done', 'db': 'sqlserver', 'check_status': 'SUCCESS', 'level': 'INFO'}\n"
                "\n\n"
                "Message from cls service:\nSubject: system_status_alert\n"
                "\n\n"
            )
        )
    ]
)
def test_runner_run_single_job(job_name, raise_error, expected_output, capfd):
    """
    Test Runner class
    """
    prep_data()

    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    runner = Runner(config)
    assert runner.config == config

    if raise_error:
        with pytest.raises(ValueError):
            runner.run_single_job(job_name=job_name)
    else:
        runner.run_single_job(job_name=job_name)
        out, err = capfd.readouterr()
        assert out == expected_output

def test_runner_run_all(capfd):
    prep_data()

    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    runner = Runner(config)

    runner.run_all()
    out, err = capfd.readouterr()
    assert "system_status_alert" in out
    assert "test_single_dest" in out
