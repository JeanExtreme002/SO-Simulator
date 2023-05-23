from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple
from process import Process

import random


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int]):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

        self.__ram_memory_pages = ram_memory_size // page_size

        self._page_usage_table = dict()  # Dicionário com relação {<ID Processo> : Quantidade de páginas}
        self.__translator_salt = random.randint(1, 10 ** 6)

        self.__real_memory_table: List[Tuple[Optional[Process], Any]] = [  # Lista de (Processo, valor)
            (None, None) for i in range(self.__ram_memory_pages)
        ]

    @property
    def ram_memory_pages(self) -> int:
        return self.__ram_memory_pages

    @property
    def ram_memory_size(self) -> int:
        return self.__ram_memory_size

    @property
    def page_size(self) -> int:
        return self.__page_size

    @property
    def page_per_process(self) -> int:
        return self.__page_per_process

    def _reserve(self, process: Process, real_memory_address: int, value: Optional[Any] = None) -> str:
        """
        Reserva uma página para o dado processo.

        :returns: Retorna o endereço da página em hexadecimal.
        """
        reserved_pages = self._page_usage_table.get(process.id, 0)

        if reserved_pages >= self.page_per_process:
            raise OverflowError("Max amount of memory page exceeded.")

        self._page_usage_table[process.id] = self._page_usage_table.get(process.id, 0) + 1
        self.__real_memory_table[real_memory_address] = (process, value)

        return self._translate_to_virtual_memory_address(real_memory_address)

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

    def _use(self, process: Process, real_memory_address: int, new_value: Optional[Any] = None) -> Any:
        """
        Utiliza uma página de memória em uma dado endereço, retornando
        o seu valor atual e escrevendo algo no espaço.
        """
        registered_process, value = self.__real_memory_table[real_memory_address]

        if process.id != registered_process:
            raise ValueError("Illegal access for this memory page.")

        if new_value is not None:
            self.__real_memory_table[real_memory_address] = (process, new_value)

        return value

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