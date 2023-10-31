class RoundRobin:
    def __init__(self, servers_):
        self.idx = 0
        self.servers = servers_

    def next(self):
        self.idx += 1
        self.idx %= len(self.servers)
        return self.servers[self.idx]


def select_server(algo):
    return algo.next()
