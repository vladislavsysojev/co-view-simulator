#!/usr/bin/env python
import pytest
from automation_infra.report.AutomationReport import Report

rep = Report()


def pytest_addoption(parser):
    parser.addoption("--w", "--workers_num", action="store", default=100)
    parser.addoption("--u", "--user_num", action="store", default=13000)
    parser.addoption("--s", "--spawn_rate", action="store", default=108)
    parser.addoption("--t", "--time_to_run", action="store", default="3m")
    parser.addoption("--ul", "--url", action="store", default="https://coview-automation.texel.live")


@pytest.fixture(scope="class")
def params(request):
    params = {'workers_num': request.config.getoption("--w", "--workers_num"),
              'user_num': request.config.getoption("--u", "--user_num"),
              "spawn_rate": request.config.getoption("--s", "--spawn_rate"),
              "time_to_run": request.config.getoption("--t", "--time_to_run"),
              "url": request.config.getoption("--ul", "--url")}
    return params
