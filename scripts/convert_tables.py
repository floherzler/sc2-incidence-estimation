# read new_cases
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('../data/given/france/france_new_cases_2022_owid.csv')

# Create a new column for daily average cases initialized to 0
df['daily_avg_cases'] = 0.0

# Iterate through the DataFrame and distribute weekly cases over the last 7 days
for i in range(len(df)):
    # Check if it's Sunday and has a non-zero value for 'new_cases'
    if df.loc[i, 'new_cases'] != 0:
        # Calculate the daily average for the last 7 days including the current one
        daily_average = df.loc[i, 'new_cases'] / 7.0
        # Assign the daily average to the last 7 days
        for j in range(i-6, i+1):
            if j >= 0:  # To avoid negative indexing
                df.loc[j, 'daily_avg_cases'] = daily_average


# delete the new_cases column
df = df.drop(columns=['new_cases'])
df.to_csv('../data/france_new_avg_cases_2022.csv', index=False)