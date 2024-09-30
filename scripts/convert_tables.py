# read new_cases
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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


# delete the new_cases column
df = df.drop(columns=['new_cases'])
df.to_csv('../data/france_new_avg_cases_2022.csv', index=False)
print(df.head(10))

# histogram of the amount of reported cases 
df = pd.read_csv('../data/france_new_avg_cases_2022.csv', parse_dates=[0], dayfirst=False) 
start_date = '2022-01-01'
end_date = '2022-06-30'
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

num_bins = 20 

plt.figure(figsize=(10, 6))
counts, bin_edges, _ = plt.hist(filtered_df['date'], weights=filtered_df['daily_avg_cases'], bins=num_bins, edgecolor='black')

plt.xlabel('Dates')
plt.ylabel('reported cases')
plt.title(f'Histogram of reported cases over Time (2022-01-01 to 2022-06-30) with {num_bins} bins')
plt.xticks(rotation=45)
plt.gca().set_xticks(bin_edges) 
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.tight_layout() 
plt.savefig('../results/plots/hist.png', dpi=300, bbox_inches='tight') 

#histogram for sequences per day
df = pd.read_csv('../data/france_sonar_output.csv', parse_dates=['date'], dayfirst=False) 
date_counts = df['date'].value_counts().sort_index()  # Count occurrences per date and sort by date
plt.figure(figsize=(10, 6))
weekdays = pd.to_datetime(date_counts.index).day_name()  # Get the day of the week for each date
colors = ['red' if day == 'Monday' else 'blue' for day in weekdays]  #
plt.bar(date_counts.index, date_counts.values, color=colors, width=0.8, edgecolor='black')
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='red', edgecolor='black', label='Monday'),
                   Patch(facecolor='blue', edgecolor='black', label='Other Days')]
plt.legend(handles=legend_elements)
plt.xlabel('Date')
plt.ylabel('Number of Entries')
plt.title('Number of sequences per Day')
plt.xticks(rotation=45)
plt.tight_layout() 
plt.savefig('../results/plots/hist_seq.png', dpi=300, bbox_inches='tight') 
