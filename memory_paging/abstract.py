from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from process import Process


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int] = None):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

        self.__ram_memory_pages = ram_memory_size // page_size

        self._page_usage_table = dict()  # {<ID Processo> : Quantidade de páginas}

        self._real_memory_table: List[Tuple[Optional[Process], Any, datetime, datetime]] = [  # Lista de (Processo, Valor, Tempo de Criação, Tempo do Último uso)
            (None, None, datetime.now(), datetime.now()) for i in range(self.__ram_memory_pages)
        ]
        self._virtual_memory_table: Dict[Tuple[int, int], Optional[int]] = dict()  # {(<ID Processo>, VMEM_ADDRESS) : RMEM_ADDRESS}
        self.__incremented_virutal_page_address = 0

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

    def _set_real_page(self, process: Optional[Process], real_memory_address: int):
        """
        Define um processo à uma página de memória real em uma dado endereço.
        """
        self._real_memory_table[real_memory_address] = (process, None, datetime.now(), datetime.now())
        self._use(process, real_memory_address)

    def _use(self, process: Process, real_memory_address: int, new_value: Optional[Any] = None) -> Any:
        """
        Utiliza uma página de memória em uma dado endereço, retornando
        o seu valor atual e escrevendo algo no espaço.
        """
        registered_process, value, created_at, last_used_at = self._real_memory_table[real_memory_address]

        if process.id != registered_process.id:
            raise ValueError("Illegal access for this memory page.")

        if new_value is not None: self._real_memory_table[real_memory_address] = (process, new_value, created_at, datetime.now())
        else: self._real_memory_table[real_memory_address] = (process, value, created_at, datetime.now())

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
            virtual_address = self.__incremented_virutal_page_address
            self.__incremented_virutal_page_address += 1

            self._virtual_memory_table[(process.id, virtual_address)] = None
            memory_addresses.append(virtual_address)

            memory -= self.page_size
        return memory_addresses

    def free_memory(self, process: Process):
        """
        Libera a memória utiliza por um processo.
        """
        for key, value in self._virtual_memory_table.items():
            if key[0] == process.id:
                self._virtual_memory_table.pop(key)
            self._set_real_page(None, value)

    def get_real_memory_table(self) -> List[Tuple[int, Optional[id], Optional[str]]]:
        """
        Retorna uma lista contendo tuplas no formato (Real Memory ID, Process ID, Virtual Memory ID).
        """
        table: List[Tuple[int, Optional[id], Optional[str]]] = list()

        for key, value in self._virtual_memory_table.items():
            if value is not None:
                table.append((value, key[0], hex(key[1])[2:]))

        return table

    @abstractmethod
    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass