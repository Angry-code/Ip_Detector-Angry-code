import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("YANDEX_DISK_TOKEN")


def get_ip():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)

    return response.json()


def get_info():
    ip_address = get_ip()["ip"]
    url_geo = f"https://ipinfo.io/{ip_address}/geo"
    response = requests.get(url_geo)

    return response


class YD:
    def __init__(self, token):
        self.token: str = token
        self.headers = {"Authorization": f"OAuth {self.token}"}
        self.base_url = "https://cloud-api.yandex.net"

    def create_folder(self, path):
        response = requests.put(
            f"{self.base_url}/v1/disk/resources",
            headers=self.headers,
            params={"path": path},
        )
        return 200 <= response.status_code < 300

    def upload_file_by_url(self, path_disk):
        file_name = get_info().json()["city"]
        params = {"path": f"{path_disk}/{file_name}.txt"}
        response = requests.get(
            f"{self.base_url}/v1/disk/resources/upload",
            headers=self.headers,
            params=params,
        )

        upload_link = response.json()["href"]
        requests.put(upload_link, get_info().text)

        return


yd = YD(TOKEN)
get_ip()
get_info()
yd.create_folder("IP-address")
yd.upload_file_by_url("IP-address")
