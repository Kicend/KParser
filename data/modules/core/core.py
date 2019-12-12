import json
import os

default_config = {
    "check_registry": True,
    "queries_number": 10,
    "search_lang": "pl",
    "pause": 5,
    "user_agent": "macOS",
    "search_type": "ext",
    "first_config": True
}

cache = {}

# Uaktualnienie zawartości pamięci podręcznej pobierając dane z pliku config.json
def cache_update():
    with open("data/config/config.json", "r") as f:
        dict_tmp = json.load(f)
    return dict_tmp

# Funckja mająca za zadanie naprawę pliku konfiguracyjnego
def config_fix(state: int):
    if state == 0:
        with open("data/config/config.json", "w") as f:
            json.dump(default_config, f, indent=4)

# Funkcja sprawdzająca program przed uruchomieniem menu głównego
def startup():
    if os.path.isfile("data/tmp/curr_session.json"):
        os.remove("data/tmp/curr_session.json")
    try:
        with open("data/config/config.json", "r") as f:
            config = json.load(f)
            config_keys = config.keys()
            if default_config.keys() != config_keys:
                choose = input("BŁĄD: Plik konfiguracji może być uszkodzony!\n"
                               "Czy chcesz, aby została przeprowadzona naprawa? (t/n)\n")
                while True:
                    if choose == "t":
                        config_fix(0)
                        print("Plik konfiguracji został pomyślnie naprawiony!")
                        break
                    elif choose == "n":
                        break

    except FileNotFoundError:
        with open("data/config/config.json", "a+") as config:
            json.dump(default_config, config, indent=4)
