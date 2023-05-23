from memory_paging import MemoryManager
from process import Process


class FIFOMemoryManager(MemoryManager):

    __count = 0

    @property
    def name(self) -> str:
        return "First In First Out (FIFO)"

    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :return: Retorna o endereço da página em hexadecimal.
        """
        self.__count %= self.ram_memory_pages
        memory_address = super()._reserve(process, self.__count)

        self.__count += 1
        return memory_address

    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        super()._use(process, self._translate_to_real_memory_address(memory_page_address))
