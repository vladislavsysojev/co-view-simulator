import random

from locust import task, TaskSet, constant, HttpUser


class Health(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        self.response = self.client.get("/health", name="Health", headers={"Content-Type": "application/json"})

    @task
    def keep_alive(self):
        pass


class HealthUser(HttpUser):
    tasks = [Health]
    wait_time = constant(1)
    weight = 1
