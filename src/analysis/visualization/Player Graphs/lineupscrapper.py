import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.lineups.com/nba/fantasy-points-per-game'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.content
else:
    print('Error: Could not retrieve data')

print(html_content)
soup = BeautifulSoup(html_content, 'html.parser')
csv_data = []

table = soup.find('table')
rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    csv_data.append(cols)

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
