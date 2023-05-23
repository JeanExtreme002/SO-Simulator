from abc import ABC, abstractmethod
from typing import Optional
from process import Process

import random


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int]):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

        self.__translator_salt = random.randint(1, 10 ** 6)
        self.__real_memory_table = [None for i in range(ram_memory_size // page_size)]

    def _translate_to_virtual_memory_address(self, real_memory_address: int) -> str:
        """
        Traduz o endereço de memória real para um endereço de memória virtual.
        """
        return hex(real_memory_address * self.__translator_salt)

    def _translate_to_real_memory_address(self, virtual_memory_address: str) -> int:
        """
        Traduz o endereço de memória virtual para um endereço de memória real.
        """
        result = int(virtual_memory_address, base = 16) / self.__translator_salt

        if int(result) != result or int(result) >= len(self.__real_memory_table):
            raise ValueError("Invalid memory address.")
        return int(result)

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
    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :returns: Retorna o endereço da página em hexadecimal.
        """
        pass

    @abstractmethod
    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass