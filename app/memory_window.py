from tkinter import Button, Label, Listbox, Toplevel


class MemoryWindow(Toplevel):
    """
    Classe para criar uma tela para mostrar as páginas de memória.
    """

    def __init__(self, title: str = "Window", size: tuple[int] = (500, 600)):
        super().__init__()
        self.__size = size

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

        self.protocol("WM_DELETE_WINDOW", self.__on_close)

    def __on_close(self):
        return False  # Impede que a janela seja fechada.

    def build(self):
        pass