import os
from data.modules.core import core as cr

dirlist = []

def dir_db_save():
    os.makedirs("data/config", exist_ok=True)
    dir_db = open("data/config/dir_db.txt", "a")
    dir_db.write("{} \n".format(cr.cache["new_dir"]))
    dir_db.close()

def dir_db_read():
    dir_db = open("data/config/dir_db.txt", "r")
    for dir in dir_db:
        if dir not in dirlist:
            dirlist.append(dir)
    dir_db.close()

def new_directory():
    dirname = input("Jak chcesz nazwać nowy folder? \n")
    cr.cache["new_dir"] = dirname
    cr.cache["cho"] = dirname
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
            cr.cache["cho"] = dirname[0:n-1]
            os.makedirs("emaile/{}".format(dirname[0:n-1]), exist_ok=True)
    else:
        print("INFORMACJA: Lista folderów jest pusta!")
        new_directory()
