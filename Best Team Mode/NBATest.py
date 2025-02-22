import pandas as pd
from pulp import LpVariable, LpProblem, LpMaximize, LpInteger, lpSum, LpStatus

# read in the csv file
df = pd.read_csv("../DraftKings Scripts and Stats/NBA Stats/25NBA2.csv")

# create a LP problem
prob = LpProblem("Fantasy Basketball Team Selector", LpMaximize)

# define the positions and the budget
positions = {"PG": 1, "SG":1, "SF":1, "PF":1, "C": 1, "G":1, "F":1, "UTIL":1}
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
            #if row.Status != "L":
            #    prob += player_vars[(player, roster_position)] == 0    

# add constraint that each player can only be selected once
for player in df['Name'].unique():
    prob += sum(player_vars[(player, pos)] for pos in positions.keys() if (player, pos) in player_vars) <= 1

# add constraint for how many players a team can have
for team in df['TeamAbbrev'].unique():
    prob += sum(player_vars[(player, pos)] for player in df['Name'].unique() for pos in positions.keys() if (player, pos) in player_vars and df.loc[df['Name'] == player, 'TeamAbbrev'].values[0] == team) <= 2

# count the number of players on each team with "O" status
#team_out_count = {}
#for team in df['TeamAbbrev'].unique():
#    team_out_count[team] = sum(1 for player in df[df['TeamAbbrev'] == team]['Status'] if player == 'O')

#print(team_out_count)

# count the number of players on each team with "L" status
#team_likely_count = {}
#for team in df['TeamAbbrev'].unique():
#    team_likely_count[team] = sum(1 for player in df[df['TeamAbbrev'] == team]['Status'] if player == 'L')

#print(team_likely_count)

# multiply the number of averagepoints by 1.1 for each player on a team with 4 or more players with "O" status
#if team_out_count[team] >= 4:
#    for roster_position in positions.keys():
#        prob += lpSum([player_vars[(player, roster_position)] * df.loc[(df["Name"] == player) & (df["Roster Position"].str.contains(roster_position)), "WAvgPoints"].values[0] * 1.1])

# multiply the number of averagepoints by 1.2 for each player on a team with 6 or less players with "L" status
#if team_likely_count[team] <= 6:
#    for roster_position in positions.keys():
#        prob += lpSum([player_vars[(player, roster_position)] * df.loc[(df["Name"] == player) & (df["Roster Position"].str.contains(roster_position)), "WAvgPoints"].values[0] * 1.2])

#print(prob)

# add constraint for the Point Guard position
prob += sum(player_vars[(player, "PG")] for player in df["Name"].unique() if (player, "PG") in player_vars) == 1

# add constraint for the Shot Guard positions
prob += sum(player_vars[(player, "SG")] for player in df["Name"].unique() if (player, "SG") in player_vars) == 1

# add constraint for the Small Forward position
prob += sum(player_vars[(player, "SF")] for player in df["Name"].unique() if (player, "SF") in player_vars) == 1

# add constraint for the Power Forward positions
prob += sum(player_vars[(player, "PF")] for player in df["Name"].unique() if (player, "PF") in player_vars) == 1

# add constraint for the Center position
prob += sum(player_vars[(player, "C")] for player in df["Name"].unique() if (player, "C") in player_vars) == 1

# add constraint for the Gaurd position
prob += sum(player_vars[(player, "G")] for player in df["Name"].unique() if (player, "G") in player_vars) == 1

# add constraint for the Forward positions
prob += sum(player_vars[(player, "F")] for player in df["Name"].unique() if (player, "F") in player_vars) == 1

# add constraint for the Utility position
prob += sum(player_vars[(player, "UTIL")] for player in df["Name"].unique() if (player, "UTIL") in player_vars) == 1


# add budget constraint
budget_constraint = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Roster Position"].str.contains(pos)), "Salary"].values[0] for name, pos in player_vars.keys()]) <= budget
prob += budget_constraint

# set objective function
#objective = lpSum([player_vars[(name, pos)] * df.loc[(df["Name"] == name) & (df["Roster Position"].str.contains(pos)), "WAvgPoints"].values[0] for name, pos in player_vars.keys()])
#prob += objective
# create the objective function
prob += lpSum([player_vars[(player, roster_position)] * df.loc[(df["Name"] == player) & (df["Roster Position"].str.contains(roster_position)), "AvgPointsPerGame"].values[0]  for (player, roster_position) in player_vars])

#* (1.1 if team_out_count[df.loc[df['Name'] == player, 'TeamAbbrev'].values[0]] >= 4 else 1) * (1.2 if team_likely_count[df.loc[df['Name'] == player, 'TeamAbbrev'].values[0]] <= 6 else 1)
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
