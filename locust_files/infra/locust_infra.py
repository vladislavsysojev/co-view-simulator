import time

from locust import HttpUser, clients, events, User


def create_conn():
    print("Connecting to MySQL")


def firebase_request():
    print("execute to Firebase")


class LocustTestUser(HttpUser):
    abstract = True

    def __init__(self, parent):
        super(LocustTestUser, self).__init__(parent)
        # self.client = MyClient()
        self.client = CustomMixedClient(self.host, self.environment.events.request_success, self.client.request_failure)
        # self.client._locust_environment = self.environment


class CustomMixedClient(clients.HttpSession):
    def __init__(self, base_url, request_success, request_failure, *args, **kwargs):
        super(CustomMixedClient, self).__init__(base_url, request_success, request_failure, *args, **kwargs)

    _locust_environment = None

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                firebase_request()
                # print('Result ----------->' + str(res.fetchone()))
                events.request_success.fire(request_type="firebase",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000), response_length=0)
            except Exception as e:
                events.request_failure.fire(request_type="firebase",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000),
                                            exception=e)

                print('error {}'.format(e))

        return wrapper
