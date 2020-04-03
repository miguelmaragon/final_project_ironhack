import argparse
import pandas as pd
from package import api_configuration


def main(current_location, bank_card):
    print('\n--- WELCOME TO THE ATM LOCATION FREE ---\n')
    print(current_location, bank_card)
    lat, lng = api_configuration.lat_lng_current_location(current_location)
    data_api = api_configuration.find_atms(lat, lng)
    comisions = pd.read_excel("./data//raw/comisiones_bancos.xlsx")
    dict_results = api_configuration.processing(data_api, comisions, bank_card)
    api_configuration.show_in_the_map(dict_results)
    print('\n--- THANKS FOR USE FORBES ---\n       HACK-REPORTING')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--current_location", help = "Introduzca una dirección", dest='current_location',
                        default='Calle Jacinto Benavente 14, Las Rozas, Madrid')
    parser.add_argument("-c", "--bank_card", help="Introduzca el Banco de su tarjeta", dest='bank_card',
                        default='santander')
    args = parser.parse_args()
    current_location = args.current_location
    bank_card = args.bank_card
    main(current_location, bank_card)
