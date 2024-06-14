from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask("fiesta_requests")

# Store your client ID, client secret, and initial access token here
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_TOKEN = "initial_access_token"

def refresh_access_token():
    # Make a POST request to refresh the access token
    refresh_token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('REFRESH_TOKEN'),
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(refresh_token_url, data=payload)
    if response.status_code == 200:
        # Update the access token
        global ACCESS_TOKEN
        ACCESS_TOKEN = response.json()['access_token']
        return True
    else:
        return False

def make_spotify_api_request(url):
    # Check if the access token is still valid
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 401:  # Unauthorized, token expired or invalid
        # Attempt to refresh the access token
        if refresh_access_token():
            # Retry the request with the new access token
            headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
            response = requests.get(url, headers=headers)
    return response

@app.route('/currently-playing')
def currently_playing():
    spotify_api_url = 'https://api.spotify.com/v1/me/player/currently-playing'
    response = make_spotify_api_request(spotify_api_url)
    if response.status_code == 200:
        currently_playing_data = response.json()
        return jsonify(currently_playing_data)
    else:
        return jsonify({'error': 'Failed to fetch currently playing song'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
