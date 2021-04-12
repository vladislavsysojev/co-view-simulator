import copy
import json
import uuid

from locust import task, TaskSet, constant, HttpUser, events
import locust_files.locust_templates as temp


class CreateDeviceId(TaskSet):

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
        access_token_data = copy.deepcopy(temp.access_token_data)
        access_token_data["userId"] = user_id
        access_token_data["deviceId"] = device_id

        response = self.client.post("/v1/auth/generateEngagementToken", name="Generate access token",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=access_token_data)
        if response.status_code == 200:
            access_token = json.loads(response.text)["auth"]["accessToken"]
            self.response = self.client.post("/v1/users/connect", name="Connect",
                                             headers={"Content-Type": "application/json",
                                                      "Authorization": access_token, "USER_ID": user_id,
                                                      "DEVICE_ID": device_id}, json=login_data)
            if self.response.status_code == 200:
                self.response = self.client.post(f"/v1/users/{user_id}/deviceGroups",
                                                 name="Create device group host sdk",
                                                 headers={"Content-Type": "application/json",
                                                          "Authorization": access_token, "USER_ID": user_id,
                                                          "DEVICE_ID": device_id}, json=create_device_id)

    @task
    def keep_alive(self):
        pass


class CreteDeviceIdUser(HttpUser):
    tasks = [CreateDeviceId]
    wait_time = constant(1)
    weight = 1
