from process_scheduler.abstract import ProcessScheduler
from process import Process


class RoundRobinProcessScheduler(ProcessScheduler):
    def run(self) -> Process:
        pass
