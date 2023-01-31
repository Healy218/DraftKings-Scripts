import pandas as pd
import pulp as pl
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, LpStatus

# read in the csv file
df = pd.read_csv("DKSalaries.csv")

# create a LP problem
prob = LpProblem("Fantasy Football Team Selector", LpMaximize)

# define the positions and the budget
positions = {"QB": 1, "RB": 2, "WR": 2, "TE": 1, "DST": 1}
budget = 50000

# create a binary variable for each player
player_vars = {row.Name: LpVariable(f"{row.Name}", 0, 1, LpInteger)
              for i, row in df.iterrows()}

# add constraints for each position
for position in positions:
    prob += sum(player_vars[player] for player in player_vars.keys() if df.loc[df.Name == player, 'Position'].values[0] == position) == positions[position]

# add budget constraint
prob += sum(df.loc[df.Name == player, 'Salary'].values[0] * player_vars[player] for player in player_vars.keys()) <= budget

# set objective function
prob += sum(df.loc[df.Name == player, 'AvgPointsPerGame'].values[0] * player_vars[player] for player in player_vars.keys())

# solve the LP problem
status = prob.solve()

print(LpStatus[status])

# print the best team
if status == 1:
    print("Best Team:")
    for i, row in df.iterrows():
        if player_vars[row.Name].varValue == 1:
            print(f"{row.Name} - ${row.Salary} - {row.AvgPointsPerGame} pts")
else:
    print("The LP problem is not solved")
