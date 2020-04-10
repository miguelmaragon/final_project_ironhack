from dotenv import load_dotenv
import googlemaps
import os
import requests
from module import column_conversion
from module import marker_template
from module import route_map
import gmaps
from ipywidgets import IntSlider
from ipywidgets.embed import embed_minimal_html
import pandas as pd

load_dotenv()
api_key_miguel = os.environ["api_key_number_2"]
gmaps.configure(api_key=api_key_miguel)


def lat_lng_current_location(current_location):
    gmaps_google = googlemaps.Client(key=api_key_miguel)
    geocode_result = gmaps_google.geocode(current_location)
    lat = str(geocode_result[0]['geometry']['location']['lat'])
    lng = str(geocode_result[0]['geometry']['location']['lng'])
    lat_current = geocode_result[0]['geometry']['location']['lat']
    lng_current = geocode_result[0]['geometry']['location']['lng']
    print(lat, lng)
    return lat, lng, lat_current, lng_current


def find_atms(lat, lng):
    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat + "," + lng + "&type=atm&language=es&rankby=distance&pagetoken&key=" + api_key_miguel
    # return response object
    r = requests.get(url)
    x = r.json()
    api_data = pd.json_normalize(x['results'])
    api_data_process = api_data[
        ['name', 'place_id', 'rating', 'types', 'vicinity', 'geometry.location.lat', 'geometry.location.lng',
         'opening_hours.open_now', 'icon']]
    api_data_process = api_data_process.copy()
    api_data_process['name_join'] = api_data_process.apply(lambda row: column_conversion.rename_f(row['name'].lower()), axis=1)
    api_data_process.to_csv('./data/processed/api_data_process.csv', index=False)
    return api_data_process


def processing(data_api, commissions, bank_card):
    if isinstance(bank_card, list):
        bank_card_process = [column_conversion.rename_f(x.lower()) for x in bank_card]
    else:
        bank_card_process = [column_conversion.rename_f(bank_card.lower())]
    result = data_api.merge(commissions, left_on='name_join', right_on='ENTIDAD_CAJERO', how='left')
    result_client = result[(result['ENTIDAD_CLIENTE'].isin(bank_card_process))]
    result_client = column_conversion.upper_column(result_client, 'name')
    result_client = column_conversion.upper_column(result_client, 'ENTIDAD_CLIENTE')
    result_client_process = result_client[
        ['name', 'geometry.location.lat', 'geometry.location.lng', 'COMISION_1', 'vicinity',
         'name_join', 'ENTIDAD_CLIENTE', 'ENTIDAD_CAJERO']].drop_duplicates(subset=['ENTIDAD_CLIENTE','ENTIDAD_CAJERO'], keep='first')
    result_client_process = result_client_process.loc[
        result_client_process.groupby("name")["COMISION_1"].idxmin()].sort_index()
    result_client_process.to_csv('./data/processed/result_client_process.csv', index=False)
    dict_results = result_client_process.to_dict('records')
    atm_frees = result_client_process.loc[
        result_client_process.groupby("ENTIDAD_CLIENTE")["COMISION_1"].idxmin()].sort_index()
    location_atm_free = (atm_frees['geometry.location.lat'].iloc[0], atm_frees['geometry.location.lng'].iloc[0])
    location_atm_near = (result_client_process['geometry.location.lat'].iloc[0], result_client_process['geometry.location.lng'].iloc[0])
    return dict_results, location_atm_free, location_atm_near


def show_in_the_map(dict_results, location_atm_free, location_atm_near, lat_current, lng_current):
    atms_locations = [(rows_result['geometry.location.lat'], rows_result['geometry.location.lng']) for rows_result in
                       dict_results]
    atm_info = marker_template.apply_template(dict_results)
    #marker_layer = gmaps.marker_layer(atms_locations, info_box_content=atm_info)
    fig = gmaps.figure()
    location_current = [(lat_current, lng_current)]
    marker_layer1 = gmaps.marker_layer(location_current)
    fig.add_layer(marker_layer1)

    marker_layer2 = gmaps.symbol_layer(atms_locations, info_box_content=atm_info, scale=6, stroke_color="blue")
    index_free = int("".join([str(integer) for integer in
                              [i for i in range(len(atms_locations)) if atms_locations[i] == location_atm_free]]))
    marker_layer2.markers[index_free].stroke_color = 'green'
    route_map.plot_route((lat_current, lng_current), location_atm_free, fig, 'green', 6.0, 'walking')

    print(location_atm_free, location_atm_near)

    if location_atm_free != location_atm_near:
        index_near = int("".join([str(integer) for integer in
                                  [i for i in range(len(atms_locations)) if atms_locations[i] == location_atm_near]]))
        marker_layer2.markers[index_near].stroke_color = 'red'
        route_map.plot_route((lat_current, lng_current), location_atm_near, fig, 'red', 4.0, 'walking')

    fig.add_layer(marker_layer2)

    embed_minimal_html('export.html', views=[fig])
