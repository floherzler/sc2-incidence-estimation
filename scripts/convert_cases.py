# read new_cases
import pandas as pd

df = pd.read_csv('../data/france_new_cases_2022_owid.csv')

# Create a new column for daily average cases initialized to 0
df['daily_avg_cases'] = 0.0

# Iterate through the DataFrame and distribute weekly cases over the last 7 days
for i in range(len(df)):
    # Check if it's Sunday and has a non-zero value for 'new_cases'
    if df['new_cases'].iloc[i] != 0:
        # Calculate the daily average for the last 7 days including the current one
        daily_average = df['new_cases'].iloc[i] / 7.0
        # Assign the daily average to the last 7 days
        for j in range(i-6, i+1):
            if j >= 0:  # To avoid negative indexing
                df['daily_avg_cases'].iloc[j] = daily_average

df.to_csv('../data/france_new_avg_cases_2022.csv', index=False)
print(df.head(10))
