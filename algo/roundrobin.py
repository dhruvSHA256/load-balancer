class RoundRobin:
    def __init__(self, servers_):
        self.idx = 0
        self.servers = servers_

    def next(self):
        try:
            filtered_servers = list(filter(lambda s: s.isAlive, self.servers))
            self.idx += 1
            self.idx %= len(filtered_servers)
            choosen_server = filtered_servers[self.idx]
            return choosen_server
        except:
            return None
