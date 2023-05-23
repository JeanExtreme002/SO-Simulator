from memory_paging import MemoryManager
from process import Process


class LRUMemoryManager(MemoryManager):
    def reserve(self, process: Process) -> str:
        """
        Reserva uma página para o dado processo.

        :returns: Retorna o endereço da página em hexadecimal.
        """
        pass

    def use(self, process: Process, memory_page_address: str):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass