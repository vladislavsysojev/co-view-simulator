

class RequestAdder():

    def __init__(self):
        self.request_dict = {}

    def addPost(self, host, url, headers=None, json=None):
        self.request_dict["post"] =[host, url, headers, json]

    def get_request_dict(self):
        return self.request_dict
