from locust import task, TaskSet, constant

from automation_infra.requests_api.rest_api_request_data import login_data, create_device_id
from locust_files.infra.locust_infra import LocustTestUser


class CreateDeviceId(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    # def on_start(self):

    @task
    def index(self):
        self.response = self.client.post("/v1/users/connect", headers={"Content-Type": "application/json"},
                                         json=login_data)
        self.response = self.client.post("/v1/users/23d23ff32/deviceGroups",
                                         headers={"Content-Type": "application/json"}, json=create_device_id)


class CreteDeviceIdUser(LocustTestUser):
    tasks = [CreateDeviceId]
    wait_time = constant(2)
    weight = 1
