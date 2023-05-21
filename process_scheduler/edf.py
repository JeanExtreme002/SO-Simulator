from typing import Optional, Tuple, List
from process_scheduler.abstract import ProcessScheduler
from process import Process


class EDFProcessScheduler(ProcessScheduler):
    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        pass
