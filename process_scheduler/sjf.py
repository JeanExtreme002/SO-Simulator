from process_scheduler.abstract import ProcessScheduler
from process import Process


class SJFProcessScheduler(ProcessScheduler):

    def run(self) -> Process:
        if not self.processes: return

        processes = self.processes

        # Ordena os processos pela duração e obtém o mais próximo de finalizar.
        processes.sort(key = lambda process: process.duration)
        process = processes[0]

        if process.is_finished():
            self.remove_process(process)

        for process in processes[1:]:
            process.wait()
