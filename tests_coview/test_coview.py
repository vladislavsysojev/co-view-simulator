import time
import unittest

import pytest
import allure

from automation_infra.pytest_config.pytes_suites.test_suite import TestClass
from automation_infra.support_utils.SupportUtils import runCmd
from automation_infra.test_validators.LocustValidator import validateLocustResults
from locust_files.create_device_group import CreateDeviceId, CreteDeviceIdUser
from locust_files.infra.locust_runners import LocustRunner


class TestCoViewSuite:
    @pytest.fixture(autouse=True)
    def prep(self):
        # kub_sup.getKubernetesPods()
        # kub_sup.exec_commands_on_pod("nginx-dep-5c5477cb4-92zwr")
        print("prep")

    @allure.title("Device group component test")
    @pytest.mark.parametrize("workers_num, user_num, spawn_rate, time_to_run", [(100, 10000, 85, "5m")])
    def test_create_device_group(self, workers_num, user_num, spawn_rate, time_to_run):
        print("test1")
        # runCmd("cd /Users/vladislavsysojev/Documents/Texel/Git/co-view-simulator/automation_infra/firebase_client"
        #        "/sample-client/;npm install;npm build .;npm start")
        runner = LocustRunner()
        # runner.run_with_docker("locust_files/create_device_group.py", 10, "https://coview-automation.texel.live",
        #                        3000, 25, "4m")
        # time.sleep(10)
        # runner.invoker_run([CreteDeviceIdUser], "https://coview-automation.texel.live", user_num, spawn_rate, time_to_run)
        # runner.cmd_run_distributed_mode_locally("locust_files/create_device_group.py", "https://coview-automation.texel.live",
        #                                         user_num,
        #                                         spawn_rate, time_to_run, "99")

        runner.run_distributed_mode_on_gcp("https://coview-automation.texel.live", workers_num, user_num, spawn_rate,
                                           time_to_run, "create_device_group.py")
        # runner.cmd_run("locust_files/create_device_group.py", "http://34.105.159.99:8080", user_num,
        #                spawn_rate, time_to_run, "99")

        validateLocustResults(runner.unique_statistics_name)

        # @allure.title("Co-view end to end load test")
        # @pytest.mark.parametrize("user_num, spawn_rate, time_to_run", [(10000, 10, "2m"), (10000, 20, "2m"),
        #                                                                (10000, 30, "2m"), (10000, 56, "2m")])
        # def create_device_group(self, user_num, spawn_rate, time_to_run):
        #     print("test1")
        #     runner = LocustRunner()
        #     time.sleep(10)
        #     runner.cmd_run_distributed_mode_locally("locust_files/coview_end_to_end_load_test.py", "https://reqres.in", user_num,
        #                                             spawn_rate, time_to_run, "99")
        #
        #     validateLocustResults(runner.unique_statistics_name)
