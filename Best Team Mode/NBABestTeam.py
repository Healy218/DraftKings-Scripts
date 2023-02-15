import pandas as pd
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, lpSum, LpStatus

# read in the csv file
df = pd.read_csv("NBA_players.csv")

# create a LP problem
prob = LpProblem("Fantasy Basketball Team Selector", LpMaximize)

# define the positions and the budget
positions = {"PG": 1, "SG":1, "SF":1, "PF":1, "C": 1, "G":1, "F":1, "UTIL":1}
budget = 50000

# create a binary variable for each player
# create a binary variable for each player and roster position
player_vars = {}
for i, row in df.iterrows():
    player = row.Name
    roster_position = row.Position
    if (player, roster_position) not in player_vars:
        player_vars[(player, roster_position)] = LpVariable(f"{player}_{roster_position}", 0, 1, LpInteger)

# add constraints for each position
for pos, count in positions.items():
    prob += lpSum([player_vars[(name, pos)] for name, p in player_vars.keys() if p == pos]) == count

# add budget constraint
prob += lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Position"] == pos), "Salary"].values[0] for name, pos in player_vars.keys()]) <= budget

# set objective function
prob += lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Position"] == pos), "AvgPointsPerGame"].values[0] for name, pos in player_vars.keys()])

# solve the LP problem
status = prob.solve()

print(LpStatus[status])

# print the best team
if status == 1:
    print("Best Team:")
    total_cost = 0
    total_points = 0
    for player, pos in player_vars.keys():
        if player_vars[player, pos].varValue == 1.0:
            cost = df.loc[df['Name'] == player, 'Salary'].values[0]
            points = df.loc[df['Name'] == player, 'AvgPointsPerGame'].values[0]
            print(f"{player} - {pos} - ${cost} - {points} pts")
            total_cost += cost
            total_points += points
    print(f"Total cost: ${total_cost}")
    print(f"Total points: {total_points} pts")
else:
    print("The LP problem is not solved")
