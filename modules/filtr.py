import os

cho_dir = []
cho_file = []

def menu_dir():
    listdir = os.listdir("emaile")
    for liczba, dir in enumerate(listdir):
        print("{} - {}".format(liczba, dir))
    choose = int(input("Wybierz folder\n"))
    cho_dir.append(listdir[choose])

    listdir = os.listdir("emaile/{}".format(cho_dir[0]))
    for liczba, file in enumerate(listdir):
        print("{} - {}".format(liczba, file))
    print("{} - Powrót do wyboru folderów".format(liczba+1))
    choose = int(input("Wybierz plik, który chcesz przefiltrować\n"))
    if choose == liczba+1:
        menu_dir()
    else:
        cho_file.append(listdir[choose])

def filter():
    menu_dir()
    f = open("emaile/{}/{}".format(cho_dir[0], cho_file[0]), "r+").readlines()
    plik = open("emaile/{}/email_filtr {}".format(cho_dir.pop(0), cho_file.pop(0)), "w+")
    tmp_db = []

    for phrase in f:
        tmp_db.append(phrase)

    while tmp_db != []:
        current = tmp_db.pop(0)
        if current.count("//" or "facebook.com" or "google.com" or "google.pl"):
            print("To nie jest adres email")
        else:
            plik.write("{} \n".format(current))

    print("Filtracja zakończona pomyślnie")
    plik.close()

