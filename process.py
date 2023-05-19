from typing import Optional


class Process(object):
    """
    Representa um processo no sistema operacional.
    """

    def __init__(self, process_id: int, duration: int, deadline: Optional[int] = None):
        """
        :param duration: Duração para o processo executar completamente na CPU.
        :param deadline: Tempo em que o processo necessita ser executado completamente.
        """
        self.__id = process_id
        self.__duration = duration
        self.__deadline = deadline

    @property
    def id(self) -> int:
        return self.__id

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def deadline(self) -> int:
        return self.__deadline

    def is_finished(self) -> True:
        """
        Verifica se o processo encerrou completamente.
        """
        return self.__duration <= 0

    def has_died(self) -> True:
        """
        Verifica se o tempo do deadline foi excedido.
        """
        return self.__deadline <= 0

    def run(self, time: Optional[int] = 1):
        """
        Executa o processo.
        :param time: tempo em que o processo permaneceu na CPU.
        """
        self.__duration -= time

    def wait(self, time: Optional[int] = 1):
        """
        Informa que o processo deve esperar.
        :param time: tempo em que o processo espera.

        :raises: TimeoutError se o tempo do deadline for excedido.
        """
        self.__deadline -= time

        if self.has_died():
            raise TimeoutError("The process is over!")
