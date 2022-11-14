from dnt.core.runner import Runner


def test_runner(test_config):
    runner = Runner(test_config)
    runner.run_single_job('test_alert')