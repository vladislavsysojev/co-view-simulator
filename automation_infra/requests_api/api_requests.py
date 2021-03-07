import requests


class ApiRequests():
    pass


class RestApiRequests(ApiRequests):

    def post_req(self, host, url, headers=None, data=None):
        response = requests.post(str.format("{0}{1}", host, url), headers, data)
        # await response.json()
        return response.json()

    def post_req(self, host, url, headers=None, json=None):
        response = requests.post(str.format("{0}{1}", host, url), headers, json)
        # await response.json()
        return response.json()
