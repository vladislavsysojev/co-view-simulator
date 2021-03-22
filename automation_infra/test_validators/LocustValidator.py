import allure

from automation_infra.load_test_statistic import  locust_statistic as stat


def validateLocustResults(unique_statistics_name):
    # final_result = True
    fail_result_string = ""
    try:
        if not stat.get_test_statistic(unique_statistics_name):
            fail_result_string = "Test results file is empty"
    except FileNotFoundError:
        fail_result_string = "Test results doesn't exists in results dir"
    result_list = stat.get_fail_statistic(unique_statistics_name)
    for result in result_list:
        if type(result) == stat.FailStatistics:
            if result.error:
                fail_result_string += createFailResultString(result)
                # final_result = False
    attachTestResults(f"{unique_statistics_name}_stats.csv")
    if fail_result_string:
        failResult(fail_result_string)
    # return final_result


@allure.step("Fail Results")
def failResult(fail_message):
    raise AssertionError(fail_message)


def createFailResultString(result):
    return str.format("\n -------------- \n Fail on load Request: {0}  Request name: {1}  Fail occurrences: {2} "
                      "Error response: {3}",
                      result.method, result.name, result.occurrences, result.error)


def attachTestResults(file_name):
    allure.attach.file(f'locust_files/locust_statistic/{file_name}', attachment_type=allure.attachment_type.CSV)