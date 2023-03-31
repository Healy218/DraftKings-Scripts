import pandas as pd
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, lpSum, LpStatus

# read in the csv file
df = pd.read_csv("../DraftKings Scripts and Stats/NHL Stats/NHLweek2.csv")

# create a LP problem
prob = LpProblem("Fantasy Baseball Team Selector", LpMaximize)

# define the positions and the budget
positions = {"P": 2, "C":1, "1B":1, "2B":1, "3B": 1, "SS":1, "OF":3}
budget = 50000

# create a binary variable for each player and each position
player_vars = {}
for i, row in df.iterrows():
    player = row.Name
    roster_positions = row["Roster Position"].split("/")
    for roster_position in roster_positions:
        if (player, roster_position) not in player_vars:
            player_vars[(player, roster_position)] = LpVariable(f"{player}_{roster_position}", 0, 1, LpInteger)
            # add constraint that player can only be selected if their status is "P"
            #if row.Status != "P":
            #    prob += player_vars[(player, roster_position)] == 0    

# add constraint that no player with a salary of 2,500 or less can be selected
for player in df['Name'].unique():
    if df.loc[df['Name'] == player, 'Salary'].values[0] <= 2500:
        for pos in positions.keys():
            if (player, pos) in player_vars:
                prob += player_vars[(player, pos)] == 0

# add constraint that each player can only be selected once
for player in df['Name'].unique():
    prob += sum(player_vars[(player, pos)] for pos in positions.keys() if (player, pos) in player_vars) <= 1

# add constraint that each team can only be selected once
for team in df['TeamAbbrev'].unique():
    prob += sum(player_vars[(player, pos)] for player in df['Name'].unique() for pos in positions.keys() if (player, pos) in player_vars and df.loc[df['Name'] == player, 'TeamAbbrev'].values[0] == team) >= 2

# add constraint for the Pitcher position
prob += sum(player_vars[(player, "P")] for player in df["Name"].unique() if (player, "P") in player_vars) == 2

# add constraint for the Catcher position
prob += sum(player_vars[(player, "C")] for player in df["Name"].unique() if (player, "C") in player_vars) == 1

# add constraint for the First Base positions
prob += sum(player_vars[(player, "1B")] for player in df["Name"].unique() if (player, "1B") in player_vars) == 1

# add constraint for the Second Base position
prob += sum(player_vars[(player, "2B")] for player in df["Name"].unique() if (player, "2B") in player_vars) == 1

# add constraint for the Third Base position
prob += sum(player_vars[(player, "3B")] for player in df["Name"].unique() if (player, "3B") in player_vars) == 1

# add constraint for the Short Stop position
prob += sum(player_vars[(player, "SS")] for player in df["Name"].unique() if (player, "SS") in player_vars) == 1

# add constraint for the Outfield position
prob += sum(player_vars[(player, "OF")] for player in df["Name"].unique() if (player, "OF") in player_vars) == 3

# add budget constraint
budget_constraint = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Roster Position"].str.contains(pos)), "Salary"].values[0] for name, pos in player_vars.keys()]) <= budget
prob += budget_constraint

# set objective function
objective = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Roster Position"].str.contains(pos)), "AvgPointsPerGame"].values[0] for name, pos in player_vars.keys()])
prob += objective

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
            cost = df.loc[(df['Name'] == player) & (df['Roster Position'].str.contains(pos)), 'Salary'].values[0]
            points = df.loc[(df['Name'] == player) & (df['Roster Position'].str.contains(pos)), 'AvgPointsPerGame'].values[0]
            print(f"{player} - {pos} - ${cost} - {points} pts")
            total_cost += cost
            total_points += points
    print(f"Total cost: ${total_cost}")
    print(f"Total points: {total_points} pts")
else:
    print("The LP problem is not solved")
