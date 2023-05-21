from tkinter import Button, Canvas, Entry, Frame, Label, Tk
from typing import Tuple, Union

from process import Process
from process_scheduler import ProcessScheduler

import random


class Application(Tk):
    """
    Classe principal da aplicação.
    """

    def __init__(self, title: str = "Window", size: tuple[int] = (1280, 720)):
        super().__init__()
        self.__size = size

        self.__history_length = 20
        self.__history_border = 1
        self.__history_min_rows = 5

        self.__process_history = []
        self.__process_list = []
        self.__process_count = 0

        self.__last_process_list_length = self.__history_min_rows

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

    def __add_process(self):
        """
        Adiciona um novo processo para o simulador.
        """
        duration = self.__duration_entry.get()
        deadline = self.__deadline_entry.get()

        if not duration: return self.__duration_label.config(foreground = "red")
        self.__duration_label.config(foreground = "black")

        duration = int(duration)
        deadline = int(deadline) if deadline else None

        process = Process(process_id = self.__process_count, duration = duration, deadline = deadline)  # Only for test. It must be replaced later.
        process.index = len(self.__process_history)
        self.__process_count += 1

        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        process.color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

        self.__process_scheduler.add_process(process)
        self.__process_history.append([None] * self.__history_length)

        self.__process_list.append(process)

    def __draw_grid(self, length: int):
        """
        Desenha um grid na tela de histórico.
        """
        length = max(length, self.__history_min_rows)

        process_width, process_height = self.__get_process_size_on_history(length)

        for y in range(length - 1):
            for x in range(self.__history_length - 1):

                self.__canvas.create_rectangle(
                    process_width * x + self.__history_border * x + process_width, 0,
                    process_width * x + self.__history_border * x + process_width + self.__history_border, self.__canvas_height + 10,
                    fill="black"
                )
            self.__canvas.create_rectangle(
                0, process_height * y + self.__history_border * y + process_height,
                self.__canvas_width + 10, process_height * y + self.__history_border * y + process_height + self.__history_border,
                fill="black"
            )

    def __get_process_size_on_history(self, length: int) -> Tuple[int, int]:
        """
        Calcula a largura e altura do processo para a tela de histórico.
        """
        length = max(length, self.__history_min_rows)

        process_width = (self.__canvas_width - self.__history_border * (self.__history_length - 1)) / self.__history_length
        process_height = (self.__canvas_height - self.__history_border * (length - 1)) / length

        return int(process_width), int(process_height)

    def __on_update(self):
        """
        Evento executado periodicamente pela interface gráfica.
        """
        self.__canvas.delete("all")

        if len(self.__process_history) == 0:
            self.__draw_grid(self.__last_process_list_length)
            return self.after(self.__on_update_interval, self.__on_update)

        # Executa o próximo processo.
        result = self.__process_scheduler.run()
        process, asleep_processes, context_switching = (result[0], result[1], result[2]) if result is not None else (None, None, None)

        # Adiciona o estado do processo ao histórico.
        if context_switching: self.__process_history[process.index][self.__history_length - 1] = (str(), "#999")
        elif process: self.__process_history[process.index][self.__history_length - 1] = (process.id, process.color)

        # Remove processos que já saíram do histórico.
        for process in self.__process_list.copy():
            if process.is_finished() and not any(self.__process_history[process.index]):
                self.__remove_process(process)

        # Calcula a largura e altura correta dos processos.
        process_width, process_height = self.__get_process_size_on_history(len(self.__process_history))
        self.__last_process_list_length = len(self.__process_history)

        # Mostra o histórico de todos os processos, até um dado momento, no canvas.
        for y in range(len(self.__process_history)):
            for x in range(self.__history_length):
                element = self.__process_history[y][x]

                if type(element) is tuple:
                    color = element[1]
                else: continue

                # Calcula o X1 do processo.
                x1 = process_width * x + self.__history_border * x

                # Calcula o Y1 do processo.
                y1 = process_height * y + self.__history_border * y

                # Calcula o X2 do processo (X1 + width).
                x2 = process_width * x + self.__history_border * x + process_width

                if x == self.__history_length - 1:
                    x2 = self.__canvas_width + 10

                # Calcula o Y2 do processo (X2 + height).
                y2 = process_height * y + self.__history_border * y + process_height

                if y == len(self.__process_history) - 1 and y >= self.__history_min_rows - 1:
                    y2 = self.__canvas_height + 10

                # Desenha o processo com o seu ID.
                self.__canvas.create_rectangle(x1, y1, x2, y2, fill = color)
                self.__canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text = element[0])

        self.__draw_grid(self.__last_process_list_length)

        # Move o histórico para a esquerda e repete a execução do método, após um determinado tempo.
        self.__shift_process_history()
        self.after(self.__on_update_interval, self.__on_update)

    def __remove_process(self, process: Process):
        """
        Remove um processo do simulador.
        """
        new_process_list = list()

        for p in self.__process_list:
            if p is not process:
                if p.index > process.index:
                    p.index -= 1
                new_process_list.append(p)

        self.__process_list = new_process_list
        self.__process_history = self.__process_history[:process.index] + self.__process_history[process.index + 1:]

    def __shift_process_history(self):
        """
        Move o histórico dos processos para a esquerda.
        """
        for y in range(len(self.__process_history)):
            for x in range(self.__history_length - 1):
                self.__process_history[y][x] = self.__process_history[y][x + 1]
            self.__process_history[y][self.__history_length - 1] = None

    def __validate_entry(self, string):
        """
        Valida a entrada do usuário na Entry.
        """
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
        self.__main_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        self.__canvas_label_frame = Frame(self.__main_frame)
        self.__canvas_label_frame["bg"] = "white"
        self.__canvas_label_frame.pack(expand = True, fill ="x")

        self.__canvas_label = Label(
            self.__canvas_label_frame, text ="Histórico do estado dos processos (por segundo).",
            background = "white"
        )
        self.__canvas_label.pack(side = "left")

        self.__canvas_width = (
            self.__size[0] * 0.95 - (self.__size[0] * 0.95 % self.__history_length)
            + self.__history_border * (self.__history_length - 1)
        )
        self.__canvas_height = self.__size[1] * 0.8

        self.__canvas = Canvas(
            self.__main_frame, width = self.__canvas_width, height = self.__canvas_height,
            borderwidth = 2, background = "white", relief = "solid"
        )
        self.__draw_grid(self.__last_process_list_length)
        self.__canvas.pack(pady = 10)

        self.__add_process_frame = Frame(self.__main_frame)
        self.__add_process_frame["bg"] = "white"
        self.__add_process_frame.pack(pady = 10)

        self.__add_process_button = Button(
            self.__add_process_frame, text = "Adicionar Processo",
            command = self.__add_process, background = "lightgreen"
        )
        self.__add_process_button.pack(padx = 10, side = "left")

        self.__duration_frame = Frame(self.__add_process_frame)
        self.__duration_frame["bg"] = "white"
        self.__duration_frame.pack(side = "left", padx = 10)

        self.__duration_label = Label(self.__duration_frame, text = "Duração: ", background = "white")
        self.__duration_label.pack(side = "left")

        self.__entry_reg = self.register(self.__validate_entry)

        self.__duration_entry = Entry(self.__duration_frame)
        self.__duration_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__duration_entry.pack(side = "left")

        self.__deadline_label = Label(self.__add_process_frame, text="Deadline: ", background = "white")
        self.__deadline_label.pack(side="left")

        self.__deadline_entry = Entry(self.__add_process_frame)
        self.__deadline_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__deadline_entry.pack(side="left")

    def run(self, process_scheduler: ProcessScheduler, interval: int = 1000):
        """
        Executa a aplicação principal, com sua parte gráfica.
        """
        self.__process_scheduler = process_scheduler
        self.__on_update_interval = interval

        self.after(self.__on_update_interval, self.__on_update)
        self.mainloop()
