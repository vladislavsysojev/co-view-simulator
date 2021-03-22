import json
import random

from locust import task, TaskSet, constant, HttpUser


class CreateDeviceId(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    def on_start(self):
        user_id = "23d23ff32" + str(random.randint(1, 100000))
        device_id = "h783hd" + str(random.randint(1, 100000))
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

        self.response = self.client.post("/v1/users/connect", name="Connect",
                                         headers={"Content-Type": "application/json"},
                                         json=login_data)
        if self.response.status_code == 200:
            self.response = self.client.post(f"/v1/users/{user_id}/deviceGroups", name="Create Device Group",
                                             headers={"Content-Type": "application/json"}, json=create_device_id)

    @task
    def keep_alive(self):
        pass


class CreteDeviceIdUser(HttpUser):
    tasks = [CreateDeviceId]
    wait_time = constant(1)
    weight = 1
