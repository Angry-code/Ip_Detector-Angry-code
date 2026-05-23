import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("YANDEX_DISK_TOKEN")


def get_ip():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)

    return response.json()["ip"]


def get_info():
    ip_address = get_ip()
    url = f"https://ipinfo.io/{ip_address}/geo"

    return url


class YD:
    def __init__(self, token):
        self.token = token
        self.headers = {"Autorization": f"OAuth {self.token}"}
        self.base_url = "https://cloud-api.yandex.net"

    def create_folder(self, path):
        response = requests.put(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={"path": path},
        )
        return 200 <= response.status_code < 300

    def upload_file_by_url(self, file_url, path):
        file_name = requests.get(file_url).json()["city"]
        params = {"path": f"{path}/{file_name}"}
        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            headers=self.headers,
            params=params,
        )

        upload_link = response.json()["href"]

        with open(self.path_disk, "wb") as f:
            f.write(requests.get(file_url).json())

        with open(self.path_disk, "rb") as f1:
            requests.put(upload_link, f1)

        return


yd = YD(TOKEN)
get_ip()
yd.create_folder("IP-address")
yd.upload_file_by_url(file_url=get_info(), path="IP-address")
