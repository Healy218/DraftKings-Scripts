import pandas as pd
import pulp as pl
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, LpStatus

# read in the csv file
df = pd.read_csv("players.csv")

# create a LP problem
prob = LpProblem("Fantasy Football Team Selector", LpMaximize)

# define the positions and the budget
positions = {"QB": 1, "RB": 2, "WR": 3, "TE": 1, "DST": 1, "FLEX": 1}
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

# create a list to store the results
results = []
teams = []

# solve the LP problem
status = prob.solve()

print(LpStatus[status])

# print the best team
if status == 1:
    print("Best Team:")
    team = []
    for player, pos in player_vars.keys():
        if player_vars[player, pos].varValue == 1.0:
            print(f"{player} - {pos} - ${df.loc[df['player'] == player, 'cost'].values[0]} - {df.loc[df['player'] == player, 'point_value'].values[0]} pts")
            team.append((player, pos, df.loc[df['player'] == player, 'cost'].values[0], df.loc[df['player'] == player, 'point_value'].values[0]))
    teams.append(team)
else:
    print("The LP problem is not solved")

# check if the problem is solved
if status == 1:
    # loop through all players and positions
    for player, pos in player_vars.keys():
        if player_vars[player, pos].varValue == 1.0:
            results.append((player, pos, df.loc[df['player'] == player, 'cost'].values[0], df.loc[df['player'] == player, 'point_value'].values[0]))
    
    # sort the results based on the point value in descending order
    results.sort(key=lambda x: x[3], reverse=True)

    # print the top 5 results
    print("Top 5 Teams:")
    for i, team in enumerate(teams[:5]):
        print(f"{str(i + 1)}. {results[0]} - {results[1]} - ${results[2]} - {results[3]} pts")
        for player in team:
            print(f"   {player[0]} - {player[1]} - ${player[2]} - {player[3]} pts")
else:
    print("The LP problem is not solved")
