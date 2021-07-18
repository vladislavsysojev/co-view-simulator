#!/usr/bin/env python
import pytest
from locust import events

from automation_infra.report.AutomationReport import Report
from locust_files.infra.locust_constants import init_cluster_name

rep = Report()


def pytest_addoption(parser):
    parser.addoption("--w", "--workers_num", action="store", default=100)
    parser.addoption("--u", "--user_num", action="store", default=13000)
    parser.addoption("--s", "--spawn_rate", action="store", default=108)
    parser.addoption("--t", "--time_to_run", action="store", default="3m")
    parser.addoption("--ul", "--url", action="store", default="https://coview-automation.texel.live")
    parser.addoption("--lcl", action="store", default="")
    parser.addoption("--app_key", action="store", default="", required=True)

@events.init_command_line_parser.add_listener
def init_parser(parser):
    parser.add_argument("--wb-host", type=str, env_var="LOCUST_WB_HOST", default="ddd", help="It's working")




@pytest.fixture(scope="session")
def params(request):
    params = {'workers_num': request.config.getoption("--w", "--workers_num"),
              'user_num': request.config.getoption("--u", "--user_num"),
              "spawn_rate": request.config.getoption("--s", "--spawn_rate"),
              "time_to_run": request.config.getoption("--t", "--time_to_run"),
              "url": request.config.getoption("--ul", "--url"),
              "lcl": request.config.getoption("--lcl"),
              "app_key": request.config.getoption("--app_key")}
    return params

@pytest.fixture(scope="session", autouse=True)
def params_check(params):
    if params["lcl"]:
        init_cluster_name(name=params["lcl"])

