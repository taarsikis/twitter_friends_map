""" GitHub """

import requests
from geopy.geocoders import Nominatim
import folium
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/")
def index():
    """
    Opens start page.
    """
    return render_template("index.html")


def generate_map(nickname_1,bearer_token_1):
    """
    Generates map of locations all followers.
    """

    my_map = folium.Map()
    geolocator = Nominatim(user_agent="twiter.py")

    def twitter_api(nickname,bearer_token):
        """
        Returns info from twitter API.
        """
        base_url = "https://api.twitter.com/"

        search_url = '{}1.1/friends/list.json'.format(base_url)

        search_headers = {
            'Authorization': 'Bearer {}'.format(bearer_token)
        }

        search_params = {
            'screen_name': nickname,
            'count':10
        }

        response = requests.get(search_url, headers = search_headers, params=search_params)
        return response

    response = twitter_api(nickname_1,bearer_token_1)
    needed_users = response.json()["users"]
    for user in needed_users:
        location = user['location']
        if location != '':
            user_location = geolocator.geocode(location)
            user_coords = (user_location.latitude,user_location.longitude)

            user_name = user['screen_name']
            my_map.add_child(folium.Marker(location=[user_coords[0],\
    user_coords[1]], \
    popup= user_name, \
    icon = folium.Icon( color="green", icon_color="yellow", icon="home")))

    my_map.save("templates/map.html")
    return my_map

@app.route("/register", methods=['POST'])
def register():
    """
    Checks requests and generates map.
    """
    nickname =  request.form.get("Nickname")
    bearer_token = request.form.get("bearer_token")
    if not nickname or not bearer_token:
        return render_template("failure.html")
    generate_map(nickname,bearer_token)
    #writer.writerow((request.form.get("name"), request.form.get("domain")))
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=False)
