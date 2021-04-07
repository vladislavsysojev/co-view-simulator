import copy
import json
import random
import uuid

from locust import task, TaskSet, constant, HttpUser
import locust_files.locust_templates as temp


class CreatePin(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        user_id = str(uuid.uuid4())
        pin_data = temp.pin_data.copy()
        pin_data["payload"] = user_id
        access_token_data = copy.deepcopy(temp.access_token_data)
        access_token_data["userId"] = user_id
        response = self.client.post("/v1/auth/generateEngagementToken", name="Generate access token",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=access_token_data)
        if response.status_code == 200:
            access_token = json.loads(response.text)["auth"]["accessToken"]
            self.response = self.client.post("/v1/pin", name="Generate pin host sdk",
                                             headers={"Content-Type": "application/json",
                                                      "Authorization": access_token, "USER_ID": user_id},
                                             json=pin_data)

    @task
    def keep_alive(self):
        pass


class CretePinUser(HttpUser):
    tasks = [CreatePin]
    wait_time = constant(1)
    weight = 1
