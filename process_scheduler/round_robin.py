from process_scheduler.abstract import ProcessScheduler
from process import Process


class RoundRobinProcessScheduler(ProcessScheduler):
    @property
    def name(self) -> str:
        return "Round Robin (RR)"
    
    def run(self) -> Process:
        pass
