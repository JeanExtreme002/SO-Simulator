from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple
from process import Process

import datetime
import random


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int] = None):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

        self.__ram_memory_pages = ram_memory_size // page_size

        self._page_usage_table = dict()  # Dicionário com relação {<ID Processo> : Quantidade de páginas}
        self.__translator_salt = random.randint(1, 10 ** 6)

        self._real_memory_table: List[Tuple[Optional[Process], Any, str]] = [  # Lista de (Processo, Valor, Tempo do Último uso)
            (None, None, str()) for i in range(self.__ram_memory_pages)
        ]

    @property
    def name(self) -> str:
        return ""

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

        :return: Retorna o endereço da página em hexadecimal.
        """
        reserved_pages = self._page_usage_table.get(process.id, 0)

        if self.page_per_process is not None and reserved_pages >= self.page_per_process:
            raise OverflowError("Max amount of memory page exceeded.")

        self._page_usage_table[process.id] = self._page_usage_table.get(process.id, 0) + 1
        self._real_memory_table[real_memory_address] = (process, value, str())

        self._use(process, real_memory_address)
        return self._translate_to_virtual_memory_address(process, real_memory_address)

    def _translate_to_virtual_memory_address(self, process: Process, real_memory_address: int) -> str:
        """
        Traduz o endereço de memória real para um endereço de memória virtual.
        """
        return hex((real_memory_address + 1) * self.__translator_salt * (process.id + 1))

    def _translate_to_real_memory_address(self, process: Process, virtual_memory_address: str) -> int:
        """
        Traduz o endereço de memória virtual para um endereço de memória real.
        """
        result = (int(virtual_memory_address, base = 16) / self.__translator_salt) / (process.id + 1) - 1

        if int(result) != result or int(result) >= len(self._real_memory_table):
            raise ValueError("Invalid memory address.")
        return int(result)

    def _use(self, process: Process, real_memory_address: int, new_value: Optional[Any] = None) -> Any:
        """
        Utiliza uma página de memória em uma dado endereço, retornando
        o seu valor atual e escrevendo algo no espaço.
        """
        registered_process, value, last_use = self._real_memory_table[real_memory_address]

        if process.id != registered_process.id:
            raise ValueError("Illegal access for this memory page.")

        last_use = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")

        if new_value is not None: self._real_memory_table[real_memory_address] = (process, new_value, last_use)
        else: self._real_memory_table[real_memory_address] = (process, value, last_use)

        return value

    def alloc_memory(self, process: Process, memory: int) -> List[int]:
        """
        Aloca um espaço na memória para o processo.

        :return: Lista com os endereços das páginas utilizadas pelo processo, em hexadecimal.
        """
        memory_addresses = []

        if memory > self.page_per_process * self.page_size:
            raise OverflowError("Max amount of memory page exceeded.")

        while memory > 0:
            memory_addresses.append(self.reserve(process))
            memory -= self.page_size
        return memory_addresses

    def free_memory(self, process: Process) -> str:
        """
        Libera a memória utiliza por um processo.
        """
        for real_address in range(self.ram_memory_pages):
            if self._real_memory_table[real_address][0] == process:
                self._real_memory_table[real_address] = (None, None, str())

        if process.id in self._page_usage_table:
            self._page_usage_table.pop(process.id)

    def get_real_memory_table(self) -> List[Tuple[int, Optional[id], Optional[str]]]:
        """
        Retorna uma lista contendo tuplas no formato (Real Memory ID, Process ID, Virtual Memory ID).
        """
        table = []

        for real_address in range(self.ram_memory_pages):
            process = self._real_memory_table[real_address][0]
            last_use = self._real_memory_table[real_address][-1]

            if process is None: continue

            virtual_address = self._translate_to_virtual_memory_address(process, real_address)
            table.append((real_address, process.id, virtual_address, last_use))

        return table

    @abstractmethod
    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :return: Retorna o endereço da página em hexadecimal.
        """
        pass

    @abstractmethod
    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass