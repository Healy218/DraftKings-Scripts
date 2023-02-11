import csv

def calculate_fantasy_points(passing_yards, passing_tds, interceptions, fumbles, rushing_yards, rushing_tds, receptions, receiving_yards, receiving_tds, feild_goals, extra_point, feild_goal40, feild_goal50):
    #Set variables
    fantasy_points = 0
    passing_yards_per_point = 25
    passing_td_points = 4
    interception_points = -1
    fumble_points = -2
    rushing_yards_per_point = 10
    rushing_td_points = 6
    reception_points = 1
    receiving_yards_per_point = 10
    receiving_td_points = 6
    extra_points = 1
    feild_goal_points = 3
    feild_goal40_points = 4
    feild_goal50_points = 5

    #Set Bonuses
    if passing_yards >= 300:
        fantasy_points += 3
    if rushing_yards >= 100:
        fantasy_points += 3
    if receptions >= 100:
        fantasy_points += 3

    #Calculate Fantasy Points
    fantasy_points += passing_yards / passing_yards_per_point 
    fantasy_points += passing_tds * passing_td_points
    fantasy_points += interceptions * interception_points
    fantasy_points += fumbles * fumble_points
    fantasy_points += rushing_yards / rushing_yards_per_point
    fantasy_points += rushing_tds * rushing_td_points
    fantasy_points += receptions * reception_points
    fantasy_points += receiving_yards / receiving_yards_per_point
    fantasy_points += receiving_tds * receiving_td_points
    fantasy_points += feild_goals * feild_goal_points
    fantasy_points += extra_point * extra_points
    fantasy_points += feild_goal40 * feild_goal40_points
    fantasy_points += feild_goal50 * feild_goal50_points

    return round(fantasy_points, 2)

def calculate_defense_points(sacks, dint, points_allowed):
    defense_points = 0 
    sack_points = 1
    dint_points = 2

    #Set Defense scheme
    if points_allowed == 0:
        defense_points += 10
    elif points_allowed >= 1 and points_allowed <= 6:
        defense_points += 7
    elif points_allowed >= 7 and points_allowed <= 13:
        defense_points += 4
    elif points_allowed >= 21 and points_allowed <= 27:
        defense_points += 0
    elif points_allowed >= 28 and points_allowed <= 34:
        defense_points -= 1
    elif points_allowed >= 35:
        defense_points -= 4
    defense_points += sacks * sack_points
    defense_points += dint * dint_points

    return defense_points 

#input data from csv file and use calculate_fantasy_points to output fantasy points in CSV
def average_stats(input_file, output_file):
    player_stats = {}

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_name = row['player']
            passing_yards = int(row['passing_yards'])
            passing_tds = int(row['passing_td'])
            interceptions = int(row['interceptions'])
            fumbles = int(row['fumbles'])
            rushing_yards = int(row['rushing_yards'])
            rushing_tds = int(row['rushing_tds'])
            receptions = int(row['receptions'])
            receiving_yards = int(row['receiving_yards'])
            receiving_tds = int(row['receiving_tds'])
            feild_goals = int(row['FeildGoal'])
            sacks = int(row['Sacks'])
            dint = int(row['DInt'])
            extra_point = int(row['Extra points']) 
            feild_goal40 = int(row['FeildGoal40'])
            feild_goal50 = int(row['FeildGoal50'])
            points_allowed = int(row['PointsAllowed'])

            fantasy_points = calculate_fantasy_points(passing_yards, passing_tds, interceptions, fumbles, rushing_yards, rushing_tds, receptions, receiving_yards, receiving_tds, feild_goals, extra_point, feild_goal40, feild_goal50)
            defense_points = 0
            if player_name in ["CheifsD", "PhillyD"]:
                defense_points = calculate_defense_points(sacks, dint, points_allowed)
            
            if player_name not in player_stats:
                player_stats[player_name] = {
                    'games': 1,
                    'fantasy_points': fantasy_points,
                    'defense_points': defense_points
                }
            else:
                player_stats[player_name]['games'] += 1
                player_stats[player_name]['fantasy_points'] += fantasy_points
                player_stats[player_name]['defense_points'] += defense_points

    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Player', 'Average Fantasy Points'])
        for player_name, stats in player_stats.items():
            writer.writerow([player_name, (stats['fantasy_points'] + stats['defense_points'])/ stats['games']])

average_stats('MS2G1.csv', 'test.csv')

