import csv

def calculate_fantasy_points(passing_yards, passing_tds, interceptions, rushing_yards, rushing_tds, receptions, receiving_yards, receiving_tds):
    fantasy_points = 0
    passing_yards_per_point = 25
    passing_td_points = 4
    interception_points = -1
    rushing_yards_per_point = 10
    rushing_td_points = 6
    reception_points = 1
    receiving_yards_per_point = 10
    receiving_td_points = 6

    fantasy_points += passing_yards / passing_yards_per_point
    fantasy_points += passing_tds * passing_td_points
    fantasy_points += interceptions * interception_points
    fantasy_points += rushing_yards / rushing_yards_per_point
    fantasy_points += rushing_tds * rushing_td_points
    fantasy_points += receptions * reception_points
    fantasy_points += receiving_yards / receiving_yards_per_point
    fantasy_points += receiving_tds * receiving_td_points

    return fantasy_points

def average_stats(input_file, output_file):
    player_stats = {}

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_name = row['Player']
            passing_yards = int(row['Passing Yards'])
            passing_tds = int(row['Passing TDs'])
            interceptions = int(row['Interceptions'])
            rushing_yards = int(row['Rushing Yards'])
            rushing_tds = int(row['Rushing TDs'])
            receptions = int(row['Receptions'])
            receiving_yards = int(row['Receiving Yards'])
            receiving_tds = int(row['Receiving TDs'])

            fantasy_points = calculate_fantasy_points(passing_yards, passing_tds, interceptions, rushing_yards, rushing_tds, receptions, receiving_yards, receiving_tds)
            
            if player_name not in player_stats:
                player_stats[player_name] = {
                    'games': 1,
                    'fantasy_points': fantasy_points
                }
            else:
                player_stats[player_name]['games'] += 1
                player_stats[player_name]['fantasy_points'] += fantasy_points

    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Player', 'Average Fantasy Points'])
        for player_name, stats in player_stats.items():
            writer.writerow([player_name, stats['fantasy_points'] / stats['games']])
