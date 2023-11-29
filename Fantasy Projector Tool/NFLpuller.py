import requests
import pandas as pd


def get_nfl_access_token():
    # Endpoint for obtaining the token
    token_url = "https://api.nfl.com/v1/reroute"

    # Data and headers for the POST request
    data = "device_id=5cb798ec-82fc-4ba0-8055-35aad432c492&grant_type=client_credentials"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Domain-Id": "100"
    }

    # Make the POST request
    response = requests.post(token_url, data=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print('Token successfully obtained')
        return response.json().get('access_token')
    else:
        print(f"Failed to obtain token: {response.status_code}")
        return None


def fetch_nfl_player_data(token):
    # URL for fetching player data - replace with the specific endpoint you need
    url = 'https://api.nfl.com/v1/players'  # Example endpoint

    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Make the request to the NFL API
    response = requests.get(url, headers=headers)

    # Print the full response for debugging
    print("Status Code:", response.status_code)
    print("Response:", response.text)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


# Obtain the access token
token = get_nfl_access_token()

# Fetch and print the player data
if token:
    player_data = fetch_nfl_player_data(token)
    if player_data is not None:
        print(player_data)
