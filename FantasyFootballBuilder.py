import pandas as pd
import pulp as pl
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger

solver = pl.getSolver('CPLEX_CMD')
# read in the csv file
df = pd.read_csv("players.csv")

# create a LP problem
prob = LpProblem("Fantasy Football Team Selector", LpMaximize)

# define the positions and the budget
positions = ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "DST", "FLEX"]
budget = 50000

# create a binary variable for each player
player_vars = {(row.player, row.position): LpVariable(f"{row.player}_{row.position}", 0, 1, LpInteger)
              for i, row in df.iterrows()}

# add constraints for each position
prob += sum(player_vars[player, "QB"] for player, pos in player_vars.keys() if pos == "QB") == 1
prob += sum(player_vars[player, "RB"] for player, pos in player_vars.keys() if pos == "RB") == 2
prob += sum(player_vars[player, "WR"] for player, pos in player_vars.keys() if pos == "WR") == 3
prob += sum(player_vars[player, "TE"] for player, pos in player_vars.keys() if pos == "TE") == 1
prob += sum(player_vars[player, "DST"] for player, pos in player_vars.keys() if pos == "DST") == 1

# add flex constraint
prob += sum(player_vars[player, "RB"] for player, pos in player_vars.keys() if pos == "RB") + \
        sum(player_vars[player, "WR"] for player, pos in player_vars.keys() if pos == "WR") + \
        sum(player_vars[player, "TE"] for player, pos in player_vars.keys() if pos == "TE") >= 1

# add budget constraint
prob += sum(player_vars[player, pos] * df.loc[df["player"] == player, "cost"].values[0] for player, pos in player_vars.keys()) <= budget

# set objective function
prob += sum(player_vars[player, pos] * df.loc[df["player"] == player, "point_value"].values[0] for player, pos in player_vars.keys())

# specify the CPLEX solver
prob.solve(solver=solver)

# solve the LP problem
status = prob.solve()

# print the best team
print("Best Team:")
for player, pos in player_vars.keys():
    if player_vars[player, pos].varValue == 1.0:
        print(f"{player} - {pos} - {df.loc[df['player'] == player, 'cost'].values[0]} - {df.loc[df['player'] == player, 'point_value'].values[0]}")