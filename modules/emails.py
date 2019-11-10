import os
import time

emails = []
dirlist = []
dirlist_f = []
dirlist_save = []
cho = []
registry_db_email = []
registry_tmp = []

# Komunikaty
odmowa = "To nie jest adres email. Odmowa zapisu"

def save(email):
    print(emails)
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

def dir_db_save(list):
    os.makedirs("config", exist_ok=True)
    dir_db = open("config/dir_db.txt", "a")
    while list:
        dir_db.write("{} \n".format(list.pop(0)))
    dir_db.close()

def dir_db_read():
    dir_db = open("config/dir_db.txt", "r")
    for dir in dir_db:
        dirlist.append(dir)
    dir_db.close()

def new_directory():
    dir_name = input("Jak chcesz nazwać nowy folder? \n")
    dirlist_save.append(dir_name)
    cho.append(dir_name)
    os.makedirs("emaile/{}".format(dir_name), exist_ok=True)

def cho_dir():
    number = 0
    for number, folder in enumerate(dirlist_f):
        print("{} - {}".format(number, folder))
    print("{} - Wróć do tworzenia nowego folderu".format(number+1))
    choose = int(input("Wybierz nazwę folderu \n"))
    if choose == number+1:
        new_directory()
    else:
        dirname = dirlist[choose]
        n = dirname.index("\n")
        cho.append(dirname[0:n-1])
        os.makedirs("emaile/{}".format(dirname[0:n-1]), exist_ok=True)

def registry_read():
    registry = open("config/rejestr.txt", "r")
    for email in registry:
        n = email.index("\n")
        email_n = email[0:n-1]
        registry_db_email.append(email_n)
    registry.close()

def registry_save(list):
    registry = open("config/rejestr.txt", "r+")
    for wpis in registry:
        n = wpis.index("\n")
        wpis_n = wpis[0:n-1]
        registry_tmp.append(wpis_n)
    for email in list:
        if registry_tmp.count(email) > 0:
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
    for dir in dirlist:
        if dir.count("\n"):
            n = dir.index("\n")
            dirlist_f.append(dir[0:n-1])
    os.makedirs("emaile", exist_ok=True)
    print("Katalog został utworzony")
    l = list(os.listdir("emaile"))
    if l == [] and dirlist == []:
        new_directory()
    else:
        decyzja = int(input("Co chcesz zrobić? \n 1 - Wybrać nazwę folderu z zapisanych \n 2 - Utworzyć nowy \n"))
        if decyzja == 1:
            try:
                cho_dir()
            except:
             print("BŁĄÐ: Lista folderów jest pusta")
        else:
            new_directory()

    data = time.strftime("%H:%M %d.%m.%Y")
    dir_db_save(dirlist_save)
    f = open("emaile/{}/email {}.txt".format(cho.pop(0), data), "a")
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
                if registry_db_email.count(email) > 0:
                    print("INFORMACJA: Adres jest już w rejestrze")
                else:
                    f.write("{} \n".format(email))
        else:
            print(odmowa)
    f.close()
    registry_save(emails)
    print("Plik został pomyślnie utworzony")

    while dirlist != [] and dirlist_f != []:
        del dirlist[0]
        del dirlist_f[0]
    print("Pamięć podręczna została wyczyszczona")

# TODO: Uproszczenie struktury, przede wszystkim zmniejszenie ilości list
# TODO: Stworzenie klasy, w której skład wejdą funkcję odpowiadające za operacje na plikach
# TODO: Nowy sposób zapisu plików z podziałem na poszczególne strony i znalezione na nich e-maile + numery telefonów
