from dotenv import load_dotenv
import googlemaps
import os
import requests
from package import column_conversion
from package import marker_template
import gmaps
from ipywidgets.embed import embed_minimal_html
import pandas as pd

load_dotenv()
api_key_miguel = os.environ["api_key_number"]
gmaps.configure(api_key=api_key_miguel)


def lat_lng_current_location(current_location):
    gmaps_google = googlemaps.Client(key=api_key_miguel)
    geocode_result = gmaps_google.geocode(current_location)
    lat = str(geocode_result[0]['geometry']['location']['lat'])
    lng = str(geocode_result[0]['geometry']['location']['lng'])
    print(lat, lng)
    return lat, lng


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


def processing(data_api, comisions, bank_card):
    result = data_api.merge(comisions, left_on='name_join', right_on='ENTIDAD_CAJERO', how='left')
    result_client = result[(result['ENTIDAD_CLIENTE'] == bank_card)]
    column_conversion.title_column(result_client, 'name')
    result_client_process = result_client[
        ['name', 'geometry.location.lat', 'geometry.location.lng', 'COMISION_1', 'vicinity',
         'name_join']].drop_duplicates(subset="name_join", keep='first')
    result_client_process.to_csv('./data/processed/result_client_process.csv', index=False)
    dict_results = result_client_process.to_dict('records')
    return dict_results


def show_in_the_map(dict_results):
    atms_locations = [(rows_result['geometry.location.lat'], rows_result['geometry.location.lng']) for rows_result in
                       dict_results]
    atm_info = marker_template.apply_template(dict_results)
    marker_layer = gmaps.marker_layer(atms_locations, info_box_content=atm_info)
    fig = gmaps.figure()
    marker_layer.markers[0].label = 'F'
    fig.add_layer(marker_layer)
    embed_minimal_html('export.html', views=[fig])
