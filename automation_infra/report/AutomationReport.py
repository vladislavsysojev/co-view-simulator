import os
import subprocess
from automation_infra.support_utils import FileUtil as f

class Report:
    folder = "Reports"
    def cleanUpReportFiles(self):
        f.cleanupFilesFromLocalDir(self.folder)

    def createReportsDir(self):
        f.createLocalFileOrDir(self.folder)

    def generateReport(self):
        # report_path = f.getFullPath(self.folder)
        # cmd = str.format("cd {0}; allure generate {1}",report_path, report_path)
        # sysrun.runCmd(cmd)
        reports = os.getcwd() + '/Reports'
        # stores processed reports int html format in this location
        report_server = os.getcwd() + '/Reports'
        command_generate_allure_report = ['allure generate ' + reports + ' -o ' + report_server + ' --clean']
        subprocess.call(command_generate_allure_report, shell=True)