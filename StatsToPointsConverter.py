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
