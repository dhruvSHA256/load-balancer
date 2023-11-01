from time import sleep
import threading
import requests


def get_server_heart_beat(server):
    try:
        resp = requests.get(f"http://{server.host}:{server.port}/health")
        return resp.text == "up"
    except:
        return False


def update_heartbeat(server, delay):
    while True:
        server_heart_beat = get_server_heart_beat(server)
        server.update_health_status(server_heart_beat)
        sleep(delay)


def check_health(servers):
    threads = []
    for s in servers:
        t = threading.Thread(target=update_heartbeat, args=(s, 2))
        threads.append(t)
        t.start()
    return threads
