import requests
import sys
import os
import shutil
import time
import urllib3
from bs4 import BeautifulSoup
from googlesearch import search
from modules.emails import save_1
from modules.emails import save_2
from modules.emails import file
from modules.filtr import filter

urls = []
dirlist = []

# Menu główne
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
        WERSJA 0.1 stworzona przez F.Kicend\n"""
      )

def Main_Menu():
    decyzja = int(input("Co chcesz zrobić?\n1 - Wyszukać adresy email na podstawie zadanej frazy w Google\n"
        "2 - Przefiltrować dane w pliku email.txt z niepotrzebnych śmieci\n"
        "3 - Ustawienia KParser\n"))
    other_modules(decyzja)

    if decyzja != 1 and decyzja != 2 and decyzja != 3:
        while True:
            decyzja = int(input("Nieprawidłowa wartość. Spróbuj jeszcze raz. Prawidłowe wartości to 1, 2 lub 3\n"
                                "1 - Wyszukiwanie adresy email na podstawie zadanej frazy w Google\n"
                                "2 - Przefiltrowanie danych w pliku email.txt z niepotrzebnych śmieci\n"
                                "3 - Ustawienia KParser\n"))
            if decyzja == 1 or decyzja == 2 or decyzja == 3:
                other_modules(decyzja)
                break

def settings():
    decyzja = int(input("Co chcesz zrobić?\n1 - Usunąć zapisane nazwy folderów\n"
                        "2 - Usunąć cały plik z zapisanymi folderami\n"
                        "3 - Usunąć folder emaile\n"
                        "4 - Powrót do menu głównego\n"))
    if decyzja == 1:
        try:
            dir_db = open("config/dir_db.txt", "r")
            for dir in dir_db:
                if dir.count("\n"):
                    n = dir.index("\n")
                    dirlist.append(dir[0:n-1])
            for liczba, folder in enumerate(dirlist):
                print("{} - {}".format(liczba+1, folder))
            dir_db.close()
            while True:
                choose = int(input("Który zapis chcesz usunąć?\n"))
                del dirlist[choose-1]
                while dirlist != []:
                    dir_db = open("config/dir_db.txt", "w+")
                    dir_db.write("{} \n".format(dirlist.pop(0)))

                decyzja = int(input("Czy chcesz jeszcze coś usunąć?\n"
                                    "1 - Tak\n2 - Nie\n"))

                if decyzja == 2:
                    dir_db.close()
                    Main_Menu()
                    break
        except:
            print("BŁĄD: Plik nie istnieje")
            time.sleep(5)
            Main_Menu()

    elif decyzja == 2:
        try:
            os.remove("config/dir_db.txt")
            print("Plik został usunięty")
            time.sleep(5)
            Main_Menu()
        except:
            print("BŁĄÐ: Plik nie istnieje")
            time.sleep(5)
            Main_Menu()

    elif decyzja == 3:
        try:
            shutil.rmtree("emaile")
            print("Folder został usunięty")
            time.sleep(5)
            Main_Menu()
        except:
            print("BŁĄÐ: Folder nie istnieje")
            time.sleep(5)
            Main_Menu()
    else:
        Main_Menu()

def parser():
    # Parametry szukajki
    query = input("Wpisz zapytanie do wyszukiwarki\n")
    queries_number = int(input("Wpisz ilość zapytań\n"))

    for result in search(query, tld="pl" and "com.pl", lang="pl", num=15, stop=queries_number, pause=5):

        urls.append(str(result))
        print("Dodano adres\n{}".format(result))

    # Parametry parsera
    # url = input("Podaj adres url")

    # Wyszukiwanie adresów email na poszczególnych stronach internetowych
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    while urls != []:
        url = urls.pop(0)
        r = requests.get(url, headers={"user-agent": "macOS"}, verify=False)
        soup = BeautifulSoup(r.text, "lxml")
        body = soup.body
        links = soup.find_all("a")
        links_2 = soup.find_all("b")
        for link in links:
            a = link.get("href")
            email = str(a)
            if email.count("@") == 1:
                save_1(email)
        for link_2 in links_2:
            b = link_2.get("b")
            email_2 = str(b)
            if email_2.count("@") == 2:
                save_2(email_2)

    file()
    back_to_menu()

def other_modules(decyzja):
    if decyzja == 1:
        parser()
    if decyzja == 2:
        filter()
        back_to_menu()
    if decyzja == 3:
        settings()

def back_to_menu():
    decyzja = int(input("1 - Wróć do menu głównego\n2 - Zakończ program\n"))
    if decyzja == 1:
        Main_Menu()
    else:
        sys.exit(0)

Main_Menu()
other_modules()

# TODO: Wprowadzenie asynchroniczności i wielowątkowości
# TODO: Funkcja wyszukiwania numerów telefonu
# TODO: Możliwość konfiguracji programu + zapis konfiguracji do pliku config.json
