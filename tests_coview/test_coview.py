import time

import pytest
import allure

from automation_infra.pytest_config.pytes_suites.test_suite import TestClass
from automation_infra.test_validators.LocustValidator import validateLocustResults
from locust_files.infra.locust_runners import LocustRunner


class TestClass1():
    @pytest.fixture(autouse=True)
    def prep(self):
        # kub_sup.getKubernetesPods()
        # kub_sup.exec_commands_on_pod("nginx-dep-5c5477cb4-92zwr")
        print("prep")

    @allure.title("Device group component test")
    @pytest.mark.parametrize("user_num, spawn_rate, time_to_run", [(300, 100, "30s"), (300, 10, "30s")])
    def test_second(self, user_num, spawn_rate, time_to_run):
        print("test1")
        runner = LocustRunner()
        time.sleep(10)
        runner.cmd_run_distributed_mode_locally("locust_files/create_device_group.py", "https://reqres.in", user_num,
                                                spawn_rate, time_to_run, "99")
        # runner.cmd_run("locust_files/create_device_group.py", "https://reqres.in", user_num,
        #                                         spawn_rate, time_to_run, "99")

        validateLocustResults(runner.unique_statistics_name)
