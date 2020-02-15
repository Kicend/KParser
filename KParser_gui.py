import sys
import data.modules.core.core as cr
import data.modules.settings as sett
import data.modules.search as search
import PyQt5.QtWidgets as QTw
import PyQt5.QtGui as QTg
from PyQt5.QtCore import pyqtSlot
from setproctitle import setproctitle
from json import load
from random import randint
from multiprocessing import Process
from os import makedirs

search_lang = ["pl",
               "en",
               "de",
               "fr",
               "cs",
               "sk"]

search_type = ["basic",
               "ext"]

class KParser(QTw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tmp = {}
        self.label = QTw.QLabel(self)
        self.layout_VBox = QTw.QVBoxLayout(self)
        self.layout_HBox = QTw.QHBoxLayout(self)
        self.layout_HBox_2 = QTw.QHBoxLayout(self)
        self.widget = QTw.QWidget(self)
        self.pixmap = QTg.QPixmap("data/images/logo.png")
        self.main()

    def main(self):
        cr.cache["start_mode"] = 0
        if cr.cache["first_config"]:
            answer = self.message_question("Czy chcesz wstępnie skonfigurować program KParser?")
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

    def main_menu(self, mode=0, layouts=None):
        if mode == 1:
            del cr.cache["mode"]
        if layouts is not None:
            self.clear_layout(layouts)
        self.clear_layout([self.layout_VBox, self.layout_HBox, self.layout_HBox_2])
        self.widget.setFixedHeight(160)
        self.resize(165, 165)
        self.setWindowTitle("Menu Główne - KParser")
        start_btn = QTw.QPushButton("Zacznij wyszukiwanie", self)
        filter_btn = QTw.QPushButton("Oczyszczenie ze śmieci", self)
        settings_btn = QTw.QPushButton("Ustawienia", self)
        label = QTw.QLabel(self)
        label.setPixmap(self.pixmap)
        self.layout_VBox.addWidget(label)
        self.layout_VBox.addWidget(start_btn, 0)
        self.layout_VBox.addWidget(filter_btn, 1)
        self.layout_VBox.addWidget(settings_btn, 2)
        self.widget.setLayout(self.layout_VBox)
        self.widget.setFixedWidth(165)
        self.widget.setFixedHeight(165)
        start_btn.clicked.connect(lambda: self.start(mode=cr.cache["start_mode"]))
        filter_btn.clicked.connect(self.filter)
        settings_btn.clicked.connect(self.settings)
        start_btn.setFixedWidth(150)
        filter_btn.setFixedWidth(150)
        settings_btn.setFixedWidth(150)
        self.show()
        if mode == 1:
            self.settings()

    @pyqtSlot()
    def start(self, mode=0):
        self.clear_layout([self.layout_VBox, self.layout_HBox, self.layout_HBox_2])
        self.resize(280, 120)
        self.setWindowTitle("KParser")
        self.tmp["path"] = "email/"
        start_btn = QTw.QPushButton("Rozpocznij wyszukiwanie", self)
        start_btn.setEnabled(False)
        back_btn = QTw.QPushButton("Wróć", self)
        if mode == 0:
            self.layout_VBox = QTw.QVBoxLayout(self)
            self.layout_HBox = QTw.QHBoxLayout(self)
            self.layout_HBox_2 = QTw.QHBoxLayout(self)
            cr.cache["start_mode"] = 1
        url_line = QTw.QLineEdit(self)
        url_line.setPlaceholderText("Wpisz szukaną frazę lub adres strony")
        url_line.setObjectName("text")
        queries_number_line = QTw.QLineEdit(str(cr.cache["queries_number"]), self)
        queries_number_line.setObjectName("query_number")
        self.tmp["query_number"] = cr.cache["queries_number"]
        path_line = QTw.QLineEdit("email/", self)
        path_line.setObjectName("path")
        search_type_radio_btn_1 = QTw.QRadioButton("Fraza do Google'a", self)
        search_type_radio_btn_1.setObjectName("radio_1")
        search_type_radio_btn_2 = QTw.QRadioButton("Konkretna strona", self)
        search_type_radio_btn_2.setObjectName("radio_2")
        self.tmp["search_type"] = "phrase"
        search_type_radio_btn_1.setChecked(True)
        self.layout_VBox.addWidget(url_line, 0)
        self.layout_HBox.addWidget(search_type_radio_btn_1, 0)
        self.layout_HBox.addWidget(search_type_radio_btn_2, 1)
        self.layout_HBox_2.addWidget(start_btn, 0)
        self.layout_HBox_2.addWidget(back_btn, 1)
        self.layout_VBox.addLayout(self.layout_HBox)
        self.layout_VBox.addWidget(QTw.QLabel("Liczba wyników do przeszukania", self), 2)
        self.layout_VBox.addWidget(queries_number_line, 3)
        self.layout_VBox.addWidget(QTw.QLabel("Katalog zapisu"), 4)
        self.layout_VBox.addWidget(path_line, 5)
        self.layout_VBox.addLayout(self.layout_HBox_2, 6)
        self.widget.setLayout(self.layout_VBox)
        self.widget.setFixedWidth(400)
        self.widget.setFixedHeight(120)
        self.widget.move(40, 0)

        def values_change():
            sending_button = self.sender()
            par_id = sending_button.objectName()
            if par_id == "radio_1":
                self.tmp["search_type"] = "phrase"
            elif par_id == "radio_2":
                self.tmp["search_type"] = "url"
            else:
                if par_id == "text":
                    self.tmp["query"] = sending_button.text()
                elif par_id == "query_number":
                    val = sending_button.text()
                    try:
                        val = int(val)
                        self.tmp[par_id] = val
                    except ValueError:
                        self.tmp[par_id] = 0
                        if val != "":
                            self.message_warning("Nieprawidłowy typ danych: Dozwolone są liczby całkowite")
                else:
                    self.tmp[par_id] = sending_button.text()
            values = list(self.tmp.values())
            if not values.count("") and self.tmp["query_number"] != 0:
                start_btn.setEnabled(True)
            else:
                start_btn.setEnabled(False)

        url_line.textChanged.connect(values_change)
        queries_number_line.textChanged.connect(values_change)
        path_line.textChanged.connect(values_change)
        start_btn.clicked.connect(self.search_start)
        back_btn.clicked.connect(self.main_menu)
        self.show()

    @pyqtSlot()
    def search_start(self):
        cr.cache["search_id"] += 1
        cr.cache["cho"] = self.tmp["path"]
        makedirs("emaile/{}".format(cr.cache["cho"]), exist_ok=True)
        if self.tmp["search_type"] == "phrase":
            process = Process(name="search_process", target=search.SearchProcess,
                              args=(cr.cache["search_id"], self.tmp["query"], self.tmp["query_number"]))
        else:
            process = Process(name="search_process", target=search.SearchProcess,
                              args=(cr.cache["search_id"], self.tmp["query"]))
        process.start()

    @pyqtSlot()
    def filter(self):
        pass

    @pyqtSlot()
    def settings(self):
        self.clear_layout([self.layout_VBox, self.layout_HBox, self.layout_HBox_2])
        self.resize(165, 310)
        self.setWindowTitle("Ustawienia - KParser")
        confirm_btn = QTw.QPushButton("Zastosuj", self)
        confirm_btn.setEnabled(False)

        def settings_change():
            sending_button = self.sender()
            par_id = sending_button.objectName()
            if par_id == "check_registry":
                self.tmp[par_id] = sending_button.isChecked()
            elif par_id == "queries_number" or par_id == "pause":
                val = sending_button.text()
                try:
                    val = int(val)
                    self.tmp[par_id] = val
                except ValueError:
                    if val != "":
                        self.message_warning("Nieprawidłowy typ danych: Dozwolone są liczby całkowite")
            else:
                self.tmp[par_id] = sending_button.currentIndex()
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
        if self.tmp:
            keys = self.tmp.keys()
            values = self.tmp.values()
            for parameter in keys:
                for value in values:
                    if parameter == "search_lang":
                        value = search_lang[value]
                    elif parameter == "search_type":
                        value = search_type[value]
                    sett.change_parameter(parameter, value)
                    break
        self.tmp = {}
        self.settings()

    @staticmethod
    def clear_layout(layouts: list):
        for layout in layouts:
            try:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            except TypeError:
                pass

    def message_question(self, text):
        answer = QTw.QMessageBox.question(
            self, "Komunikat", text,
            QTw.QMessageBox.Yes | QTw.QMessageBox.No)

        if answer == QTw.QMessageBox.Yes:
            return "Yes"
        else:
            return "No"

    def message_warning(self, text: str):
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
