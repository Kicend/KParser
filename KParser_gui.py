import sys
from PyQt5.QtWidgets import QApplication, QWidget

class KParser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()

    def interface(self):
        self.resize(300, 100)
        self.setWindowTitle("KParser")
        self.show()

app = QApplication(sys.argv)
window = KParser()
sys.exit(app.exec_())
