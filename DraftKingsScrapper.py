import requests

URL = "https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=96&draftGroupId=81607"

page = requests.get(URL)

print(page.Response())