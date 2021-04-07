import copy
import json
import random
import uuid

from locust import task, TaskSet, constant, HttpUser
import locust_files.locust_templates as temp


class CreateDeviceId(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        user_id = str(uuid.uuid4())
        pin_data = temp.pin_data.copy()
        pin_data["payload"] = user_id
        enter_pin_data = temp.enter_pin_data.copy()
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
            if self.response.status_code == 200:
                enter_pin_data["pin"] = json.loads(self.response.text)["pin"]
                self.response = self.client.put("/v1/pin", name=f"Enter pin participant web app",
                                                headers={"Content-Type": "application/json",
                                                         "Authorization": access_token, "USER_ID": user_id},
                                                data=json.dumps(enter_pin_data))

    @task
    def keep_alive(self):
        pass


class CreteEnterPinUser(HttpUser):
    tasks = [CreateDeviceId]
    wait_time = constant(1)
    weight = 1
