import pandas as pd
import pulp as pl
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, LpStatus

# read in the csv file
df = pd.read_csv("../DraftKings Scripts and Stats/NFL Stats/SB2025.csv")

# create a LP problem
lp_maximize = LpMaximize
prob = LpProblem("Fantasy Football Team Selector", lp_maximize)

# define the positions and the budget
positions = {"CPT": 1, "FLEX": 5}
budget = 50000

# create a binary variable for each player and roster position
player_vars = {}
for i, row in df.iterrows():
    player = row.Name
    roster_position = row.Roster_Position
    if (player, roster_position) not in player_vars:
        player_vars[(player, roster_position)] = LpVariable(
            f"{player}_{roster_position}", 0, 1, LpInteger)

# add constraint for the captain position
prob += sum(player_vars[(player, "CPT")]
            for player in df["Name"].unique() if (player, "CPT") in player_vars) == 1

# add constraint for the flex positions
prob += sum(player_vars[(player, "FLEX")]
            for player in df["Name"].unique() if (player, "FLEX") in player_vars) == 5

# add budget constraint
prob += sum(df.loc[(df["Name"] == player) & (df["Roster_Position"] == roster_position), 'Salary'].values[0] * player_vars[(player, roster_position)]
            for player, roster_position in player_vars.keys()) <= budget

# add constraint to make sure that a player cannot be CPT and FLEX
for player in df["Name"].unique():
    if (player, "CPT") in player_vars and (player, "FLEX") in player_vars:
        prob += player_vars[(player, "CPT")] + \
            player_vars[(player, "FLEX")] <= 1

# set objective function
prob += sum(df.loc[(df["Name"] == player) & (df["Roster_Position"] == roster_position), 'AvgPointsPerGame'].values[0] *
            (1.5 if roster_position == "CPT" else 1) *
            player_vars[(player, roster_position)]
            for player, roster_position in player_vars.keys())

# solve the LP problem
status = prob.solve(solver=pl.GLPK())

print(LpStatus[status])

# print the best team
if status == 1:
    print("Best Team:")
    total_salary = 0
    total_points = 0

    for player, roster_position in player_vars.keys():
        if player_vars[(player, roster_position)].varValue == 1:
            salary = df.loc[(df["Name"] == player) & (
                df["Roster_Position"] == roster_position), 'Salary'].values[0]
            avg_points = df.loc[(df["Name"] == player) & (
                df["Roster_Position"] == roster_position), 'AvgPointsPerGame'].values[0]
            teamposition = df.loc[(df["Name"] == player) & (
                df["Roster_Position"] == roster_position), 'Roster_Position'].values[0]
            total_salary += salary
            total_points += avg_points
            print(f"{player} - ${salary} - {avg_points} pts {teamposition}")
    print(f"Total Salary: ${total_salary}")

else:
    print("The LP problem is not solved")
