from typing import List
from algo import Algo
from backend.BackendServer import BackendServer


class RoundRobin(Algo):
    def __init__(self):
        self.idx = 0

    def next(self, servers: List[BackendServer]) -> BackendServer | None:
        try:
            filtered_servers: List[BackendServer] = list(filter(lambda s: s.is_alive, servers))
            self.idx += 1
            self.idx %= len(filtered_servers)
            choosen_server = filtered_servers[self.idx]
            return choosen_server
        except Exception as err:
            print(f"Error {err}")
            return None
