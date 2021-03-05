import os
import json
import time
import requests
import urllib3
from googlesearch import search
from bs4 import BeautifulSoup
from .core import io_functions as io_f

# Klasa, która jest uruchamiana w osobnym procesie z pomocą multiprocessing
class SearchProcess:
    def __init__(self, search_id, query=None, queries_number=None, url=None):
        self.id = search_id
        self.query = query
        self.queries_number = int(queries_number)
        self.url = url
        self.cache = self.cache_update()
        self.urls = []
        self.emails = []
        self.registry_db = []
        self.search()

    @staticmethod
    def cache_update():
        with open("data/tmp/curr_session_cache.json", "r") as f:
            cache = json.load(f)

        return cache

    def search(self):
        if self.url is None:
            for result in search(self.query,
                                 tld="pl",
                                 lang=self.cache["search_lang"],
                                 stop=self.queries_number,
                                 pause=self.cache["pause"]):
                self.urls.append(str(result))
        else:
            self.urls.append(self.url)
        self.parser()

    def parser(self):
        # Wyszukiwanie adresów email na poszczególnych stronach internetowych
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        while self.urls:
            url = self.urls.pop(0)
            r = requests.get(url, headers={"User-Agent": self.cache["user_agent"]}, verify=False)
            soup = BeautifulSoup(r.text, "lxml")
            links = soup.find_all("a")
            links_2 = soup.find_all("b")
            if links_2:
                links.extend(links_2)
            for link in links:
                result = str(link.get("href"))
                if result.count("@") == 1:
                    self.save(result)
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
        if self.cache["OS"] == "linux":
            data = time.strftime("%d.%m.%Y %H:%M")
        else:
            data = time.strftime("%d.%m.%Y %HH %MM")
        if "new_dir" in self.cache.keys():
            io_f.dir_db_save()
        f = open("emaile/{}/email {}.txt".format(self.cache["cho"], data), "a")
        self.registry_read()
        for email in self.emails:
            if email.count("@"):
                if email.count("\\"):
                    index = int(email.index("\\"))
                    email_e = email[0:index]
                    if email_e in self.registry_db and self.cache["check_registry"] is True:
                        pass
                    else:
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
                    if email in self.registry_db and self.cache["check_registry"] is True:
                        pass
                    else:
                        f.write("{} \n".format(email))
            else:
                pass
        f.close()
        self.registry_save(self.emails)

        while io_f.dirlist:
            del io_f.dirlist[0]

        # Koniec zadania
        os.makedirs("data/tmp", exist_ok=True)
        if not os.path.exists("data/tmp/curr_session.json"):
            with open("data/tmp/curr_session.json", "a") as f:
                json.dump({self.query: str(self.id)}, f, indent=4)
        else:
            session_dict = {}
            try:
                with open("data/tmp/curr_session.json", "r") as f:
                    session_dict = json.load(f)
                    session_dict[self.query] = str(self.id)
            except json.decoder.JSONDecodeError:
                pass
            with open("data/tmp/curr_session.json", "w+") as f:
                if session_dict:
                    json.dump(session_dict, f, indent=4)
                else:
                    json.dump({self.query: str(self.id)}, f, indent=4)

        # TODO: Uproszczenie kodu poprzez dzielenie pamięci z procesem KParser_cli

    def registry_read(self):
        registry = open("data/config/registry.txt", "r")
        for email in registry:
            n = email.index("\n")
            email_n = email[0:n - 1]
            self.registry_db.append(email_n)
        registry.close()

    def registry_save(self, entries):
        registry = open("data/config/registry.txt", "r+")
        for email in entries:
            if email in self.registry_db:
                pass
            else:
                position = entries.index(email)
                registry.write("{} \n".format(entries[position]))
        registry.close()

# TODO: Nowy sposób zapisu plików z podziałem na poszczególne strony i znalezione na nich e-maile + numery telefonów
