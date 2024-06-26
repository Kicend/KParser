import json
import os

default_config = {
    "check_registry": True,
    "queries_number": 10,
    "search_lang": "pl",
    "pause": 5,
    "search_type": "ext",
    "first_config": True
}

keys_id = {
    0: "check_registry",
    1: "queries_number",
    2: "search_lang",
    3: "pause",
    4: "search_type",
    5: "first_config"
}

cache = {}
language_strings = {}

# Uaktualnienie zawartości pamięci podręcznej pobierając dane z pliku config.json
def cache_update():
    with open("data/config/config.json", "r") as f:
        dict_tmp = json.load(f)
    return dict_tmp

def load_cache_file():
    with open("data/tmp/curr_session_cache.json", "r") as f:
        data = json.load(f)
    return data

def update_cache_file(new_data: dict):
    with open("data/tmp/curr_session_cache.json", "r") as f:
        data = json.load(f)
        new_cache = data | new_data
    with open("data/tmp/curr_session_cache.json", "w") as f:
        json.dump(new_cache, f, indent=4)

# Funkcja mająca za zadanie naprawę pliku konfiguracyjnego
def config_fix(state: int, mist_list=None, config=None):
    if state == 0:
        with open("data/config/config.json", "w") as f:
            json.dump(default_config, f, indent=4)
    elif state == 1:
        for mistake_id in mist_list:
            config[keys_id[mistake_id]] = default_config[keys_id[mistake_id]]
        with open("data/config/config.json", "w") as f:
            json.dump(config, f, indent=4)

# Funkcja sprawdzająca program przed uruchomieniem menu głównego
def startup():
    os.makedirs("data/tmp", exist_ok=True)
    if os.path.isfile("data/tmp/curr_session.json"):
        os.remove("data/tmp/curr_session.json")
    try:
        config_correct_types = (bool, int, str, int, str, bool)
        with open("data/config/config.json", "r") as f:
            config = json.load(f)
            # Sprawdzanie typów wartości w pliku konfiguracyjnym
            config_mistakes_list = []
            for number, value in enumerate(config.values()):
                if type(value) != config_correct_types[number]:
                    config_mistakes_list.append(number)
            if default_config.keys() != config.keys() or config_mistakes_list:
                choose = input("BŁĄD: Plik konfiguracji może być uszkodzony!\n"
                               "Czy chcesz, aby została przeprowadzona naprawa? (t/n)\n")
                while True:
                    if choose == "t":
                        if default_config.keys() != config.keys():
                            config_fix(0)
                        else:
                            config_fix(1, config_mistakes_list, config)
                        print("Plik konfiguracji został pomyślnie naprawiony!")
                        break
                    elif choose == "n":
                        break

    except FileNotFoundError:
        os.makedirs("data/config", exist_ok=True)
        with open("data/config/config.json", "a+") as config:
            json.dump(default_config, config, indent=4)
