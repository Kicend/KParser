import sys
import PyQt5.QtWidgets as QTw

class KParser(QTw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logo = QTw.QLabel("""
            888    d8P  8888888b.                                            
            888   d8P   888   Y88b                                           
            888  d8P    888    888                                           
            888d88K     888   d88P 8888b.  888d888 .d8888b   .d88b.  888d888 
            8888888b    8888888P"     "88b 888P"   88K      d8P  Y8b 888P"   
            888  Y88b   888       .d888888 888     "Y8888b. 88888888 888     
            888   Y88b  888       888  888 888          X88 Y8b.     888     
            888    Y88b 888       "Y888888 888      88888P'  "Y8888  888
        """, self)
        self.main_menu()

    def main_menu(self):
        self.resize(540, 480)
        self.setWindowTitle("KParser")
        test_btn = QTw.QPushButton("&Test", self)
        layout = QTw.QGridLayout()
        layout.addWidget(self.logo, 0, 0)
        layout.addWidget(test_btn, 1, 0)
        self.setLayout(layout)
        self.show()

app = QTw.QApplication(sys.argv)
window = KParser()
sys.exit(app.exec_())
