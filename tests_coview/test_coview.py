#!/usr/bin/env python
import pytest
import allure

from automation_infra.support_utils import FileUtil as f
from automation_infra.test_validators.LocustValidator import validateLocustResults
from locust_files.infra.locust_runners import LocustRunner
from automation_infra.report.AutomationReport import Report
from locust_files.infra import locust_constants as const
from automation_infra.support_utils import SupportUtils as sup
from automation_infra.support_utils.gcp_support import wait_cluster_status

rep = Report()


@pytest.fixture(autouse=True, scope="class")
@pytest.mark.usefixtures("params")
def set_up(params):
    print("Automation infra general preparation start")
    from pathlib import Path
    home = str(Path.home())
    print(home)
    f.createLocalFileOrDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
    f.cleanupDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
    rep.createReportsDir()
    rep.cleanUpReportFiles()
    sup.runCmd(const.gcloud_set_project_cmd)
    if not params["lcl"]:
        sup.runCmd(const.gcloud_cluster_delete)
        min_nodes_num = int(int(params["workers_num"])/6)
        max_nodes_num = min_nodes_num + 3
        sup.runCmd(str.format(const.create_cluster_cmg, const.init_cluster_name(), const.gcp_zone, str(min_nodes_num),
                              str(max_nodes_num)))
    else:
        const.init_cluster_name(params["lcl"])
    sup.runCmd(const.upgrade_cluster_cmd)
    wait_cluster_status("running", 5, 30)
    print("Automation infra general preparation completed")
    yield
    print("Automation infra general cleanup start")
    if not params["lcl"]:
        sup.runCmd(const.gcloud_cluster_delete)
    print("Automation infra general cleanup completed")


@allure.title("Device group component test")
@pytest.mark.usefixtures("params")
def test_create_device_group(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "create_device_group.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("Co-view end to end load test")
@pytest.mark.usefixtures("params")
def test_end_to_end_co_view(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "coview_end_to_end_load_test.py")
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
                                       params["time_to_run"], params["app_key"], "create_pin_code.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("health test")
@pytest.mark.usefixtures("params")
def test_health(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "health.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("create room")
@pytest.mark.usefixtures("params")
def test_create_room(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "create_room.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("monitoring test")
@pytest.mark.usefixtures("params")
def test_monitoring(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "coview_monitoring_load_test.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)


@allure.title("Co-view end to end load test with leave room")
def test_end_to_end_with_leave_room(params):
    runner = LocustRunner()
    runner.run_distributed_mode_on_gcp(params["url"], params["workers_num"],
                                       params["user_num"], params["spawn_rate"], params["time_to_run"],
                                       params["app_key"], "coview_end_to_end_with_leave_room_load_test.py")
    validateLocustResults(runner.unique_statistics_name, runner.unique_log_name)
