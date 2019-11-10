import json

default_config = {
    "check_registry": True,
    "queries_number": 10,
    "tlds": ["pl", "com.pl"],
    "search_lang": "pl",
    "pause": 5,
    "user_agent": "macOS",
    "search_type": "fast",
    "first_config": True
}

cache = {}

def cache_update():
    with open("config/config.json", "r") as f:
        dict_tmp = json.load(f)
    return dict_tmp

def change_parameter(parameter: str, value):
    try:
        with open("config/config.json", "w") as f:
            cache[parameter] = value
            json.dump(cache, f, indent=4)
    except FileNotFoundError:
        config_fix(0)

def config_fix(state: int):
    if state == 0:
        with open("config/config.json", "w") as f:
            json.dump(default_config, f, indent=4)

def startup():
    try:
        with open("config/config.json", "r") as f:
            config = json.load(f)
            config_keys = config.keys()
            if default_config.keys() == config_keys:
                pass
            else:
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
        with open("config/config.json", "a+") as config:
            json.dump(default_config, config, indent=4)

def configuration():
    with open("config/config.json", "r") as f:
        config = json.load(f)
    number = 1
    for parameter, value in config.items():
        print("{}. {} = {}".format(number, parameter, value))
        number += 1
