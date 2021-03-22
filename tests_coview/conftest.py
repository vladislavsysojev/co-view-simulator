import pytest
from automation_infra.support_utils import FileUtil as f
from automation_infra.report.AutomationReport import Report

rep = Report()
@pytest.fixture(scope="session", autouse=True)
def general_prep(request):
    # prepare something ahead of all tests
    print("general setup")
    f.createLocalFileOrDir("locust_files/locust_statistic")
    f.createLocalFileOrDir("automation_logs")
    f.cleanupDir("locust_files/locust_statistic")


    f.cleanupFilesFromLocalDir("locust_statistic")
    rep.createReportsDir()
    rep.cleanUpReportFiles()