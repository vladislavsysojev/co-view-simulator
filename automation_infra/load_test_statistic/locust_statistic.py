from automation_infra.support_utils import FileUtil as f, JsonDictUtil as json_util


def get_statistic(unique_statistics_name):
    # locust_data = LocustStatistic(**data)
    # requests_failures_data = RequestStatistic(**locust_data.requests, **locust_data.failures)
    # request_failure_data = RequestStatistic(**requests_failures_data.executed_requests, **requests_failures_data.fail_requests)
    return f.parseCsvToObjectList(FailStatistics, f"locust_statistic/{unique_statistics_name}_failures.csv")


class LocustStatistic:
    def __init__(self, requests, failures):
        self.requests = requests
        self.failures = failures


class RequestStatistic:
    def __init__(self, executed_requests, fail_requests):
        self.executed_requests = executed_requests
        self.fail_requests = fail_requests


class SingleRequestStatistic:
    def __init__(self, executed_request, fail_request):
        self.executed_request = executed_request
        self.fail_request = fail_request


class FailStatistics:
    def __init__(self, method, name, error, occurrences):
        self.method = method
        self.name = name
        self.error = error
        self.occurrences = occurrences


class TestStatistics:
    def __init__(self, type, name, count, fail_count, median_resp_time, average_resp_time, min_resp_time,
                 max_response_time, average_content_size, rps, f_rps, percent_50, percent_66, percent_75, percent_80,
                 percent_90, percent_95, percent_98, percent_99, percent_99_9, percent_99_99, percent_100):
        self.type = type
        self.name = name
        self.count = count
        self.fail_count = fail_count
        self.median_resp_time = median_resp_time
        self.average_resp_time = average_resp_time
        self.min_resp_time = min_resp_time
        self.max_response_time = max_response_time
        self.average_content_size = average_content_size
        self.rps = rps
        self.f_rps = f_rps
        self.percent_50 = percent_50
        self.percent_66 = percent_66
        self.percent_75 = percent_75
        self.percent_80 = percent_80
        self.percent_90 = percent_90
        self.percent_95 = percent_95
        self.percent_98 = percent_98
        self.percent_99 = percent_99
        self.percent_99_9 = percent_99_9
        self.percent_99_99 = percent_99_99
        self.percent_100 = percent_100


import csv
