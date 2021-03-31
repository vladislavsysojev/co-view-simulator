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
        self.response = self.client.post("/v1/pin", name="Generate pin host sdk",
                                         headers={"Content-Type": "application/json", "USER_ID": user_id}, json=pin_data)

    @task
    def keep_alive(self):
        pass


class CretePinUser(HttpUser):
    tasks = [CreatePin]
    wait_time = constant(1)
    weight = 1
