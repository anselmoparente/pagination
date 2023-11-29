import sys
from pathlib import Path

from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtCore import QObject, Slot, Signal

class Controller(QObject):
    fileName = ''
    content = ''
    option = 0
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
