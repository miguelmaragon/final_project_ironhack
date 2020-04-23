import argparse
import pandas as pd
from module import api_configuration


def main(current_location, bank_card, route_mode):
    print('\n--- WELCOME TO FREE FEE ATM LOCATION ---\n')
    print('  The process is looking for ATM near these address:\n    '
          + current_location.title()
          + '\n\n  And for the cards: \n    '
          + str(bank_card))
    lat, lng, lat_current, lng_current = api_configuration.lat_lng_current_location(current_location)
    data_api = api_configuration.find_atms(lat, lng)
    commissions = pd.read_excel("./data/raw/comisiones_bancos.xlsx")
    dict_results, location_atm_free, location_atm_near = api_configuration.processing(data_api, commissions, bank_card)
    api_configuration.show_in_the_map(dict_results, location_atm_free, location_atm_near, lat_current, lng_current,
                                      route_mode)
    print('\n--- THANKS FOR FREE FEE ATM LOCATION ---\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--current_location", help="Please enter an address", dest='current_location',
                        default='Avenida Luis Aragones, 4, 28022, Madrid')
    parser.add_argument("-c", "--bank_card", help="Enter your card's bank", dest='bank_card',
                        default='santander')
    parser.add_argument("-m", "--route_mode", help="Enter the mode of transport", dest='route_mode',
                        default='driving')
    args = parser.parse_args()
    current_location = args.current_location
    try:
        bank_card = eval(args.bank_card.upper())
    except:
        bank_card = args.bank_card.upper()
    route_mode = args.route_mode
    main(current_location, bank_card, route_mode)
