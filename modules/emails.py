import os, time

emails = []
d = []
dirlist = []
dirlist_f = []
dirlist_save = []
cho = []
rejestr_db_email = []
rejestr_tmp = []

# Komunikaty
odmowa = "To nie jest adres email. Odmowa zapisu"

def save_1(email):
    print(emails)
    if email.count(":"):
        if email.count(";"):
            c = int(email.index(";"))
            d.append(c)
        b = int(email.index(":"))
        if b == 0:
            emails.append(email[1:])
        else:
            if d != []:
                e = d.pop(0)
                emails.append(email[b+1:e])
            else:
                emails.append(email[b+1:])

    if email.count("/"):
        if email.count("www.google.com/maps"):
            print(odmowa)
        else:
            b = int(email.index("/"))
            if b == 0:
                emails.append(email[1:])
            else:
                emails.append(email[b+1:])

def save_2(email_2):
    if email_2.count(":"):
        if email_2.count(";"):
            c = int(email_2.index(";"))
            d.append(c)
        b = int(email_2.index(":"))
        if b == 0:
            emails.append(email_2[1:])
        else:
            if d != []:
                e = d.pop(0)
                emails.append(email_2[b+1:e])
            else:
                emails.append(email_2[b+1:])

    if email_2.count("/"):
        if email_2.count("www.google.com/maps"):
            print(odmowa)
        else:
            b = int(email_2.index("/"))
            if b == 0:
                emails.append(email_2[1:])
            else:
                emails.append(email_2[b+1:])

def dir_db_save(list):
    os.makedirs("config", exist_ok=True)
    dir_db = open("config/dir_db.txt", "a")
    while list != []:
        dir_db.write("{} \n".format(list.pop(0)))
    dir_db.close()

def dir_db_read():
    dir_db = open("config/dir_db.txt", "r")
    for dir in dir_db:
        dirlist.append(dir)
    dir_db.close()

def new_directory():
    dirname = input("Jak chcesz nazwać nowy folder? \n")
    dirlist_save.append(dirname)
    cho.append(dirname)
    os.makedirs("emaile/{}".format(dirname), exist_ok=True)

def cho_dir():
    liczba = 0
    def g():
        global liczba
    for liczba, folder in enumerate(dirlist_f):
        print("{} - {}".format(liczba, folder))
    print("{} - Wróć do tworzenia nowego folderu".format(liczba+1))
    choose = int(input("Wybierz nazwę folderu \n"))
    if choose == liczba+1:
        new_directory()
    else:
        dirname = dirlist[choose]
        n = dirname.index("\n")
        cho.append(dirname[0:n-1])
        os.makedirs("emaile/{}".format(dirname[0:n-1]), exist_ok=True)

def rejestr_read():
    rejestr = open("config/rejestr.txt", "a+")
    rejestr_read = open("config/rejestr.txt", "r")
    for email in rejestr_read:
        n = email.index("\n")
        email_n = email[0:n-1]
        rejestr_db_email.append(email_n)
    rejestr.close()

def rejestr_save(list):
    rejestr = open("config/rejestr.txt", "r")
    rejestr_save = open("config/rejestr.txt", "a+")
    for wpis in rejestr:
        n = wpis.index("\n")
        wpis_n = wpis[0:n-1]
        rejestr_tmp.append(wpis_n)
    for email in list:
        if rejestr_tmp.count(email) > 0:
            print("INFORMACJA: Adres jest już w rejestrze")
        else:
            position = emails.index(email)
            rejestr_save.write("{} \n".format(emails[position]))
    rejestr_save.close()

def file():
    try:
        dir_db_read()
    except:
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
    rejestr_read()
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
                if rejestr_db_email.count(email) > 0:
                    print("INFORMACJA: Adres jest już w rejestrze")
                else:
                    f.write("{} \n".format(email))
        else:
            print(odmowa)
    f.close()
    rejestr_save(emails)
    print("Plik został pomyślnie utworzony")

    while dirlist != [] and dirlist_f != []:
        del dirlist[0]
        del dirlist_f[0]
    print("Pamięć podręczna została wyczyszczona")
