from process_scheduler.abstract import ProcessScheduler
from process import Process


class SJFProcessScheduler(ProcessScheduler):
    __running = None

    def remove_process(self, process: Process):
        super().remove_process(process)

        if process == self.__running:
            self.__running = None

    def run(self) -> Process:
        if not self.processes: return

        processes = self.processes
        process = self.__running

        # Se não houver processo em execução, ordena os processos pela duração e obtém o mais próximo de finalizar.
        if process is None:
            processes.sort(key = lambda process: process.duration)
            process = processes[0]

        self.__running = process

        if process.is_finished():
            self.remove_process(process)

        for process_asleep in processes:
            if process_asleep.id != process.id:
                process_asleep.wait()
