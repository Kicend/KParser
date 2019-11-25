import sys
import os
import shutil
import time
from multiprocessing import Process
from data.modules.search import SearchProcess
from data.modules.search import cho_dir
from data.modules.search import dir_db_read
from data.modules.search import new_directory
from data.modules.filtr import menu_dir
from data.modules import core as cr

dirlist = []
search_id = 0

def main_menu():
    print("""

    888    d8P  8888888b.                                            
    888   d8P   888   Y88b                                           
    888  d8P    888    888                                           
    888d88K     888   d88P 8888b.  888d888 .d8888b   .d88b.  888d888 
    8888888b    8888888P"     "88b 888P"   88K      d8P  Y8b 888P"   
    888  Y88b   888       .d888888 888     "Y8888b. 88888888 888     
    888   Y88b  888       888  888 888          X88 Y8b.     888     
    888    Y88b 888       "Y888888 888      88888P'  "Y8888  888     

                         \n
            WERSJA 0.5 stworzona przez F.Kicend\n"""
          )

    while True:
        decision = int(input("1 - Wyszukiwanie adresy email na podstawie zadanej frazy w Google\n"
                             "2 - Przefiltrowanie danych w pliku email.txt z niepotrzebnych śmieci\n"
                             "3 - Ustawienia KParser\n"))

        if decision == 1 or decision == 2 or decision == 3:
            other_modules(decision)
            break

def search_parameters(mode):
    def menu_cho_dir():
        try:
            dir_db_read()
        except FileNotFoundError:
            pass
        os.makedirs("emaile", exist_ok=True)
        print("Katalog został utworzony")
        files_list = list(os.listdir("emaile"))
        if files_list == [] and dirlist == []:
            new_directory()
        else:
            decision = int(input("Co chcesz zrobić?\n 1 - Wybrać nazwę folderu z zapisanych\n 2 - Utworzyć nowy\n"))
            if decision == 1:
                cho_dir()
            else:
                new_directory()

    if mode == 1:
        # Parametry szukajki
        queries_number = cr.cache["queries_number"]
        query = input("Wpisz zapytanie do wyszukiwarki: ")
        queries_number = int(input("Wpisz ilość zapytań [{}]: ".format(queries_number))
                             or queries_number)
        menu_cho_dir()
        process = Process(name="search_process", target=SearchProcess,
                          args=(search_id+1, query, queries_number))
        process.start()

    else:
        while True:
            url = input("Podaj adres url: ")
            if url.count("http") or url.count("https"):
                menu_cho_dir()
                process = Process(name="search_process", target=SearchProcess,
                                  args=(search_id+1, url))
                process.start()
                break
            else:
                print("To nie jest adres URL!")

    main_menu()

def settings():
    decision = int(input("Co chcesz zrobić?\n1 - Usunąć zapisane nazwy folderów\n"
                         "2 - Usunąć cały plik z zapisanymi folderami\n"
                         "3 - Usunąć folder emaile\n"
                         "4 - Skonfigurować program\n"
                         "5 - Powrót do menu głównego\n"))
    if decision == 1:
        try:
            dir_db = open("data/config/dir_db.txt", "r")
            for dir in dir_db:
                if dir.count("\n"):
                    n = dir.index("\n")
                    dirlist.append(dir[0:n-1])
            for number, folder in enumerate(dirlist):
                print("{} - {}".format(number+1, folder))
            dir_db.close()
            while True:
                dirname = int(input("Który zapis chcesz usunąć?\n"))
                del dirlist[dirname-1]
                while dirlist:
                    dir_db = open("data/config/dir_db.txt", "w+")
                    dir_db.write("{} \n".format(dirlist.pop(0)))

                decision = int(input("Czy chcesz jeszcze coś usunąć?\n"
                                     "1 - Tak\n2 - Nie\n"))

                if decision == 2:
                    dir_db.close()
                    main_menu()
                    break
        except FileNotFoundError:
            print("BŁĄD: Plik nie istnieje")
            time.sleep(5)
            main_menu()

    elif decision == 2:
        try:
            os.remove("data/config/dir_db.txt")
            print("Plik został usunięty")
            time.sleep(5)
            main_menu()
        except FileNotFoundError:
            print("BŁĄÐ: Plik nie istnieje")
            time.sleep(5)
            main_menu()

    elif decision == 3:
        try:
            shutil.rmtree("emaile")
            print("Folder został usunięty")
            time.sleep(5)
            main_menu()
        except FileNotFoundError:
            print("BŁĄÐ: Folder nie istnieje")
            time.sleep(5)
            main_menu()

    elif decision == 4:
        cr.configuration()
        cr.cache_update()
        main_menu()
    else:
        main_menu()

def other_modules(decision):
    if decision == 1:
        while True:
            try:
                mode = int(input("Gdzie chcesz wyszukiwać?\n"
                                 "1 - Ze stron na podstawie frazy w wyszukiwarce Google\n"
                                 "2 - Z konkretnej strony na podstawie adresu URL\n"))
                if mode == 1 or mode == 2:
                    break
            except ValueError:
                print("Nieprawidłowa wartość!")
        search_parameters(mode)
    elif decision == 2:
        menu_dir()
        back_to_menu()
    elif decision == 3:
        settings()

def back_to_menu():
    decision = int(input("1 - Wróć do menu głównego\n2 - Zakończ program\n"))
    if decision == 1:
        main_menu()
    else:
        sys.exit(0)

cr.startup()
cr.cache = dict(cr.cache_update())
cr.cache["OS"] = sys.platform
if cr.cache["first_config"]:
    while True:
        choose = input("Czy chcesz wstępnie skonfigurować program KParser? (t/n)\n")
        if choose == "t":
            cr.configuration()
            cr.change_parameter("first_config", False)
            break
        elif choose == "n":
            cr.change_parameter("first_config", False)
            break
main_menu()

# TODO: Wprowadzenie asynchroniczności i wielowątkowości
# TODO: Funkcja wyszukiwania numerów telefonu
# TODO: GUI
