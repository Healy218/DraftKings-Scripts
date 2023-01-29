import pandas as pd
import scipy.optimize as opt


# read player data from a csv file into a DataFrame
headers = ['position', 'players', 'cost', 'point_value']
players = pd.read_csv('players.csv', header=None, names=headers)

# define the budget and the number of players needed at each position
budget = 50000
positions = {'QB': 1, 'RB': 1, 'WR': 2, 'TE': 1, 'DST': 1,'FLEX':1}

# create an empty dictionary to store the selected players
selected_players = {}

print(players, budget, positions)

# objective function
def objective(x, players, budget):
    total_cost = sum([players.loc[i]['cost']*x[i] for i in range(len(players))])
    total_points = sum([players.loc[i]['point_value']*x[i] for i in range(len(players))])
    return total_points if total_cost <= budget else float('inf')

# constraints
def constraint(x, players, budget):
    total_cost = sum([players.loc[i]['cost']*x[i] for i in range(len(players))])
    return total_cost - budget

def constraint_flex(x, players, num_players):
    flex_players = players[(players['position'] == 'RB')| (players['position'] == 'WR')|(players['position'] == 'TE')]
    flex_variables = x[flex_players.index]
    return sum(flex_variables) - num_players

for position, num_players in positions.items():
    # filter the players by position
    if position == 'FLEX':
        position_players = players[(players['position'] == 'RB')| (players['position'] == 'WR')|(players['position'] == 'TE')]
    else:
        position_players = players[players['position'] == position]
    # optimize
    x0 = [0] * len(position_players.index)
    bounds = [(0, 1) for i in range(len(position_players))]
    if position == 'FLEX':
        con = [{'type': 'eq', 'fun': constraint_flex, 'args': (position_players,num_players)}, {'type': 'ineq', 'fun': constraint, 'args': (position_players, budget)}]
    else:
        con = {'type': 'ineq', 'fun': constraint, 'args': (position_players, budget)}

    res = opt.minimize(objective, x0, args=(position_players, budget), bounds=bounds, constraints=con)
    # select the top num_players players
    selected_players[position] = position_players.loc[res.x.round() == 1]

# calculate the total cost of the selected players
total_cost = sum([df['cost'].sum() for position, df in selected_players.items()])

# check if the total cost is less than the budget
if total_cost > budget:
    print("The team exceeds the budget")
else:
    print("The team is within budget")
    print("Total cost:", total_cost)
    print("Total points:", res.fun)
for position, df in selected_players.items():
    total_cost_position = df['cost'].sum()
    print(f"Total cost of {position} position: {total_cost_position}")