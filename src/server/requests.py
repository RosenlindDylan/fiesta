from flask import Flask, jsonify, request
import requests

app = Flask(__fiesta_requests__)

@app.route('/currently-playing')
def currently_playing():
    access_token = request.args.get('access_token')

    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)

        if response.status_code == 200:
            currently_playing_data = response.json()
            return jsonify(currently_playing_data)
        else:
            return jsonify({'error': 'Failed to fetch currently playing song'}), response.status_code
    else:
        return jsonify({'error': 'Access token not provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
