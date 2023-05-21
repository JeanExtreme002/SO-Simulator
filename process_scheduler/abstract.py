from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from process import Process


class ProcessScheduler(ABC):
    def __init__(self, quantum: Optional[int] = None):
        self.__process_list = list()
        self.__quantum = quantum

    def __len__(self) -> int:
        return len(self.__process_list)

    @property
    def processes(self) -> List[Process]:
        return self.__process_list.copy()

    @property
    def quantum(self):
        return self.__quantum

    def add_process(self, process: Process):
        """
        Adiciona um processo.
        """
        self.__process_list.append(process)

    def remove_process(self, process: Process):
        """
        Remove um processo.
        """
        self.__process_list.remove(process)

    @abstractmethod
    def run(self) -> Optional[Tuple[Process, List[Process]]]:
        """
        Executa um processo.

        :return: Retorna o processo executado e uma lista com os processos em espera.
        """
        pass

