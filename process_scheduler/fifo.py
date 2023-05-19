from .abstract import ProcessScheduler
from ..process import Process


class FIFOProcessScheduler(ProcessScheduler):
    def run(self) -> Process:
        if not self.processes: return

        process = self.processes[0]
        process.run()

        if process.is_finished():
            self.remove_process(process)

        for process in self.processes[1:]:
            process.wait()
