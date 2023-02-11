def calculate_fantasy_points(passing_yards, passing_tds, interceptions, fumbles, rushing_yards, rushing_tds, receptions, receiving_yards, receiving_tds, feild_goals, sacks, dint, points_allowed, extra_point, feild_goal40, feild_goal50):
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
    sack_points = 1
    dint_points = 2

    #Set Bonuses
    if passing_yards >= 300:
        fantasy_points += 3
    if rushing_yards >= 100:
        fantasy_points += 3
    if receptions >= 100:
        fantasy_points += 3

    #Set Defense scheme
    if points_allowed == 0:
        fantasy_points += 10
    elif points_allowed >= 1 and points_allowed <= 6:
        fantasy_points += 7
    elif points_allowed >= 7 and points_allowed <= 13:
        fantasy_points += 4
    elif points_allowed >= 21 and points_allowed <= 27:
        fantasy_points += 0
    elif points_allowed >= 28 and points_allowed <= 34:
        fantasy_points -= 1
    elif points_allowed >= 35:
        fantasy_points -= 4

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
    fantasy_points += sacks * sack_points
    fantasy_points += dint * dint_points

    return fantasy_points