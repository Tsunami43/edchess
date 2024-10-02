import json


class Proxy:
    def __init__(self):
        with open("proxy.json", "r") as file:
            self.data = json.load(file)

    @property
    def url(self):
        return f"{self.data['scheme']}://{self.data['hostname']}:{self.data['port']}"
