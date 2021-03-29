import json
import random
import uuid

from locust import task, TaskSet, constant, HttpUser, events

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


class CreateDeviceId(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    def on_start(self):
        # user_id = "23d23ff32" + str(random.randint(1, 100000000))
        # device_id = "h783hd" + str(random.randint(1, 100000000))
        user_id = str(uuid.uuid4())
        device_id = str(uuid.uuid4())
        create_device_id = {
            "deviceId": device_id,
        }

        login_data = {
            "userId": user_id,
            "device": {
                "id": device_id,
                "name": "TV APP",
                "platform": "ANDROID",
                "capabilities": {
                    "MEDIA_SYNC": "READ"
                }
            },
            "clientProtocols": [
                "FIRESTORE"
            ]
        }
        # with self.client.post("/v1/users/connect", json=login_data,
        #                       headers={"Content-Type": "application/json"}, name="Connect", catch_response=True) as response:
        #     if response.status_code != 200:
        #         print(response.status_code)
        #         response.failure(
        #             "User with id: " + self.user_id + " Got unexpected response: " + str(response.status_code) +
        #             " Error: " + str(response.text))

        self.response = self.client.post("/v1/users/connect", name="Connect",
                                         headers={"Content-Type": "application/json"},
                                         json=login_data)
        if self.response.status_code == 200:
            self.response = self.client.post(f"/v1/users/{user_id}/deviceGroups",
                                             name="Create device group host sdk",
                                             headers={"Content-Type": "application/json"}, json=create_device_id)


    # def on_request_failure(request_type, name, response_time, exception):
    #     global_stats.log_error(request_type, name, exception)
    @task
    def keep_alive(self):
        pass


class CreteDeviceIdUser(HttpUser):
    tasks = [CreateDeviceId]
    wait_time = constant(1)
    weight = 1
