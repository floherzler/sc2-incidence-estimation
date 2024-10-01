import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch


plt.rcParams.update({'font.size': 14})

def plot_histogram(df, ax, title):
    date_counts = df['date'].value_counts().sort_index()  # Count occurrences per date and sort by date
    weekdays = pd.to_datetime(date_counts.index).day_name()  # Get the day of the week for each date
    colors = ['red' if day == 'Monday' else 'blue' for day in weekdays]  # Color Monday differently
    ax.bar(date_counts.index, date_counts.values, color=colors, width=0.8, edgecolor='black')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Entries')
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)


df1 = pd.read_csv('data/sonar_out_fr.csv', parse_dates=['date'], dayfirst=False)
df2 = pd.read_csv('data/sonar_out_sp.csv', parse_dates=['date'], dayfirst=False)
df3 = pd.read_csv('data/given/germany/sequences_Germany_220101_220630.csv', parse_dates=['date'], dayfirst=False)

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(20, 12), sharex=True)

plot_histogram(df1, axes[0], 'Number of sequences per Day (France)')
plot_histogram(df2, axes[1], 'Number of sequences per Day (Spain)')
plot_histogram(df3, axes[2], 'Number of sequences per Day (Germany)')

# Create a common legend
legend_elements = [Patch(facecolor='red', edgecolor='black', label='Monday'),
                   Patch(facecolor='blue', edgecolor='black', label='Other Days')]
fig.legend(handles=legend_elements, loc='upper right')

plt.subplots_adjust(hspace=0.4, bottom=0.1)  
plt.savefig('results/plots/hist_seq_multiple.png', dpi=300, bbox_inches='tight')
plt.show()
