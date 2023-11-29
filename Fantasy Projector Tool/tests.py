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
        return response.json().get('access_token')
        print('good job')
    else:
        print(f"Failed to obtain token: {response.status_code}")
        return None


def fetch_nfl_player_data():
    # URL for the NFL API - replace with the specific endpoint you need
    url = 'https://api.nfl.com/v1/reroute'

    # Headers or parameters might be required for authorization or specific data
    # Replace with actual headers or params as needed
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',  # Replace with your API key if needed
    }

    # Make the request to the NFL API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed - this will depend on the structure of the response
        # For example, converting it to a pandas DataFrame
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


# Fetch and print the data
player_data = fetch_nfl_player_data()
if player_data is not None:
    print(player_data)
