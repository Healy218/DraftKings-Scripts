import pandas as pd
import matplotlib.pyplot as plt

# Load data
# Replace 'your_data.csv' with your file path
data = pd.read_csv('your_data.csv')
# Ensure Date is in datetime format
data['Date'] = pd.to_datetime(data['Date'])
data.sort_values('Date', inplace=True)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['FantasyPoints'], color='blue', marker='o')
plt.title('Fantasy Football Points Over Time')
plt.xlabel('Date')
plt.ylabel('Fantasy Points')
plt.grid(True)
plt.show()
