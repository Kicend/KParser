import sys
import data.modules.core.core as cr
import data.modules.settings as sett
import PyQt5.QtWidgets as QTw
import PyQt5.QtGui as QTg
import PyQt5.QtCore as QTc
from PyQt5.QtCore import pyqtSlot
from setproctitle import setproctitle
from json import load, decoder
from random import randint

class KParser(QTw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_tmp = {}
        self.label = QTw.QLabel(self)
        self.layout_VBox = QTw.QVBoxLayout(self)
        self.layout_HBox = QTw.QHBoxLayout(self)
        self.widget = QTw.QWidget(self)
        self.pixmap = QTg.QPixmap("data/images/logo.png")
        self.main()

    def main(self):
        if cr.cache["first_config"]:
            answer = self.first_config_event()
            if answer == "Yes":
                sett.change_parameter("first_config", False)
                cr.cache["mode"] = 1
            else:
                sett.change_parameter("first_config", False)
        del cr.cache["first_config"]
        cr.cache["OS"] = sys.platform
        cr.cache["search_id"] = 0
        with open("data/UA.json", "r") as f:
            ua = load(f)
            cr.cache["user_agent"] = ua[str(randint(0, 8))]
        try:
            self.main_menu(cr.cache["mode"])
        except KeyError:
            self.main_menu()

    def main_menu(self, mode=0):
        if mode == 1:
            del cr.cache["mode"]
        self.clear_layout(self.layout_VBox)
        self.widget.setFixedHeight(160)
        self.resize(160, 200)
        self.setWindowTitle("Menu Główne - KParser")
        start_btn = QTw.QPushButton("Zacznij wyszukiwanie", self)
        settings_btn = QTw.QPushButton("Ustawienia", self)
        label = QTw.QLabel(self)
        label.setPixmap(self.pixmap)
        self.layout_VBox.addWidget(label)
        self.layout_VBox.addWidget(start_btn, 0)
        self.layout_VBox.addWidget(settings_btn, 1)
        self.widget.setLayout(self.layout_VBox)
        start_btn.clicked.connect(self.start)
        settings_btn.clicked.connect(self.settings)
        self.show()
        if mode == 1:
            self.settings()

    @pyqtSlot()
    def start(self):
        self.clear_layout(self.layout_VBox)
        self.resize(160, 200)
        self.setWindowTitle("KParser")
        start_btn = QTw.QPushButton("Zacznij wyszukiwanie", self)
        settings_btn = QTw.QPushButton("Ustawienia", self)
        self.label.setPixmap(self.pixmap)
        self.layout_VBox.addWidget(self.label)
        self.layout_VBox.addWidget(start_btn, 0)
        self.layout_VBox.addWidget(settings_btn, 1)
        self.widget.setLayout(self.layout_VBox)
        self.show()

    @pyqtSlot()
    def settings(self):
        self.clear_layout(self.layout_VBox)
        self.clear_layout(self.layout_HBox)
        self.resize(160, 320)
        self.setWindowTitle("Ustawienia - KParser")
        confirm_btn = QTw.QPushButton("Zastosuj", self)
        confirm_btn.setEnabled(False)

        def settings_change():
            sending_button = self.sender()
            par_id = sending_button.objectName()
            if par_id == "check_registry":
                self.settings_tmp[par_id] = sending_button.isChecked()
            elif par_id == "queries_number" or par_id == "pause":
                val = sending_button.text()
                try:
                    val = int(val)
                    self.settings_tmp[par_id] = val
                except ValueError:
                    if val != "":
                        self.invalid_value_type("Nieprawidłowy typ danych: Dozwolone są liczby całkowite")
            else:
                self.settings_tmp[par_id] = sending_button.currentIndex()
            confirm_btn.setEnabled(True)
        back_btn = QTw.QPushButton("Wróć", self)
        with open("data/config/config.json", "r") as f:
            config = load(f)
        i = 0
        for parameter, value in config.items():
            if parameter == "first_config":
                break
            self.layout_VBox.addWidget(QTw.QLabel(parameter, self), i)
            if type(value) == bool:
                check_box = QTw.QCheckBox(self)
                check_box.setObjectName(parameter)
                if value is True:
                    check_box.setChecked(True)
                self.layout_VBox.addWidget(check_box, i + 1)
                check_box.clicked.connect(settings_change)
            elif type(value) == int:
                edit_line = QTw.QLineEdit(str(value), self)
                edit_line.setObjectName(parameter)
                self.layout_VBox.addWidget(edit_line, i + 1)
                edit_line.textChanged.connect(settings_change)
            elif type(value) == str:
                combo_box = QTw.QComboBox(self)
                combo_box.setObjectName(parameter)
                if parameter == "search_lang":
                    for element in sett.search_lang:
                        combo_box.addItem(element)
                else:
                    combo_box.addItem("basic")
                    combo_box.addItem("ext")
                combo_box.setCurrentText(value)
                self.layout_VBox.addWidget(combo_box, i + 1)
                # noinspection PyUnresolvedReferences
                combo_box.currentIndexChanged.connect(settings_change)
            i += 1
        self.layout_HBox.addWidget(confirm_btn)
        self.layout_HBox.addWidget(back_btn)
        self.layout_VBox.addLayout(self.layout_HBox)
        self.widget.setLayout(self.layout_VBox)
        self.widget.setFixedHeight(300)
        confirm_btn.clicked.connect(self.change_settings_confirm)
        back_btn.clicked.connect(self.main_menu)
        self.show()

    @pyqtSlot()
    def change_settings_confirm(self):
        if self.settings_tmp:
            keys = self.settings_tmp.keys()
            values = self.settings_tmp.values()
            for parameter in keys:
                for value in values:
                    sett.change_parameter(parameter, value)
                    break
        self.settings()

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def first_config_event(self):
        answer = QTw.QMessageBox.question(
            self, "Komunikat",
            "Czy chcesz wstępnie skonfigurować program KParser?",
            QTw.QMessageBox.Yes | QTw.QMessageBox.No)

        if answer == QTw.QMessageBox.Yes:
            return "Yes"
        else:
            return "No"

    def invalid_value_type(self, text: str):
        QTw.QMessageBox.warning(
            self, "Błąd", text
        )

if __name__ == "__main__":
    setproctitle("KParser_gui")
    cr.startup()
    cr.cache = dict(cr.cache_update())
    app = QTw.QApplication(sys.argv)
    window = KParser()
    sys.exit(app.exec_())
