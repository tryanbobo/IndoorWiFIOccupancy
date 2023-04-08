import matplotlib.dates as mdates

"""
This will generate a separate graph for each day in the DataFrame.
"""

def plot_time_series(df, title):
    # Set 'Datetime' as index
    df = df.set_index('Datetime')

    # Get the unique dates from the DataFrame
    unique_dates = df.index.normalize().unique()

    for date in unique_dates:
        # Select data for the specific date
        daily_df = df.loc[date.strftime('%Y-%m-%d')]

        # Plot the time series for the specific date
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_df.index, daily_df['Floor'], '.', label='Floor')
        ax.plot(daily_df.index, daily_df['GroundTruthFloor'], '-', label='GroundTruthFloor')
        ax.plot(daily_df.index, daily_df['Corrected_Floor'], '--', label='Corrected_Floor')

        ax.set_xlabel('Datetime')
        ax.set_ylabel('Floor')
        ax.set_title(f'{title} - {date.strftime("%Y-%m-%d")}')

        # Format x-axis ticks to display hour and minute
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Set y-axis ticks to integers from 1 to 7
        axs[i].set_yticks(range(1, 8))

        plt.legend(loc='best')
        plt.show()