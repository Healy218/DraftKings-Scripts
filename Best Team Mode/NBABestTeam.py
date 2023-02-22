import pandas as pd
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, lpSum, LpStatus

# read in the csv file
df = pd.read_csv("NBA_players.csv")

# create a LP problem
prob = LpProblem("Fantasy Basketball Team Selector", LpMaximize)

# define the positions and the budget
positions = {"PG": 1, "SG":1, "SF":1, "PF":1, "C": 1, "G":1, "F":1, "UTIL":1}
budget = 50000

# create a binary variable for each player and roster position
player_vars = {}
for i, row in df.iterrows():
    player = row.Name
    roster_position = row.Position
    if (player, roster_position) not in player_vars:
        player_vars[(player, roster_position)] = LpVariable(f"{player}_{roster_position}", 0, 1, LpInteger)

# add constraint for the PG position
prob += sum(player_vars[(player, "PG")] for player in df["Name"].unique() if (player, "PG") in player_vars) == 1

# add constraint for the SG positions
prob += sum(player_vars[(player, "SG")] for player in df["Name"].unique() if (player, "SG") in player_vars) == 1

# add constraint for the SF position
prob += sum(player_vars[(player, "SF")] for player in df["Name"].unique() if (player, "SF") in player_vars) == 1

# add constraint for the PF positions
prob += sum(player_vars[(player, "PF")] for player in df["Name"].unique() if (player, "PF") in player_vars) == 1

# add constraint for the C position
prob += sum(player_vars[(player, "C")] for player in df["Name"].unique() if (player, "C") in player_vars) == 1

# add constraint for the SG and PG positions (G position)
# add constraint for the SG and PG positions (G position)
guard_vars = [player_vars[player, pos] for player, pos in player_vars.keys() if pos in ["SG", "PG"]]
for player, pos in player_vars.keys():
    if pos == "G":
        prob += player_vars[player, "G"] <= 1 - lpSum(guard_vars + [player_vars[player, pos]])


# add constraint for the F position
forward_vars = [player_vars[player, pos] for player, pos in player_vars.keys() if pos in ["SF", "PF"]]
for player, pos in player_vars.keys():
    if pos == "F":
        prob += player_vars[player, "F"] <= 1 - lpSum(forward_vars + [player_vars[player, pos]])

# add constraint for the UTIL positions
utility_vars = [player_vars[player, pos] for player, pos in player_vars.keys() if pos in ["SG", "PG", "SF", "PF", "C"]]
for player, pos in player_vars.keys():
    if pos == "UTIL":
        prob += player_vars[player, "UTIL"] <= 1 - lpSum(utility_vars + [player_vars[player, pos]])

# add budget constraint
budget_constraint = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Position"] == pos), "Salary"].values[0] for name, pos in player_vars.keys()]) <= budget
#print(f"Adding budget constraint: {budget_constraint}")
prob += budget_constraint

# set objective function
objective = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Position"] == pos), "AvgPointsPerGame"].values[0] for name, pos in player_vars.keys()])
#print(f"Setting objective function: {objective}")
prob += objective

#print(prob)
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

