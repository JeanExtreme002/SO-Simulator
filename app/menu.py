from tkinter import Button, Frame, Label, Menu, Tk
from tkinter.ttk import Entry, Menubutton
from process_scheduler.edf import EDFProcessScheduler
from process_scheduler.fifo import FIFOProcessScheduler
from process_scheduler.round_robin import RoundRobinProcessScheduler
from process_scheduler.sjf import SJFProcessScheduler


class MenuWindow(Tk):
    """
    Classe para criar uma tela inicial de menu.
    """
    def __init__(self, title: str = "Window", size: tuple[int] = (350, 200)):
        super().__init__()
        self.__size = size

        self.__algorithm = FIFOProcessScheduler
        self.__context_switching = None
        self.__quantum = None
        self.__closed = True

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

    @property
    def closed(self):
        return self.__closed

    def __finish_config(self):
        """
        Encerra a janela de menu, salvando as configurações feitas.
        """
        self.__quantum = self.__entry_2.get()
        self.__context_switching = self.__entry_3.get()

        # Deve haver um quantum e um chaveamento para os algoritmos RR e EDF.
        if self.__algorithm in [RoundRobinProcessScheduler, EDFProcessScheduler]:
            if len(self.__quantum) == 0:
                self.__label_2["fg"] = "red"
                return
            self.__label_2["fg"] = "black"

            if len(self.__context_switching) == 0:
                self.__label_3["fg"] = "red"
                return

            self.__quantum = int(self.__quantum)
            self.__context_switching = int(self.__context_switching)
        else:
            self.__quantum = None
            self.__context_switching = None

        self.__closed = False
        self.destroy()

    def __set_algorithm(self, index: int):
        """
        Define o algorimo (classe) que será utilizado pelo simulador.
        """
        self.__algorithm = [
            FIFOProcessScheduler,
            SJFProcessScheduler,
            RoundRobinProcessScheduler,
            EDFProcessScheduler
        ][index]

        if index in [0, 1]:
            self.__entry_2.delete(0, "end")
            self.__entry_3.delete(0, "end")

        self.__label_2["fg"] = "black"
        self.__label_3["fg"] = "black"

        self.__menu_button.config(text = ["FIFO", "SFJ", "RR", "EDF"][index])

    def __validate_entry(self, string):
        """
        Valida a entrada do usuário na Entry.
        """
        if self.__algorithm not in [RoundRobinProcessScheduler, EDFProcessScheduler]:
            self.__entry_2.delete(0, "end")
            self.__entry_3.delete(0, "end")
            return False

        for char in string:
            if char not in "0123456789": return False
        return True

    def build(self):
        """
        Constrói a parte gráfica da janela.
        """
        self["bg"] = "white"

        self.__main_frame = Frame(self)
        self.__main_frame["bg"] = "white"
        self.__main_frame.pack(pady = 20, padx = 20, expand = True, fill = "x")

        # Widgets para selecionar o algoritmo para escalonar os processos
        self.__frame_1 = Frame(self.__main_frame)
        self.__frame_1["bg"] = "white"
        self.__frame_1.pack(expand = True, fill = "x")

        self.__label_1 = Label(self.__frame_1, text = "Selecione o algoritmo de escalonamento:", bg = "white")
        self.__label_1.pack(side = "left")

        self.__menu_button = Menubutton(self.__frame_1)
        self.__menu_button.pack(side = "left", expand = True, fill = "x")

        self.__menu = Menu(tearoff = 0, bg = "white")

        self.__menu.add_command(label = "FIFO", command = lambda: self.__set_algorithm(0))
        self.__menu.add_command(label = "SJF", command = lambda: self.__set_algorithm(1))
        self.__menu.add_command(label = "RR", command = lambda: self.__set_algorithm(2))
        self.__menu.add_command(label = "EDF", command = lambda: self.__set_algorithm(3))

        self.__menu_button.config(menu = self.__menu, text = "FIFO")

        self.__entry_reg = self.register(self.__validate_entry)

        # Widgets para selecionar o quantum da CPU.
        self.__frame_2 = Frame(self.__main_frame)
        self.__frame_2["bg"] = "white"
        self.__frame_2.pack(pady = 10, expand = True, fill = "x")

        self.__label_2 = Label(self.__frame_2, text = "Quantum do processador (inteiro):", bg = "white")
        self.__label_2.pack(side = "left")

        self.__entry_2 = Entry(self.__frame_2, width = 4)
        self.__entry_2.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__entry_2.pack(side = "left", expand = True, fill = "x")

        # Widgets para selecionar o chaveamento da CPU.
        self.__frame_3 = Frame(self.__main_frame)
        self.__frame_3["bg"] = "white"
        self.__frame_3.pack(expand = True, fill = "x")

        self.__label_3 = Label(self.__frame_3, text = "Chaveamento do processador (inteiro):", bg = "white")
        self.__label_3.pack(side = "left")

        self.__entry_3 = Entry(self.__frame_3, width = 4)
        self.__entry_3.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__entry_3.pack(side = "left", expand = True, fill = "x")

        # Botão para sair do menu de configuração.
        self.__button = Button(
            self.__main_frame, text = "Iniciar", command = self.__finish_config,
            font = ("Arial", int(self.__size[1] * 0.13))
        )
        self.__button.pack(pady = 10)

    def get_config(self):
        """
        Retorna as configurações enviadas pelo usuário.
        """
        return self.__algorithm(), self.__quantum, self.__context_switching

    def run(self):
        """
        Executa a janela de menu.
        """
        self.mainloop()