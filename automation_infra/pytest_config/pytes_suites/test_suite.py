import unittest
from automation_infra.report.AutomationReport import Report
import allure
rep = Report()


# @allure.testcase("Automation infra")
class TestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Automation infra suite preparation start")

        print("Automation infra suite preparation completed")

    @classmethod
    def tearDownClass(cls):
        print("Automation infra suite teardown start")
        print("Automation infra suite teardown completed")


# if __name__ == "__main__":
#     unittest.main()
