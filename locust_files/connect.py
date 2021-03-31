import uuid

from locust import task, TaskSet, constant, HttpUser
import locust_files.locust_templates as temp


# from automation_infra.support_utils.ts_var import Ts_Var
# results = set()
#
#
# @events.init.add_listener
# def on_locust_init(environment, **kwargs):
#     print("Test started")
#
#
# @events.quitting.add_listener
# def on_locust_quit(environment, **kwargs):
#     for result in results:
#         print(result)
#     print("Test finished")
#
#
# @events.request_failure.add_listener
# def on_request_failure(request_type, name, response_time, exception, **kwargs):
#     events.request_failure.fire(request_type, name, response_time, exception, **kwargs)


class Connect(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        user_id = str(uuid.uuid4())
        device_id = str(uuid.uuid4())

        # with self.client.post("/v1/users/connect", json=login_data,
        #                       headers={"Content-Type": "application/json"}, name="Connect", catch_response=True) as response:
        #     if response.status_code != 200:
        #         print(response.status_code)
        #         response.failure(
        #             "User with id: " + self.user_id + " Got unexpected response: " + str(response.status_code) +
        #             " Error: " + str(response.text))
        login_data = temp.login_data.copy()
        login_data["userId"] = user_id
        login_data["device"]["id"] = device_id
        create_device_id = temp.create_device_id.copy()
        create_device_id["deviceId"] = device_id
        self.response = self.client.post("/v1/users/connect", name="Connect",
                                         headers={"Content-Type": "application/json", "USER_ID": user_id,
                                                  "DEVICE_ID": device_id}, json=login_data)

    @task
    def keep_alive(self):
        pass


class ConnectUser(HttpUser):
    tasks = [Connect]
    wait_time = constant(1)
    weight = 1
