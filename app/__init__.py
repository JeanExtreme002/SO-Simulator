from tkinter import Button, Canvas, Label, Tk


class Application(Tk):
    """
    Classe principal da aplicação.
    """
    def __init__(self, title: str = "Window", size: tuple[int] = (1280, 720)):
        super().__init__()
        self.__title = title
        self.__size = size

    def build(self):
        pass

    def run(self):
        pass
