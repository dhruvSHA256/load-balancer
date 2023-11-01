import abc
from typing import List
from backend.BackendServer import BackendServer


class Algo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next(self) -> BackendServer:
        """Load in the data set"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def servers(self) -> List[BackendServer]:
        """Abstract property for 'servers' attribute"""
        pass


def select_server(algo: Algo) -> BackendServer:
    return algo.next()
