from memory_paging import MemoryManager
from process import Process


class LRUMemoryManager(MemoryManager):

    __count = 0

    @property
    def name(self) -> str:
        return "Least Recently Used (LRU)"

    def __find_least_recently_used_address(self) -> int:
        """
        Retorna o endereço da página menos recentemente utilizada.
        """
        minimum, address = float("inf"), 0

        for index in range(self.ram_memory_pages):
            value = self._real_memory_table[index]
            if value < minimum: minimum, address = value, index
        return address

    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :returns: Retorna o endereço da página em hexadecimal.
        """
        if self.__count < self.ram_memory_pages:
            real_memory_address = self.__count
            self.__count += 1
        else:
            real_memory_address = self.__find_least_recently_used_address()

        return super()._reserve(process, real_memory_address, 1)

    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        real_memory_address = self._translate_to_real_memory_address(memory_page_address)

        # Aumenta a pontuação da página de memória utilizada.
        value = super()._use(process, real_memory_address)
        self._real_memory_table[real_memory_address][1] += 1

        # Diminui a pontuação das outras páginas de memória.
        for address in range(self.ram_memory_pages):
            if address == real_memory_address: continue
            self._real_memory_table[address][1] -= 1