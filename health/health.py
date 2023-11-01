from time import sleep
from threading import Thread
from typing import List
import requests


def get_server_heart_beat(server) -> bool:
    try:
        resp = requests.get(f"http://{server.host}:{server.port}/health")
        return resp.text == "up"
    except:
        return False


def update_heartbeat(server, delay) -> None:
    while True:
        server_heart_beat = get_server_heart_beat(server)
        server.update_health_status(server_heart_beat)
        sleep(delay)


def check_health(servers) -> List[Thread]:
    threads = []
    for s in servers:
        t = Thread(target=update_heartbeat, args=(s, 2))
        threads.append(t)
        t.start()
    return threads
