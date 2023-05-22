from abc import ABC, abstractmethod
from typing import Optional
from process import Process


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int]):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

    @property
    def ram_memory_size(self) -> int:
        return self.__ram_memory_size

    @property
    def page_size(self) -> int:
        return self.__page_size

    @property
    def page_per_process(self) -> int:
        return self.__page_per_process

    @abstractmethod
    def reserve(self, process: Process) -> int:
        """
        Reserva uma página para o dado processo.

        :returns: Retorna o endereço da página.
        """
        pass

    @abstractmethod
    def use(self, process: Process, address: int):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass