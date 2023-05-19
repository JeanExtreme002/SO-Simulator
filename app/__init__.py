from tkinter import Button, Canvas, Label, Tk


class Application(Tk):
    """
    Classe principal da aplicação.
    """
    def __init__(self, title: str = "Window", size: tuple[int] = (1280, 720)):
        super().__init__()

        self.title(title)
        self.geometry("{}x{}".format(*size))

    def build(self):
        self["bg"] = "white"

    def run(self):
        self.mainloop()
