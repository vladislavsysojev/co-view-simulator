#!/usr/bin/env python
import pytest
from automation_infra.support_utils import FileUtil as f
from automation_infra.report.AutomationReport import Report

rep = Report()
@pytest.fixture(scope="session", autouse=True)
def general_prep(request):
    # prepare something ahead of all tests
    print("general setup")
    f.createLocalFileOrDir("locust_files/locust_statistic")
    f.cleanupDir("locust_files/locust_statistic")
    rep.createReportsDir()
    rep.cleanUpReportFiles()

def pytest_addoption(parser):
    parser.addoption("--w", "--workers_num", action="store", default=100)
    parser.addoption("--u", "--user_num", action="store", default=13000)
    parser.addoption("--s", "--spawn_rate", action="store", default=108)
    parser.addoption("--t", "--time_to_run", action="store", default="3m")

@pytest.fixture(scope="class")
def params(request):
    params = {'workers_num': request.config.getoption("--w", "--workers_num"),
              'user_num': request.config.getoption("--u", "--user_num"),
              "spawn_rate": request.config.getoption("--s", "--spawn_rate"),
              "time_to_run": request.config.getoption("--t", "--time_to_run")}
    return params

