import pandas as pd
import pulp as pl
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, LpStatus

# read in the csv file
df = pd.read_csv("DKSalaries.csv")

print(df)
# create a LP problem
prob = LpProblem("Fantasy Football Team Selector", LpMaximize)

# define the positions and the budget
positions = {"CPTN": 1, "FLEX": 5}
budget = 50000

# create a binary variable for each player
player_vars = {(row.player, row.position): LpVariable(f"{row.player}_{row.position}", 0, 1, LpInteger)
              for i, row in df.iterrows()}

# add constraints for each position
for pos, count in positions.items():
    prob += sum(player_vars[player, pos] for player, p in player_vars.keys() if p == pos) == count

# add constraint to ensure that the selected FLEX isn't already on the team as a RB, WR or TE
# add constraint to ensure that the selected FLEX isn't already on the team as a RB, WR or TE
rb_wr_te_vars = [player_vars[player, pos] for player, pos in player_vars.keys() if pos in ["RB", "WR", "TE"]]
flex_vars = [player_vars[player, pos] for player, pos in player_vars.keys() if pos == "FLEX"]
for player, pos in player_vars.keys():
    if pos in ["RB", "WR", "TE"]:
        prob += player_vars[player, "FLEX"] <= 1 - player_vars[player, pos]


# add budget constraint
prob += sum(player_vars[player_name, pos] * df.loc[df["player"] == player_name, "cost"].values[0] for player_name, pos in player_vars.keys()) <= budget

# set objective function
prob += sum(player_vars[player, pos] * df.loc[df["player"] == player, "point_value"].values[0] for player, pos in player_vars.keys())

# specify the CPLEX solver
prob.solve(solver=pl.getSolver('CPLEX_CMD'))

# solve the LP problem
status = prob.solve()

print(LpStatus[status])

# print the best team
if status == 1:
    print("Best Team:")
    for player, pos in player_vars.keys():
        if player_vars[player, pos].varValue == 1.0:
            print(f"{player} - {pos} - ${df.loc[df['player'] == player, 'cost'].values[0]} - {df.loc[df['player'] == player, 'point_value'].values[0]} pts")
else:
    print("The LP problem is not solved")