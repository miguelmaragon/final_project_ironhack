import argparse
import pandas as pd
from module import api_configuration


def main(current_location, bank_card):
    print('\n--- WELCOME TO FREE COMMISSION ATM LOCATION ---\n')
    print(current_location, bank_card)
    lat, lng, lat_current, lng_current = api_configuration.lat_lng_current_location(current_location)
    data_api = api_configuration.find_atms(lat, lng)
    commissions = pd.read_excel("./data//raw/comisiones_bancos.xlsx")
    dict_results, location_atm_free, location_atm_near = api_configuration.processing(data_api, commissions, bank_card)
    api_configuration.show_in_the_map(dict_results, location_atm_free, location_atm_near, lat_current, lng_current)
    print('\n--- THANKS FOR FREE COMMISSION ATM LOCATION ---\n')


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
