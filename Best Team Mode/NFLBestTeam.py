import pandas as pd
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, lpSum, LpStatus

# read in the csv file
df = pd.read_csv("../DraftKings Scripts and Stats/NFL Stats/NFLweek1323.csv")

# create a LP problem
prob = LpProblem("Fantasy Football Team Selector", LpMaximize)

# define the positions and the budget
positions = {"QB": 1, "RB": 2, "WR": 3, "TE": 1, "FLEX": 1, "DST": 1}
budget = 50000

# create a binary variable for each player and each position
player_vars = {}
for i, row in df.iterrows():
    player = row['Name']
    salary = row['Salary']  # Correctly retrieving the salary from the row
    roster_positions = row["Roster Position"].split("/")
    for roster_position in roster_positions:
        if (player, roster_position) not in player_vars:
            player_vars[(player, roster_position)] = LpVariable(
                f"{player}_{roster_position}", 0, 1, LpInteger)

        # Adding minimum salary constraints
        if roster_position in ['RB']:
            prob += player_vars[(player, roster_position)] * \
                salary >= player_vars[(player, roster_position)] * 4200
        if roster_position in ['QB']:
            prob += player_vars[(player, roster_position)] * \
                salary >= player_vars[(player, roster_position)] * 5200
        if roster_position in ['WR']:
            prob += player_vars[(player, roster_position)] * \
                salary >= player_vars[(player, roster_position)] * 3100

        if roster_position in ['FLEX']:
            prob += player_vars[(player, roster_position)] * \
                salary >= player_vars[(player, roster_position)] * 4100

# add constraint that each player can only be selected once
for player in df['Name'].unique():
    prob += sum(player_vars[(player, pos)]
                for pos in positions.keys() if (player, pos) in player_vars) <= 1

# add constraint for the QB position
prob += sum(player_vars[(player, "QB")]
            for player in df["Name"].unique() if (player, "QB") in player_vars) == 1

# add constraint for the Running Back positions
prob += sum(player_vars[(player, "RB")]
            for player in df["Name"].unique() if (player, "RB") in player_vars) == 2

# add constraint for the Wide Receiver positions
prob += sum(player_vars[(player, "WR")]
            for player in df["Name"].unique() if (player, "WR") in player_vars) == 3

# add constraint for the Tight End position
prob += sum(player_vars[(player, "TE")]
            for player in df["Name"].unique() if (player, "TE") in player_vars) == 1

# add constraint for the Defense position
prob += sum(player_vars[(player, "DST")]
            for player in df["Name"].unique() if (player, "DST") in player_vars) == 1

# add constraint for the Utility position
prob += sum(player_vars[(player, "FLEX")]
            for player in df["Name"].unique() if (player, "FLEX") in player_vars) == 1


# add budget constraint
budget_constraint = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (
    df["Roster Position"].str.contains(pos)), "Salary"].values[0] for name, pos in player_vars.keys()]) <= budget
prob += budget_constraint

# set objective function
objective = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) &
                  (df["Roster Position"].str.contains(pos)), "AvgPointsPerGame"].values[0] for name, pos in player_vars.keys()])
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
            cost = df.loc[(df['Name'] == player) & (
                df['Roster Position'].str.contains(pos)), 'Salary'].values[0]
            points = df.loc[(df['Name'] == player) & (
                df['Roster Position'].str.contains(pos)), 'AvgPointsPerGame'].values[0]
            print(f"{player} - {pos} - ${cost} - {points} pts")
            total_cost += cost
            total_points += points
    print(f"Total cost: ${total_cost}")
    print(f"Total points: {total_points} pts")
else:
    print("The LP problem is not solved")
