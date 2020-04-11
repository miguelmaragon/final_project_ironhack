import polyline
from dotenv import load_dotenv
import googlemaps
import gmaps
import os

load_dotenv()
api_key_miguel = os.environ["api_key_number_2"]

gmaps_google = googlemaps.Client(key=api_key_miguel)
gmaps.configure(api_key=api_key_miguel)


def plot_route(start_location, end_location, fig, color, stroke_weight_line, route_mode='driving'):
    directions_result = gmaps_google.directions(start_location, end_location, mode=route_mode)
    polyline_directions_result = polyline.decode(directions_result[0]['overview_polyline']['points'])

    polyline_directions_result_due = [(a, b) for a, b in
                                      zip(polyline_directions_result, polyline_directions_result[1:])]
    for i in range(len(polyline_directions_result_due)):
        line_drawing = gmaps.Line(start=polyline_directions_result_due[i][0], end=polyline_directions_result_due[i][1],
                                  stroke_weight=stroke_weight_line, stroke_color=color, stroke_opacity=1.0)
        drawing = gmaps.drawing_layer(features=[line_drawing], show_controls=False)
        fig.add_layer(drawing)