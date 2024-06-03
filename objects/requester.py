import requests
import objects.saver as saver

class Requester():
    def __init__(self, url: str = "https://choplifter.donnarieix.fr") -> None:
        self.__url = url
        self.__save_manager = saver.Saver()
    
    # Geter / Seter
    
    def get_url(self) -> str:
        return self.__url
    def set_url(self, url: str) -> None:
        self.__url = url
    
    def get_save_path(self) -> str:
        return self.__save_manager.get_path()
    def set_save_path(self, path: str) -> None:
        self.__save_manager.set_path(path)
    
    # Méthodes
    
    def upload(self, data: dict) -> None:
        response = requests.post(self.__url, json=data)
        if response.json()["ID"] != "":
            data = self.__save_manager.load()
            data["ID"] = response.json()["ID"]
            self.__save_manager.save(data)
    
    def download(self, self_: bool, all: bool) -> dict:
        data = {
            "download": {}
        }
        if self_:
            data["download"]["self"] = self.__save_manager.load()["ID"]
        if all:
            data["download"]["all"] = True
        response = requests.post(self.__url, json=data)
        return response.json()