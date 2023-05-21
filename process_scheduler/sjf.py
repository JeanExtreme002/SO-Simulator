from typing import List, Optional, Tuple
from process_scheduler.abstract import ProcessScheduler
from process import Process


class SJFProcessScheduler(ProcessScheduler):
    __running = None

    @property
    def name(self) -> str:
        return "Shortest Job First (SJF)"

    def remove_process(self, process: Process):
        super().remove_process(process)

        if process == self.__running:
            self.__running = None

    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        if not self.processes: return

        processes = self.processes
        process = self.__running

        # Se não houver processo em execução, ordena os processos pela duração e obtém o mais próximo de finalizar.
        if process is None:
            processes.sort(key = lambda process: process.duration)
            process = processes[0]

        process.run()
        self.__running = process

        if process.is_finished():
            self.remove_process(process)

        asleep_processes = list()

        for asleep_process in processes:
            if asleep_process.id != process.id:
                asleep_process.wait()
                asleep_processes.append(asleep_process)

        return process, asleep_processes, False
