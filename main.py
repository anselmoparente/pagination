import sys
from pathlib import Path

from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtCore import QObject, Slot, Signal

class Controller(QObject):
    fileName = ''
    content = ''
    option = 5
    frames = 0
    reference = 0

    @Slot(str)
    def changeFileName(self, text):
        self.fileName = text[8:]
        with open(self.fileName, 'r') as file:
            self.content = file.read()
        if self.content[len(self.content) - 1:len(self.content)]:
            self.content = self.content[:len(self.content) - 1]

    @Slot(str)
    def changeOption(self, selectedOption):
        self.option = int(selectedOption)

    @Slot(str)
    def changeFrames(self, value):
        self.frames = int(value)

    @Slot(str)
    def changeReferences(self, value):
        self.reference = int(value)

    @Slot()
    def run(self):
        if self.option == 0:
            fifo_algorithm = FIFO(self.frames)
            fifo_algorithm.simulate(self.content)
        if self.option == 1:
            second_chance_algorithm = SecondChance(self.frames, self.reference)
            references = self.content.split('-')
            reference_list = [(int(references[i][:-1]), references[i][-1]) for i in range(len(references))]
            second_chance_algorithm.apply_algorithm(reference_list)
        if self.option == 3:
            lru = LeastRecentlyUsed(self.frames)
            lru.process_reference_string(self.content)
            lru.print_results()

class FIFO:
    def __init__(self, frames):
        self.frames = frames  # Número de quadros de página
        self.page_queue = []  # Fila de páginas na memória
        self.total = 0  # Total de elementos na string
        self.faults = 0  # Faltas
        self.accepts = 0  # Acertos

    def page_fault(self, page):
        if len(self.page_queue) < self.frames:
            self.page_queue.append(page)
        else:
            evicted_page = self.page_queue.pop(0)
            self.page_queue.append(page)

    def simulate(self, reference_string):
        for operation in reference_string.split('-'):
            page = int(operation[:-1])  # Remove o último caractere para obter o número da página
            operation_type = operation[-1]

            if page not in self.page_queue:
                self.faults = self.faults + 1
                self.page_fault(page)
                self.total = self.total + 1
            else:
                self.accepts = self.accepts + 1
                self.total = self.total + 1

        print('Número da faltas: ' + str(self.faults))
        print('Número da acertos: ' + str(self.accepts))
        print('Porcentagem de acerto: ' + str(round(self.accepts/self.total, 2) * 100) + '%')
        print('Estado final: ' + str(self.page_queue))

class SecondChance:
    def __init__(self, no_of_frames, reset_frequency):
        self.no_of_frames = no_of_frames  # Total de frames
        self.reset_frequency = reset_frequency  # Frequencia que o bit R eh resetado
        self.frames = [(-1, False) for _ in range(no_of_frames)]  # Os Frames
        self.total_page_fault = 0  # Numero de faltas
        self.pointer = 0  # Ponteiro que sera utilizado na procura da pagina na memoria
        self.reset_counter = 0  # Contador para resetar o bit R
        self.total_page_hit = 0 # Numero de acertos
        self.total = 0

    def print_frames(self):  # Imprime os frames
        #print("Estado final:", self.frames)
        for i in self.frames:
            print(i[0], end=" ")
        print()

    def find_and_replace(self, page):  # Procura qual pagina devera ser substituida
        while True:
            if not self.frames[self.pointer][1]:
                self.frames[self.pointer] = (page, True)
                self.pointer = (self.pointer + 1) % self.no_of_frames
                return
            self.frames[self.pointer] = (self.frames[self.pointer][0], False)
            self.pointer = (self.pointer + 1) % self.no_of_frames

    def is_need_for_update(self, page):  # Checa se a pagina ja esta nos frames
        for i in range(self.no_of_frames):
            if self.frames[i][0] == page:
                self.frames[i] = (self.frames[i][0], True)
                self.total_page_hit += 1
                return False
        return True

    def apply_algorithm(self, reference_string):
        for page in reference_string:
            if self.reset_counter == self.reset_frequency:
                # Reseta o bit R para todas as paginas nos frames
                self.frames = [(frame[0], False) for frame in self.frames]
                self.reset_counter = 0

            # Procura se a pagina nao esta na memoria
            if self.is_need_for_update(page[0]):
                self.find_and_replace(page[0])
                self.total_page_fault += 1

            self.reset_counter += 1
            self.total += 1

        print('Número da faltas: ' + str(self.total_page_fault))
        print('Número da acertos: ' + str(self.total - self.total_page_fault))
        print('Porcentagem de acerto: ' + str(round((self.t0otal - self.total_page_fault)/self.total, 2) * 100) + '%')
        print('Estado final: ')
        self.print_frames()

class LeastRecentlyUsed:
    def __init__(self, size):
        self.size = size  # Número de quadros de página
        self.pages = []  # Fila de páginas na memória
        self.listorder = []  # Lista de ordem de entrada das páginas
        self.total = 0  # Total de elementos na string
        self.faults = 0  # Faltas
        self.accepts = 0  # Acertos

    def parse_reference(self, reference):  # Pega a reference_string
        page_number, operation = reference[:-1], reference[-1]  # Separa a parte do numero da parte da operacao(R ou W)
        return int(page_number), operation  # Converte o numero da pagina para um inteiro

    def process_reference_string(self, reference_string):
        for ref in reference_string.split('-'):
            page, op = self.parse_reference(ref)

            if page in self.pages:
                self.listorder.remove(page)
                self.listorder.append(page)
                self.accepts += 1
            else:
                self.faults += 1
                if len(self.pages) < self.size:
                    self.pages.append(page)
                else:
                    # Acha a pagina menos recetemente usada
                    lru_page = min(self.listorder, key=self.listorder.index)  # Procura a pagina com menor index na fila
                    self.listorder.remove(lru_page)
                    self.pages[self.pages.index(lru_page)] = page

                self.listorder.append(page)

            self.total += 1

    def print_results(self):
        print('Número da faltas: ' + str(self.faults))
        print('Número da acertos: ' + str(self.accepts))
        print('Porcentagem de acerto: ' + str(round(self.accepts / self.total, 2) * 100) + '%')
        print('Estado final: ' + str(self.pages))


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    controller = Controller()
    engine.rootContext().setContextProperty("backend", controller)
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
