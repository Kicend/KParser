import os

def menu_dir():
    number = 0
    listdir = os.listdir("emaile")
    for number, dir in enumerate(listdir):
        print("{} - {}".format(number, dir))
    choose = int(input("Wybierz folder\n"))
    dir = listdir[choose]

    listdir = os.listdir("emaile/{}".format(dir))
    for number, file in enumerate(listdir):
        print("{} - {}".format(number, file))
    print("{} - Powrót do wyboru folderów".format(number+1))
    choose = int(input("Wybierz plik, który chcesz przefiltrować\n"))
    if choose == number+1:
        menu_dir()
    else:
        file = listdir[choose]
        email_filter(dir, file)

def email_filter(dir, filename):
    file = open("emaile/{}/{}".format(dir, filename), "r+").readlines()
    file_filter = open("emaile/{}/email_filtr {}".format(dir, filename), "w+")
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
