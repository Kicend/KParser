import os
import time

emails = []
dirlist = []
registry_db = []
tmp = {}

# Komunikaty
odmowa = "To nie jest adres email. Odmowa zapisu"

def save(email):
    if email.count(":"):
        symbol_index = None
        if email.count(";"):
            symbol_index = int(email.index(";"))
        symbol_index_1 = int(email.index(":"))
        if symbol_index_1 == 0:
            emails.append(email[1:])
        else:
            if symbol_index is not None:
                emails.append(email[symbol_index_1+1:symbol_index])
            else:
                emails.append(email[symbol_index_1+1:])

    if email.count("/"):
        if email.count("www.google.com/maps"):
            print(odmowa)
        else:
            symbol_index = int(email.index("/"))
            if symbol_index == 0:
                emails.append(email[1:])
            else:
                emails.append(email[symbol_index+1:])

def dir_db_save():
    os.makedirs("config", exist_ok=True)
    dir_db = open("config/dir_db.txt", "a")
    dir_db.write("{} \n".format(tmp["new_dir"]))
    dir_db.close()

def dir_db_read():
    dir_db = open("config/dir_db.txt", "r")
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

def registry_read():
    registry = open("config/rejestr.txt", "r")
    for email in registry:
        n = email.index("\n")
        email_n = email[0:n-1]
        registry_db.append(email_n)
    registry.close()

def registry_save(list):
    registry = open("config/rejestr.txt", "r+")
    for email in list:
        if email in registry_db:
            print("INFORMACJA: Adres jest już w rejestrze")
        else:
            position = emails.index(email)
            registry.write("{} \n".format(emails[position]))
    registry.close()

def file():
    try:
        dir_db_read()
    except FileNotFoundError:
        print("Plik konfiguracji nie istnieje")
    os.makedirs("emaile", exist_ok=True)
    print("Katalog został utworzony")
    files_list = list(os.listdir("emaile"))
    if files_list == [] and dirlist == []:
        new_directory()
    else:
        decision = int(input("Co chcesz zrobić? \n 1 - Wybrać nazwę folderu z zapisanych \n 2 - Utworzyć nowy \n"))
        if decision == 1:
            cho_dir()
        else:
            new_directory()

    data = time.strftime("%H:%M %d.%m.%Y")
    if "new_dir" in tmp.keys():
        dir_db_save()
    f = open("emaile/{}/email {}.txt".format(tmp["cho"], data), "a")
    print("Plik zapisu w trakcie tworzenia...")
    registry_read()
    for email in emails:
        if email.count("@"):
            if email.count("\\"):
                g = int(email.index("\\"))
                email_e = email[0:g]
                f.write("{} \n".format(email_e))
            if email.count("www.google.com/maps"):
                print(odmowa)
            if email.count("www.google.pl/maps"):
                print(odmowa)
            if email.count("facebook"):
                print(odmowa)
            if email.count("&"):
                print(odmowa)
            else:
                if email in registry_db:
                    print("INFORMACJA: Adres jest już w rejestrze")
                else:
                    f.write("{} \n".format(email))
        else:
            print(odmowa)
    f.close()
    registry_save(emails)
    print("Plik został pomyślnie utworzony")

    while dirlist:
        del dirlist[0]
    print("Pamięć podręczna została wyczyszczona")

# TODO: Stworzenie klasy, w której skład wejdą funkcję odpowiadające za operacje na plikach
# TODO: Nowy sposób zapisu plików z podziałem na poszczególne strony i znalezione na nich e-maile + numery telefonów
