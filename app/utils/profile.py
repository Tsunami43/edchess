import json
from fake_useragent import UserAgent


class Profile:
    def __init__(self, name: str):
        with open("profiles.json", "r") as file:
            data = json.load(file)
        self.__data = data.get(name, None)
        self.__proxy = self.__data.get("proxy", None) if self.__data else None
        self.__user_agent = self.__data.get("user_agent", None) if self.__data else None

    @property
    def user_agent(self):
        return self.__user_agent if self.__user_agent else UserAgent().random

    @property
    def proxy_data(self):
        return self.__proxy

    @property
    def proxy_url(self):
        proxy_data = self.proxy_data
        if proxy_data:
            return f"{proxy_data['scheme']}://{proxy_data['hostname']}:{proxy_data['port']}"
        return None
