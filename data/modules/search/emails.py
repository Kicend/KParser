import os
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from data.modules import core as cr

dirlist = []
tmp = {}

class SearchProcess:
    def __init__(self, search_id, urls):
        self.id = search_id
        self.urls = urls
        self.emails = []
        self.registry_db = []
        self.parser()

    def parser(self):
        # Wyszukiwanie adresów email na poszczególnych stronach internetowych
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        while self.urls:
            url = self.urls.pop(0)
            r = requests.get(url, headers={"user-agent": cr.cache["user_agent"]}, verify=False)
            soup = BeautifulSoup(r.text, "lxml")
            links = soup.find_all("a")
            links_2 = soup.find_all("b")
            if links_2:
                links.extend(links_2)
            for link in links:
                email = str(link.get("href"))
                if email.count("@") == 1:
                    self.save(email)
        self.file()

    def save(self, email):
        if email.count(":"):
            symbol_index = None
            if email.count(";"):
                symbol_index = int(email.index(";"))
            symbol_index_1 = int(email.index(":"))
            if symbol_index_1 == 0:
                self.emails.append(email[1:])
            else:
                if symbol_index is not None:
                    self.emails.append(email[symbol_index_1+1:symbol_index])
                else:
                    self.emails.append(email[symbol_index_1+1:])

        if email.count("/"):
            if email.count("www.google.com/maps"):
                pass
            else:
                symbol_index = int(email.index("/"))
                if symbol_index == 0:
                    self.emails.append(email[1:])
                else:
                    self.emails.append(email[symbol_index+1:])

    def file(self):
        data = time.strftime("%H:%M %d.%m.%Y")
        if "new_dir" in tmp.keys():
            dir_db_save()
        f = open("emaile/{}/email {}.txt".format(tmp["cho"], data), "a")
        self.registry_read()
        for email in self.emails:
            if email.count("@"):
                if email.count("\\"):
                    g = int(email.index("\\"))
                    email_e = email[0:g]
                    f.write("{} \n".format(email_e))
                if email.count("www.google.com/maps"):
                    pass
                if email.count("www.google.pl/maps"):
                    pass
                if email.count("facebook"):
                    pass
                if email.count("&"):
                    pass
                else:
                    if email in self.registry_db and cr.cache["check_registry"] is True:
                        pass
                    else:
                        f.write("{} \n".format(email))
            else:
                pass
        f.close()
        self.registry_save(self.emails)

        while dirlist:
            del dirlist[0]
        # TODO: Zgłaszanie końca zadania

    def registry_read(self):
        registry = open("data/config/rejestr.txt", "r")
        for email in registry:
            n = email.index("\n")
            email_n = email[0:n - 1]
            self.registry_db.append(email_n)
        registry.close()

    def registry_save(self, list):
        registry = open("data/config/rejestr.txt", "r+")
        for email in list:
            if email in self.registry_db:
                pass
            else:
                position = list.index(email)
                registry.write("{} \n".format(list[position]))
        registry.close()

def dir_db_save():
    os.makedirs("config", exist_ok=True)
    dir_db = open("data/config/dir_db.txt", "a")
    dir_db.write("{} \n".format(tmp["new_dir"]))
    dir_db.close()

def dir_db_read():
    dir_db = open("data/config/dir_db.txt", "r")
    for dir in dir_db:
        dirlist.append(dir)
    dir_db.close()

def new_directory():
    dirname = input("Jak chcesz nazwać nowy folder? \n")
    tmp["new_dir"] = dirname
    tmp["cho"] = dirname
    os.makedirs("emaile/{}".format(dirname), exist_ok=True)

def cho_dir():
    number = 0
    if dirlist:
        for number, folder in enumerate(dirlist):
            n = folder.index("\n")
            folder_n = folder[0:n - 1]
            print("{} - {}".format(number, folder_n))
        print("{} - Wróć do tworzenia nowego folderu".format(number+1))
        choose = int(input("Wybierz nazwę folderu \n"))
        if choose == number+1:
            new_directory()
        else:
            dirname = dirlist[choose]
            n = dirname.index("\n")
            tmp["cho"] = dirname[0:n-1]
            os.makedirs("emaile/{}".format(dirname[0:n-1]), exist_ok=True)
    else:
        print("INFORMACJA: Lista folderów jest pusta!")
        new_directory()

# TODO: Stworzenie klasy, w której skład wejdą funkcję odpowiadające za operacje na plikach
# TODO: Nowy sposób zapisu plików z podziałem na poszczególne strony i znalezione na nich e-maile + numery telefonów
