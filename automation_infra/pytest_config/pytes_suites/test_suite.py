import unittest

import allure
import pytest
from automation_infra.support_utils import FileUtil as f
from automation_infra.report.AutomationReport import Report
from locust_files.infra import locust_constants as const
rep = Report()


@allure.feature("Automation infra")
class TestClass:
    @pytest.fixture(autouse=True, scope="session")
    def set_up(self):
        print("Automation infra general preparation start")
        from pathlib import Path
        home = str(Path.home())
        print(home)
        f.createLocalFileOrDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
        f.cleanupDir(f"{const.locust_files_dir}/{const.locust_statistic_dir}")
        rep.createReportsDir()
        rep.cleanUpReportFiles()
        print("Automation infra general preparation completed")




