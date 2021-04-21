#!/usr/bin/env python
import pytest
import allure

from automation_infra.support_utils import FileUtil as f
from automation_infra.test_validators.LocustValidator import validateLocustResults
from locust_files.infra.locust_runners import LocustRunner
from automation_infra.report.AutomationReport import Report
from locust_files.infra import locust_constants as const

rep = Report()


@pytest.fixture(autouse=True, scope="session")
def set_up():
    print("Automation infra general preparation start")
    from pathlib import Path
    home = str(Path.home())
    print(home)
    f.createLocalFileOrDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
    f.cleanupDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
    rep.createReportsDir()
    rep.cleanUpReportFiles()
    print("Automation infra general preparation completed")


@allure.title("Device group component test")
@pytest.mark.usefixtures("params")
def test_create_device_group(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       "create_device_group.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("Co-view end to end load test")
@pytest.mark.usefixtures("params")
def test_end_to_end_co_view(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       "coview_end_to_end_load_test.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("Create Enter Pin code test")
@pytest.mark.usefixtures("params")
def test_enter_pin_code(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       "create_enter_pin_code.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("Create Pin code test")
@pytest.mark.usefixtures("params")
def test_create_pin_code(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"],
                                       params["time_to_run"], "create_pin_code.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("health test")
@pytest.mark.usefixtures("params")
def test_health(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"], "health.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("create room")
@pytest.mark.usefixtures("params")
def test_create_room(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       "create_room.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)
