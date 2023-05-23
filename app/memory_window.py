from tkinter import Button, Frame, Label, Listbox, Toplevel


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

    def build(self, pages: int):
        self.__main_frame = Frame(self)
        self.__main_frame.pack(expand = True, fill = "both")

        self.__list_box_1 = Listbox(self.__main_frame, width = 20, background = "white")
        self.__list_box_1.insert(0, "Real Address:")

        for index in range(1, pages + 1):
            self.__list_box_1.insert(index, str(index))

        self.__list_box_1.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_2 = Listbox(self.__main_frame, width = 20, background = "white")
        self.__list_box_2.insert(0, "Process ID:")
        self.__list_box_2.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_3 = Listbox(self.__main_frame, background = "white")
        self.__list_box_3.insert(0, "Virtual Memory Address")
        self.__list_box_3.pack(side = "left", expand = True, fill = "both")