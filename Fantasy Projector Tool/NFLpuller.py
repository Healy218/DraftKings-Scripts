import requests
import pandas as pd


def fetch_nfl_player_data():
    # URL for the NFL API - replace with the specific endpoint you need
    url = 'https://api.nfl.com/v1/players'

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
