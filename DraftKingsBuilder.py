from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, value
import pandas as pd

# Read in the CSV file containing player data
headers = ['position', 'players', 'cost', 'point_value']
df = pd.read_csv("players.csv", dtype={'cost': float, 'point_value': float})


# Create the LP problem
prob = LpProblem("Fantasy Football Team Optimization", LpMaximize)

# Create the decision variables
x1 = LpVariable("QB", 0, 1, LpInteger)
x2 = LpVariable("RB", 0, 2, LpInteger)
x3 = LpVariable("WR", 0, 3, LpInteger)
x4 = LpVariable("TE", 0, 1, LpInteger)
x5 = LpVariable("DST", 0, 1, LpInteger)
x6 = LpVariable("FLEX", 0, 1, LpInteger)

# Define the objective function
#prob += sum([x1*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'QB']) + \
#        sum([x2*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'RB']) + \
#        sum([x3*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'WR']) + \
#        sum([x4*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'TE']) + \
#        sum([x5*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'DST']) + \
#        sum([x6*df.loc[i,'point_value'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'FLEX'])

# Define the budget constraint
#prob += sum([x1*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'QB']) + \
#        sum([x2*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'RB']) + \
#        sum([x3*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'WR']) + \
#        sum([x4*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'TE']) + \
#        sum([x5*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'DST']) + \
#        sum([x6*df.loc[i,'cost'].item() for i in range(df.shape[0]) if df.loc[i,'position'] == 'FLEX']) <= 50000

# Define the objective function
prob += x1*df['point_value'][df['position']=='QB'].sum() + x2*df['point_value'][df['position']=='RB'].sum() + x3*df['point_value'][df['position']=='WR'].sum() + x4*df['point_value'][df['position']=='TE'].sum() + x5*df['point_value'][df['position']=='DST'].sum() + x6*df['point_value'][df['position']=='FLEX'].sum()

# Define the budget constraint
prob += x1*df['cost'][df['position']=='QB'].sum() + x2*df['cost'][df['position']=='RB'].sum() + x3*df['cost'][df['position']=='WR'].sum() + x4*df['cost'][df['position']=='TE'].sum() + x5*df['cost'][df['position']=='DST'].sum() + x6*df['cost'][df['position']=='FLEX'].sum() <= 50000


# Define the positional constraints
prob += x1 == 1  # exactly one QB
prob += x2 == 2  # exactly two RBs
prob += x3 == 3  # exactly three WRs
prob += x4 == 1  # exactly one TE
prob += x5 == 1  # exactly one DST

# Define the FLEX constraint
prob += x2 + x3 + x4 <= 1

print(prob, x1, x2, x3, x4, x5)
# Solve the LP problem
prob.solve()
if prob.status == 1:
    print("Optimal solution found")
elif prob.status == -1:
    print("Infeasible solution")
elif prob.status == -2:
    print("Unbounded solution")
else:
    print("Other solution status: ", prob.status)

print("x1 =", value(x1))
print("x2 =", value(x2))
print("x3 =", value(x3))
print("x4 =", value(x4))
print("x5 =", value(x5))
print("x6 =", value(x6))

# Print out the team
print("Team:")
for i in range(df.shape[0]):
    if df.loc[i,'position'] == 'QB' and value(x1) > 0:
        print(df.loc[i,'players'])
    if df.loc[i,'position'] == 'RB' and value(x2) > 0:
        print(df.loc[i,'players'])
    if df.loc[i,'position'] == 'WR' and value(x3) > 0:
        print(df.loc[i,'players'])
    if df.loc[i,'position'] == 'TE' and value(x4) > 0:
        print(df.loc[i,'players'])
    if df.loc[i,'position'] == 'DST' and value(x5) > 0:
        print(df.loc[i,'players'])