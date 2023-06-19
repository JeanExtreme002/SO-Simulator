from tkinter import Entry, Frame, Label, Listbox, Scrollbar, Toplevel
from memory_paging import MemoryManager


class VirtualMemoryWindow(Toplevel):
    """
    Classe para criar uma tela para mostrar as páginas de memória virtuais.
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

    def __validate_entry(self, string):
        """
        Valida a entrada do usuário para a Entry de Process ID.
        """
        for char in string:
            if char not in "0123456789": return False

        self.update_table(string)
        return True

    def build(self, memory_manager: MemoryManager):
        """
        Constrói a parte gráfica da janela.
        """
        self.__memory_manager = memory_manager

        self["bg"] = "white"
        
        self.__main_frame = Frame(self)
        self.__main_frame["bg"] = "white"
        self.__main_frame.pack(expand = True, fill = "both")

        self.__list_box_1 = Listbox(self.__main_frame, width = 20, height = int(self.__size[1] * 0.05), background = "white")
        self.__list_box_1.insert(0, "Process ID:")

        self.__list_box_1.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_1.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_2 = Listbox(self.__main_frame, width = 20, height = int(self.__size[1] * 0.05), background = "white")
        self.__list_box_2.insert(0, "Memória Virtual:")

        self.__list_box_2.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_2.pack(side = "left", fill = "y", ipadx = 0)

        self.__list_box_3 = Listbox(self.__main_frame, height = int(self.__size[1] * 0.05), background = "white")
        self.__list_box_3.insert(0, "Endereço Real:")

        self.__list_box_3.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_3.pack(side = "left", expand = True, fill = "both")

        self.__list_box_4 = Listbox(self.__main_frame, height = int(self.__size[1] * 0.05), background = "white")
        self.__list_box_4.insert(0, "Último Acesso:")

        self.__list_box_4.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__list_box_4.pack(side = "left", expand = True, fill = "both")

        self.__scrollbar = Scrollbar(self.__main_frame, orient = "vertical", command = self.__on_move_list_box)
        self.__list_box_1.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_2.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_3.config(yscrollcommand = self.__scrollbar.set)
        self.__list_box_4.config(yscrollcommand = self.__scrollbar.set)
        self.__scrollbar.pack(side = "left", expand = True, fill = "both")

        self.__input_frame = Frame(self)
        self.__input_frame["bg"] = "white"
        self.__input_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        self.__label = Label(
            self.__input_frame,
            text = "Search by inserting a process ID:",
            background = "white",
            font = ("Arial", int(self.__size[1] * 0.02))
        )
        self.__label.pack(side = "left")

        self.__entry_reg = self.register(self.__validate_entry)

        self.__entry = Entry(self.__input_frame, width = 30)
        self.__entry.config(validate = "key", validatecommand = (self.__entry_reg, "%P"))
        
        self.__entry["bg"] = "white"
        self.__entry.pack(padx = 10, side = "left")

        
    def update_table(self, filter_by_process_id: str = ""):
        """
        Atualiza a tabela com as informações da memória real.
        """
        if not filter_by_process_id:
            filter_by_process_id = self.__entry.get()
            
        self.__list_box_1.delete(1, "end")
        self.__list_box_2.delete(1, "end")
        self.__list_box_3.delete(1, "end")
        self.__list_box_4.delete(1, "end")

        for process_id, virtual_address, real_address, last_used_at in self.__memory_manager.get_virtual_memory_table():
            if filter_by_process_id != str(process_id): continue

            self.__list_box_1.insert("end", process_id)
            self.__list_box_2.insert("end", virtual_address)
            self.__list_box_3.insert("end", real_address if real_address is not None else "")
            self.__list_box_4.insert("end", last_used_at if last_used_at is not None else "")
