import json
import random

from locust import task, TaskSet, constant, HttpUser


class CreateDeviceId(TaskSet):



    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    def on_start(self):
        enter_pin_data = {"pin": ""}
        pin_data = {"payload": "34f43f34", "expiration": 1610004200660}
        self.response = self.client.post("/v1/pin", name="Generate pin host sdk",
                                         headers={"Content-Type": "application/json"}, json=pin_data)
        pin = ""
        if self.response.status_code == 200:
            pin = json.loads(self.response.text)["pin"]
            enter_pin_data["pin"] = pin
            self.response = self.client.put("/v1/pin", name=f"Enter pin participant web app",
                                            headers={"Content-Type": "application/json"},
                                            data=json.dumps(enter_pin_data))

    @task
    def keep_alive(self):
        pass







class CreteEnterPinUser(HttpUser):
    tasks = [CreateDeviceId]
    wait_time = constant(1)
    weight = 1
