import argparse
import json
from random import randint
from sys import platform
from data.modules.search import SearchProcess

cache = {}

def parser():
    kparser_parser = argparse.ArgumentParser(prog="KParser",
                                             usage="%(prog)s [OPTIONS] query",
                                             description="Program do pozyskiwania adresów email na stronach")
    kparser_parser.add_argument("query", type=str)
    """
    kparser_parser.add_argument("-m", "--mode", help="Określa czy wyszukiwanie ma odbywać się za pośrednictwiem "
                                                     "Google'a czy na konkretnej stronie internetowej\n"
                                                     "0 (domyślnie) - zapytanie do wyszukiwarki\n"
                                                     "1 - strona internetowa"
                                                     "(należy podać adres strony zamiast zapytania)\n")
    """
    kparser_parser.add_argument("-n", "--number", type=int, default=10,
                                help="Określa ilość zapytań do wyszukiwarki (domyślnie 10)")
    kparser_parser.add_argument("-l", "--language", type=str, default="pl",
                                help="Określa w jakim języku ma odbywać się przeszukiwanie "
                                     "(domyślnie pl)")
    args = kparser_parser.parse_args()

    cache["pause"] = 5
    cache["search_lang"] = args.language
    cache["cho"] = "test"
    cache["check_registry"] = True
    cache["OS"] = platform
    with open("data/tmp/curr_session_cache.json", "w") as csc:
        json.dump(cache, csc, indent=4)

    if args.query.count("http") or args.query.count("https"):
        SearchProcess(0, args.query, 1)
    else:
        SearchProcess(0, args.query, args.number)

if __name__ == "__main__":
    with open("data/UA.json", "r") as f:
        ua = json.load(f)
        cache["user_agent"] = ua[str(randint(0, 8))]
    parser()
