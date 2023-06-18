from tkinter import Button, Frame, Label, Listbox, Scrollbar, Toplevel
from typing import List, Optional, Tuple

from memory_paging import MemoryManager


class MemoryWindow(Toplevel):
    """
    Classe para criar uma tela para mostrar as páginas de memória.
    """

    def __init__(self, title: str = "Window", size: tuple[int] = (600, 600)):
        super().__init__()
        self.__size = size

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

        self.protocol("WM_DELETE_WINDOW", self.__on_close)

    def __on_close(self):
        return False  # Impede que a janela seja fechada.

    def __on_move_list_box(self, *args):
        self.__list_box_1.yview(*args)
        self.__list_box_2.yview(*args)
        self.__list_box_3.yview(*args)
        self.__list_box_4.yview(*args)

    def __on_mouse_wheel(self, event):
        self.__list_box_1.yview("scroll", event.delta, "units")
        self.__list_box_2.yview("scroll", event.delta, "units")
        self.__list_box_3.yview("scroll", event.delta, "units")
        self.__list_box_4.yview("scroll", event.delta, "units")
        return "break"

    def build(self, pages: int):
        """
        Constrói a parte gráfica da janela.
        """
        self.__pages = pages

        self.__main_frame = Frame(self)
        self.__main_frame.pack(expand = True, fill = "both")

        self.__list_box_1 = Listbox(self.__main_frame, width = 20, background = "white")
        self.__list_box_1.insert(0, "Endereço Real:")

        for index in range(pages):
            self.__list_box_1.insert(index, str(index))

        self.__list_box_1.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_1.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_2 = Listbox(self.__main_frame, width = 20, background = "white")
        self.__list_box_2.insert(0, "Process ID:")

        self.__list_box_2.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_2.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_3 = Listbox(self.__main_frame, background = "white")
        self.__list_box_3.insert(0, "Endereço Virtual:")

        self.__list_box_3.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_3.pack(side = "left", expand = True, fill = "both")

        self.__list_box_4 = Listbox(self.__main_frame, background = "white")
        self.__list_box_4.insert(0, "Último Acesso:")

        self.__list_box_4.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_4.pack(side = "left", expand = True, fill = "both")

        self.__scrollbar = Scrollbar(self.__main_frame, orient = "vertical", command = self.__on_move_list_box)
        self.__list_box_1.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_2.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_3.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_4.config(yscrollcommand = self.__scrollbar.set)
        self.__scrollbar.pack(side = "left", expand = True, fill = "both")

    def update_real_memory_table(self, memory_manager: MemoryManager):
        """
        Atualiza a tabela com as informações da memória real.
        """
        real_memory_table = memory_manager.get_real_memory_table()

        self.__list_box_2.delete(1, "end")
        self.__list_box_3.delete(1, "end")
        self.__list_box_4.delete(1, "end")

        data = [("", "", "")] * self.__pages

        for real_address, process_id, virtual_address, last_use in real_memory_table:
            if process_id is None: continue
            data[real_address] = (str(process_id), str(virtual_address), last_use)

        for process_id, virtual_address, last_use in data:
            self.__list_box_2.insert("end", process_id)
            self.__list_box_3.insert("end", virtual_address)
            self.__list_box_4.insert("end", last_use)
