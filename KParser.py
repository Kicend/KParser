import requests
import sys
import os
import shutil
import time
import urllib3
from bs4 import BeautifulSoup
from googlesearch import search
from data.modules.search.emails import save
from data.modules.search.emails import file
from data.modules.filtr import menu_dir
from data.modules import core as cr

urls = []
dirlist = []

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
            WERSJA 0.4 stworzona przez F.Kicend\n"""
          )

    while True:
        decision = int(input("1 - Wyszukiwanie adresy email na podstawie zadanej frazy w Google\n"
                             "2 - Przefiltrowanie danych w pliku email.txt z niepotrzebnych śmieci\n"
                             "3 - Ustawienia KParser\n"))

        if decision == 1 or decision == 2 or decision == 3:
            other_modules(decision)
            break

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

def parser():
    # Parametry szukajki
    query = input("Wpisz zapytanie do wyszukiwarki\n")
    queries_number = int(input("Wpisz ilość zapytań\n"))

    for result in search(query,
                         tld="pl",
                         lang=cr.cache["search_lang"],
                         stop=queries_number,
                         pause=5):

        urls.append(str(result))
        print("Dodano adres\n{}".format(result))

    # Parametry parsera
    # url = input("Podaj adres url")

    # Wyszukiwanie adresów email na poszczególnych stronach internetowych
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    while urls:
        url = urls.pop(0)
        r = requests.get(url, headers={"user-agent": "macOS"}, verify=False)
        soup = BeautifulSoup(r.text, "lxml")
        links = soup.find_all("a")
        links_2 = soup.find_all("b")
        if links_2:
            links.extend(links_2)
        for link in links:
            email = str(link.get("href"))
            if email.count("@") == 1:
                save(email)

    file()
    back_to_menu()

def other_modules(decision):
    if decision == 1:
        parser()
    if decision == 2:
        menu_dir()
        back_to_menu()
    if decision == 3:
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
