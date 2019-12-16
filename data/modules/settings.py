import json
from .core import core as cr

# Komunikaty
change_parameter_successful = "Parametr pomyślnie zmieniony!"

# Funkcja odpowiedzialna za zmianę i zapis parametru do pliku konfiguracyjnego
def change_parameter(parameter: str, value):
    try:
        with open("data/config/config.json", "w") as f:
            cr.cache[parameter] = value
            config_tmp = cr.cache
            json.dump(config_tmp, f, indent=4)
    except FileNotFoundError:
        cr.config_fix(0)

# Szczegółowe ustawienia programu znajdują się w tej funkcji
def configuration():
    def except_value(setting, value_type: str, is_return: bool):
        if value_type == "int":
            print("Nieprawidłowa wartość parametru!\n"
                  "Prawidłową wartością jest liczba całkowita!")
        elif value_type == "str":
            print("Nieprawidłowa wartość parametru!\n"
                  "Prawidłową wartością jest napis!")
        while True:
            print("Obecna wartość: {} = {}\n".format(setting, config[setting]))
            try:
                value_2 = int(input("Jaką wartość chcesz wprowadzić?\n"))
                if not is_return:
                    change_parameter(setting, value_2)
                    print(change_parameter_successful)
                    break
                else:
                    return value_2
            except ValueError:
                print("Nieprawidłowa wartość!")

    decisions = (1, 2, 3, 4, 5, 6, 7)
    search_lang = {"polski": "pl",
                   "angielski": "en",
                   "niemiecki": "de",
                   "francuski": "fr",
                   "czeski": "cs",
                   "słowacki": "sk"
                   }

    with open("data/config/config.json", "r") as f:
        config = json.load(f)
    number = 1
    keys = list(config.keys())
    for parameter, value in config.items():
        print("{}. {} = {}".format(number, parameter, value))
        number += 1
        if number == 7:
            break
    while True:
        decision = int(input("7. Powrót do menu głównego\n"
                             "Wybierz ustawienie wpisując odpowiedni numer\n"))
        if decision in decisions and decision <= 6:
            parameter = keys[decision-1]
            if parameter == "check_require":
                if config[parameter]:
                    print("Obecna wartość to: {} = Tak\n"
                          "Jaką wartość chcesz wprowadzić?".format(parameter))
                else:
                    print("Obecna wartość to: {} = Nie\n"
                          "Jaką wartość chcesz wprowadzić?".format(parameter))
            else:
                print("Obecna wartość to: {} = {}\n"
                      "Jaką wartość chcesz wprowadzić?".format(parameter, config[parameter]))
            if decision == 3:
                while True:
                    for number, lang in enumerate(search_lang.keys()):
                        print("{} - {}".format(number+1, lang))
                    try:
                        choose_lang = int(input("Który język wyszukiwania wybierasz?\n"))
                        if 6 >= choose_lang >= 0:
                            lang_list = list(search_lang.values())
                            lang = lang_list[choose_lang-1]
                            change_parameter(parameter, lang)
                            print(change_parameter_successful)
                            break
                        else:
                            print("Nieprawidłowa wartość!")
                    except ValueError:
                        choose_lang = except_value(parameter, "int", True)
                        if 6 >= choose_lang >= 0:
                            lang_list = list(search_lang.values())
                            lang = lang_list[choose_lang-1]
                            change_parameter(parameter, lang)
                            print(change_parameter_successful)
                            break
                        else:
                            print("Nieprawidłowa wartość!")
            elif decision == 2 or decision == 4:
                try:
                    value = int(input())
                    change_parameter(parameter, value)
                    print(change_parameter_successful)
                except ValueError:
                    except_value(parameter, "int", False)
            elif decision == 1 or decision == 5 or decision == 6:
                if parameter == "check_registry":
                    while True:
                        try:
                            value = int(input("1 - Tak\n"
                                              "2 - Nie\n"))
                            if value == 1:
                                change_parameter(parameter, True)
                                print(change_parameter_successful)
                                break
                            elif value == 2:
                                change_parameter(parameter, False)
                                print(change_parameter_successful)
                                break
                            else:
                                print("Nieprawidłowa wartość!")
                        except ValueError:
                            value = except_value(parameter, "int", True)
                            if value == 1:
                                change_parameter(parameter, True)
                                print(change_parameter_successful)
                                break
                            elif value == 2:
                                change_parameter(parameter, False)
                                print(change_parameter_successful)
                                break
                            else:
                                print("Nieprawidłowa wartość!")
                elif parameter == "search_type":
                    while True:
                        try:
                            value = int(input("Wyszukiwanie\n"
                                              "1 - Podstawowe (tylko emaile)\n"
                                              "2 - Rozszerzone (emaile + nr telefonów)\n"))
                            if value == 1:
                                change_parameter(parameter, "basic")
                                print(change_parameter_successful)
                                break
                            elif value == 2:
                                change_parameter(parameter, "ext")
                                print(change_parameter_successful)
                                break
                            else:
                                print("Nieprawidłowa wartość!")
                        except ValueError:
                            value = except_value(parameter, "int", True)
                            if value == 1:
                                change_parameter(parameter, "basic")
                                print(change_parameter_successful)
                                break
                            elif value == 2:
                                change_parameter(parameter, "ext")
                                print(change_parameter_successful)
                                break
                            else:
                                print("Nieprawidłowa wartość!")
                elif parameter == "user_agent":
                    while True:
                        value = input("Jako jaki system ma się przedstawiać ten program podczas wyszukiwania?\n")
                        if len(value) <= 15:
                            change_parameter(parameter, value)
                            print(change_parameter_successful)
                            break
                        else:
                            print("Nazwa za długa! Maksymalna długość to 15 znaków!")
        else:
            break

# TODO: USER-AGENT brany z pliku z predefiniowanymi UA
