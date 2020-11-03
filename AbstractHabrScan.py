from abc import ABCMeta, abstractmethod
"""""
 в надежде, что habr API рано или поздно станет доступным
"""""


class AbstractHabrScan(metaclass=ABCMeta):
    @staticmethod
    def postRequest():
        pass
