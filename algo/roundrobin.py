from typing import List
from algo import Algo
from backend.BackendServer import BackendServer


class RoundRobin(Algo):
    def __init__(self, servers_: List[BackendServer]):
        self.idx = 0
        self.servers_ = servers_

    @property
    def servers(self) -> List[BackendServer]:
        return self.servers_

    def next(self) -> BackendServer | None:
        try:
            filtered_servers: List[BackendServer] = list(filter(lambda s: s.isAlive, self.servers))
            self.idx += 1
            self.idx %= len(filtered_servers)
            choosen_server = filtered_servers[self.idx]
            return choosen_server
        except:
            return None
