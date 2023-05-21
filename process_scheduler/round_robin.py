from typing import Optional, Tuple, List
from process_scheduler.abstract import ProcessScheduler
from process import Process


class RoundRobinProcessScheduler(ProcessScheduler):

    @property
    def name(self) -> str:
        return "Round Robin (RR)"
    
    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        pass
