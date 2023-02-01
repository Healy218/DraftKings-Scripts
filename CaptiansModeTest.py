import csv

def update_team_score(team, player_data):
    """
    Calculates the total score of a team based on the players in it
    """
    score = 0
    captain = False
    for p in team:
        if p in player_data:
            if not captain:
                score += player_data[p]["score"] * 1.5
                captain = True
            else:
                score += player_data[p]["score"]
    return score

def get_best_team(player_data, budget=50000):
    """
    Returns the best team based on player data and budget
    """
    n = len(player_data)
    players = list(player_data.keys())
    team = []
    best_team = []
    best_team_value = 0
    best_team_score = 0

    players = sorted(players, key=lambda x: player_data[x]["score"], reverse=True)
    
    for player in players:
        if len(team) == 6:
            break
        if player_data[player]["price"] <= budget:
            team.append(player)
            budget -= player_data[player]["price"]

    best_team = team[:]
    best_team_value = 50000 - budget
    best_team_score = update_team_score(best_team, player_data)
    
    return {"Value": best_team_value, "Score": best_team_score, "Team": best_team}

def print_best_team(best_team, player_data):
    """
    Prints the best team and its value and score
    """
    print("Optimal")
    print("Best Team:")
    for p in best_team["Team"]:
        print("{} - ${} - {:.2f} pts".format(p, player_data[p]["price"], player_data[p]["score"]))
        
def import_csv_data(file_name):
    player_data = {}
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_data[row['Name']] = {"price": float(row['Salary']), "score": float(row['AvgPointsPerGame'])}
    return player_data

if __name__ == "__main__":
    player_data = import_csv_data("DKSalaries.csv")
    best_team = get_best_team(player_data)
    print_best_team(best_team, player_data)
