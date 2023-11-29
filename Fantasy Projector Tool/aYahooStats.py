import os
from requests_oauthlib import OAuth1Session

# Your consumer key and secret
consumer_key = 'dj0yJmk9MENRenlmWmdIQ1hZJmQ9WVdrOU9XMXRkVWR3ZWt3bWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWM4'
consumer_secret = '567f0d483ce061816f3aca9e0a8defbc78fe3e1a'

# File to store tokens
token_file_name = f'/tmp/oauth_data_token_storage_{consumer_key}.out'

# Initialize variables
access_token = None
access_secret = None
access_session = None

# Check if token file exists and read tokens
if os.path.exists(token_file_name):
    with open(token_file_name, 'r') as file:
        lines = file.readlines()
        if len(lines) == 3:
            access_token, access_secret, access_session = [
                line.strip() for line in lines]
        else:
            print("Token file is not formatted correctly")

# Start OAuth session
yahoo = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

if access_token:
    # If tokens exist, try using them
    yahoo.token = (access_token, access_secret)
    try:
        response = yahoo.get(
            'https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nfl/teams')
        if response.status_code == 200:
            print("Successfully fetched data from API")
            print(response.text)
        else:
            print("Failed to fetch data")
    except Exception as e:
        print(f"Error when using existing tokens: {str(e)}")
else:
    # If no tokens, start OAuth flow
    try:
        # Step 1: Get a request token
        print("Attempting to get a request token...")
        yahoo.fetch_request_token(
            'https://api.login.yahoo.com/oauth/v2/get_request_token')
        # Step 2: Redirect user to Yahoo for authorization
        authorization_url = yahoo.authorization_url(
            'https://api.login.yahoo.com/oauth/v2/request_auth')
        print(f"Please go to this URL and authorize: {authorization_url}")
    except Exception as e:
        print(f"Error during request token acquisition: {str(e)}")
        exit()

    # Step 3: Get the authorization verifier code from the user
    try:
        verifier = input("Paste the verifier code here: ")
        # Step 4: Fetch the access token
        yahoo.fetch_access_token(
            'https://api.login.yahoo.com/oauth/v2/get_token', verifier)
        access_token, access_secret = yahoo.token
        # Save the new tokens
        with open(token_file_name, 'w') as file:
            file.write(
                f"{access_token}\n{access_secret}\n{yahoo.client.resource_owner_key}\n")
    except Exception as e:
        print(f"Error during access token acquisition: {str(e)}")
