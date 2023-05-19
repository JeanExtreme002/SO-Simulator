from tkinter import Button, Canvas, Label, Tk
from typing import Union
from process_scheduler import ProcessScheduler


class Application(Tk):
    """
    Classe principal da aplicação.
    """
    def __init__(self, title: str = "Window", size: tuple[int] = (1280, 720)):
        super().__init__()
        self.__size = size

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

    def build(self):
        self["bg"] = "white"

        self.__canvas = Canvas(
            self, width = self.__size[0] * 0.95, height = self.__size[1] * 0.8,
            borderwidth = 2, background = "white", relief = "solid"
        )
        self.__canvas.pack(pady = 10)

    def run(self, process_scheduler: ProcessScheduler, quantum: Union[int, None]):
        self.__process_scheduler = process_scheduler
        self.__quantum = quantum
        self.mainloop()
