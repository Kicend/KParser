import os

cho_dir = []
cho_file = []

def menu_dir():
    number = 0
    listdir = os.listdir("emaile")
    for number, dir in enumerate(listdir):
        print("{} - {}".format(number, dir))
    choose = int(input("Wybierz folder\n"))
    cho_dir.append(listdir[choose])

    listdir = os.listdir("emaile/{}".format(cho_dir[0]))
    for number, file in enumerate(listdir):
        print("{} - {}".format(number, file))
    print("{} - Powrót do wyboru folderów".format(number+1))
    choose = int(input("Wybierz plik, który chcesz przefiltrować\n"))
    if choose == number+1:
        menu_dir()
    else:
        cho_file.append(listdir[choose])

def email_filter():
    menu_dir()
    file = open("emaile/{}/{}".format(cho_dir[0], cho_file[0]), "r+").readlines()
    file_filter = open("emaile/{}/email_filtr {}".format(cho_dir.pop(0), cho_file.pop(0)), "w+")
    tmp_db = []

    for phrase in file:
        tmp_db.append(phrase)

    while tmp_db:
        current = tmp_db.pop(0)
        if current.count("//" or "facebook.com" or "google.com" or "google.pl"):
            print("To nie jest adres email")
        else:
            file_filter.write("{} \n".format(current))

    print("Filtracja zakończona pomyślnie!")
    file_filter.close()
