"""
Configuration file for API keys and settings.
DO NOT commit this file with actual API keys.
"""

# DraftKings API Configuration
DRAFTKINGS_API = {
    'base_url': 'https://api.draftkings.com',
    'api_key': 'YOUR_API_KEY_HERE',
    'timeout': 30
}

# ESPN API Configuration
ESPN_API = {
    'base_url': 'https://site.api.espn.com/apis/site/v2/sports',
    'api_key': 'YOUR_API_KEY_HERE',
    'timeout': 30
}

# Yahoo Sports API Configuration
YAHOO_API = {
    'base_url': 'https://api.yahoo.com/v1',
    'client_id': 'YOUR_CLIENT_ID_HERE',
    'client_secret': 'YOUR_CLIENT_SECRET_HERE',
    'timeout': 30
}

# Twitter API Configuration (for news and updates)
TWITTER_API = {
    'consumer_key': 'YOUR_CONSUMER_KEY',
    'consumer_secret': 'YOUR_CONSUMER_SECRET',
    'access_token': 'YOUR_ACCESS_TOKEN',
    'access_token_secret': 'YOUR_ACCESS_TOKEN_SECRET'
}

# General Settings
SETTINGS = {
    'default_sport': 'NBA',
    'data_update_frequency': 'daily',
    'timezone': 'America/New_York',
    'cache_timeout': 3600  # 1 hour
}
