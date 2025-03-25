import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('lineup.csv')

# convert dates to datetime objects
#dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]

# create plot
#plt.plot(dates, points)

# set x-axis label
#plt.xlabel("Date")

# set y-axis label
#plt.ylabel("Points")

# set plot title
#plt.title("Points vs Dates")

# display plot
#plt.show()

curry_df = df[df['Name'] == 'Stephen Curry']

date_col = 'Date'  # set to the correct column name
points_col = 'Fantasy Points'

plt.plot(curry_df[date_col], curry_df[points_col])
plt.xlabel('Date')
plt.ylabel('Fantasy Points')
plt.title('Stephen Curry Fantasy Points')
plt.show()

