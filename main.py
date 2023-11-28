import sys
from pathlib import Path

from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtCore import QObject, Slot, Signal

class Controller(QObject):
    @Slot()
    def pickFile(self):
        print('hello')


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
