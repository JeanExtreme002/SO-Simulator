from abc import ABC, abstractmethod


class ProcessScheduler(ABC):
    def __init__(self): pass


class FIFOProcessScheduler(ProcessScheduler):
    pass


class SJFProcessScheduler(ProcessScheduler):
    pass


class RoundRobinProcessScheduler(ProcessScheduler):
    pass


class EDFProcessScheduler(ProcessScheduler):
    pass