import abc
from typing import List
from backend.BackendServer import BackendServer


class Algo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next(self, servers: List[BackendServer]) -> BackendServer:
        """Load in the data set"""
        raise NotImplementedError


def select_server(algo: Algo, servers: List[BackendServer]) -> BackendServer:
    return algo.next(servers)
