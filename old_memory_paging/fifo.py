from typing import Optional
from memory_paging import MemoryManager
from process import Process


class FIFOMemoryManager(MemoryManager):

    __count = 0

    @property
    def name(self) -> str:
        return "First In First Out (FIFO)"

    def __get_available_address(self) -> Optional[int]:
        """
        Retorna um endereço disponível na memória real, se houver.
        :return:
        """
        available_addresses = list(range(self.ram_memory_pages))

        for real_address, process_id, virtual_address, last_use in self.get_real_memory_table():
            available_addresses.remove(real_address)

        return available_addresses[0] if available_addresses else None

    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :return: Retorna o endereço da página em hexadecimal.
        """
        self.__count %= self.ram_memory_pages
        real_address = self.__count

        # Verifica se a página já está ocupada. Se sim, tenta obter uma página livre.
        if self._real_memory_table[self.__count][0] is not None:
            real_address = self.__get_available_address()

            # Se não houver, a página será sobrescrita.
            if real_address is None:
                real_address = self.__count
                self.__count += 1
        else:
            self.__count += 1

        return super()._reserve(process, real_address)

    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        super()._use(process, self._translate_to_real_memory_address(process, memory_page_address))
