from espn_api.football import League
from espn_api.football import Player
import pandas as pd
import matplotlib.pyplot as plt

# https://github.com/cwendt94/espn-api/tree/master/espn_api/football
# Init
league = League(league_id=1064715703, year=2023, espn_s2='AECg5MCZ0W%2FsLl6Bt2UcmBRGTMp%2FITK75UuotCLyTl6rTMVC2z5XBrJjOXcmMo9Bb2RJIvxmQZarAwAKIN87ul0EvEctdnl3bbKjb5DQqAU9ZLlF39owuK0nC%2BHcPHEkYepNmuBphEYK3sCIwR4JDxPAg2UdkeC4fZaefDNZOlU8nFe3l8x%2F%2Fqpyf1FtZYwdOe%2FTQDjzUA0oBFFZdbmYocIi%2FIjqaw%2BMqDAhRQHKDPMGjg6dPM4phWwgADfMB75f72GkBb0Zr47qYXOExdOWb1a%2BZf5TasqSRMhVEG6%2F0UoxvQ%3D%3D',
                swid='{5A6B5D45-5299-45F5-B11A-8A5E5713B4DB}')

# Find Patrick Mahomes in the league teams
mahomes = None
for team in league.teams:
    for player in team.roster:
        if player.name == "Jordan Love":
            mahomes = player
            break
    if mahomes:
        break

print(mahomes.stats[12])
if mahomes:
    # Extracting week numbers and corresponding points
    weeks = mahomes.stats.keys()
    points = [mahomes.stats[12]['points'] for week in weeks]

    # Creating DataFrame
    data = pd.DataFrame(
        {'Week': list(weeks), 'Points': points}).set_index('Week')

    # Plotting
    plt.plot(data['Points'], marker='o')
    plt.title('Weekly Fantasy Points of Patrick Mahomes')
    plt.xlabel('Week')
    plt.ylabel('Fantasy Points')
    plt.xticks(range(1, max(weeks) + 1))  # Set x-ticks to week numbers
    plt.grid(True)
    plt.show()
else:
    print("Patrick Mahomes not found in the league.")
