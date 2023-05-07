import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load data
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output"
file = path + '\GtMergedEdited.csv'
df = pd.read_csv(file, parse_dates=['Datetime'])

# Convert Datetime column to datetime object
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Sort DataFrame by 'user' and 'Datetime'
df.sort_values(by=['user', 'Datetime'], inplace=True)

# Drop duplicates and unnecessary data
df = df.drop(columns=['action', 'mac_address'])
df= df.drop_duplicates()

# Group data by user
grouped = df.groupby(['user'])

# Function to plot out the various floor columns
# Function to plot out the various floor columns
def plot_time_series(df, title):
    # Set 'Datetime' as index
    df = df.set_index('Datetime')

    # Get the unique dates from the DataFrame
    unique_dates = df.index.normalize().unique()

    # Calculate the number of rows and columns for the subplots
    num_dates = len(unique_dates)
    num_cols = 2
    num_rows = math.ceil(num_dates / num_cols)

    # Create a figure with subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, num_rows * 5), sharey=True)
    axs = axs.flatten()

    # Calculate overall RMSE for the entire DataFrame
    clean_df = df.dropna(subset=['GroundTruthFloor'])
    overall_rmse = math.sqrt(mean_squared_error(clean_df['GroundTruthFloor'], clean_df['Corrected_Floor']))



    for i, date in enumerate(unique_dates):
        # Select data for the specific date
        daily_df = df.loc[date.strftime('%Y-%m-%d')]

        # Calculate RMSE for the specific date
        cleanDaily_df = daily_df.dropna(subset=['GroundTruthFloor'])
        rmse = math.sqrt(mean_squared_error(cleanDaily_df['GroundTruthFloor'], cleanDaily_df['Corrected_Floor']))

        # Plot the time series for the specific date
        axs[i].plot(daily_df.index, daily_df['GroundTruthFloor'], '-', label='Floor: Ground Truth')
        axs[i].plot(daily_df.index, daily_df['Floor'], '--', label='Floor: Wi-Fi Raw')
        axs[i].plot(daily_df.index, daily_df['Corrected_Floor'], ':', label='Floor: Wi-Fi Corrected')

        axs[i].set_xlabel('Datetime')
        axs[i].set_ylabel('Floor')
        axs[i].set_title(f'{date.strftime("%Y-%m-%d")} (RMSE: {rmse:.2f})', fontsize=10, fontweight='bold')

        # Format x-axis ticks to display hour and minute
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Set y-axis ticks to integers from 1 to 7
        axs[i].set_yticks(range(1, 8))

        axs[i].legend(loc='best')

    # Remove extra subplots if any
    for i in range(num_dates, num_rows * num_cols):
        fig.delaxes(axs[i])

    # Adjust the layout and display the plot
    plt.tight_layout()

    fig.subplots_adjust(hspace=0.326, bottom=0.067, top=0.905)

    # Set main title for entire plot with overall RMSE using plt.annotate
    #plt.annotate(f'{title} (Overall RMSE: {overall_rmse:.2f})', xy=(0.5, 0.99), xycoords='figure fraction', ha='center',
    #             va='top', fontsize=16)
    # Set main title for entire plot with overall RMSE using fig.suptitle
    fig.suptitle(f'{title} (Overall RMSE: {overall_rmse:.2f})', fontsize=16, fontweight='bold', y=0.96)

    # Save plot as png
    outputFile = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\BlipFilter\output\figures'

    outputFile = os.path.join(outputFile,f"{title.lstrip('Blip Filter:')}.png"
    )
    plt.savefig(outputFile, bbox_inches='tight')
    print(f"Figure {title} saved at {outputFile}")
    #plt.show()
    plt.close(fig)



# Define function to correct Floor column with variable thresholds
def correct_floor_time_threshold(df, threshold_time_on_initial_floor, threshold_time_on_succeeding_floor):
    # Initialize variables
    floor = df.iloc[0]['Floor']
    last_floor = floor
    last_floor_time = df.iloc[0]['Datetime']
    time_on_current_floor = 0
    corrected_floor = []

    # Iterate through rows in the DataFrame
    for i, row in df.iterrows():
        # Condition 1: Check if floor has changed
        if row['Floor'] != floor:
            # Check if previous floor was correct (change of less than threshold_time_on_succeeding_floor minutes and occupancy of at least threshold_time_on_initial_floor minutes on the floor)
            if (row['Datetime'] - last_floor_time).seconds / 60 < threshold_time_on_succeeding_floor and time_on_current_floor >= threshold_time_on_initial_floor:
                # Set corrected floor to previous floor
                corrected_floor.append(last_floor)
                floor = last_floor
            else:
                # Set corrected floor to current floor
                corrected_floor.append(row['Floor'])
                floor = row['Floor']
                last_floor_time = row['Datetime']
                time_on_current_floor = 0
        else:
            # Set corrected floor to current floor
            corrected_floor.append(row['Floor'])
            last_floor = row['Floor']
            time_on_current_floor += (row['Datetime'] - last_floor_time).seconds / 60
            last_floor_time = row['Datetime']

    # Create a new DataFrame with the same index as the input DataFrame and the corrected_floor as a column
    corrected_floor_df = df.copy()
    corrected_floor_df['Corrected_Floor'] = corrected_floor
    return corrected_floor_df

# Define function to correct isolated floor changes (Condition 2)
def correct_isolated_floor_changes(df):
    for index in range(1, len(df) - 1):
        prev_floor = df.at[index - 1, 'Corrected_Floor']
        curr_floor = df.at[index, 'Corrected_Floor']
        next_floor = df.at[index + 1, 'Corrected_Floor']

        # Condition 2: Check if current floor is different from both previous and next floors
        if curr_floor != prev_floor and curr_floor != next_floor:
            df.at[index, 'Corrected_Floor'] = prev_floor

    return df

# Main loop iterating through threshold combinations
results = []

for threshold_time_on_initial_floor in range(0, 4):
    for threshold_time_on_succeeding_floor in range(0, 4):
        corrected_floor_dfs = [correct_floor_time_threshold(group, threshold_time_on_initial_floor, threshold_time_on_succeeding_floor) for _, group in grouped]
        df_combined = pd.concat(corrected_floor_dfs)
        df_combined = correct_isolated_floor_changes(df_combined)

        df_clean = df_combined.dropna(subset=['GroundTruthFloor'])
        # Calculate Mean Squared Error (MSE) and Mean Absolute Error (MAE)
        mse = mean_squared_error(df_clean['GroundTruthFloor'], df_clean['Corrected_Floor'])
        mae = mean_absolute_error(df_clean['GroundTruthFloor'], df_clean['Corrected_Floor'])

        #calc RMSE
        rmse = math.sqrt(mse)

        # Store results
        results.append({
            'Initial floor threshold': threshold_time_on_succeeding_floor,
            'Succeeding floor threshold ': threshold_time_on_initial_floor,
            'mse': mse,
            'mae': mae,
            'rmse': rmse
        })
        # Plot the time series for the current combination (only for the first user for demonstration purposes)
        if threshold_time_on_initial_floor < 4 and threshold_time_on_succeeding_floor < 4:
            plot_title = f' Blip Filter: Initial floor threshold = {threshold_time_on_succeeding_floor}-minutes and Succeeding floor threshold = {threshold_time_on_initial_floor}-minutes'
            plot_time_series(df_combined[df_combined['user'] == df_combined['user'].unique()[0]], plot_title)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Sort results_df by RMSE and print the top 5 rows
results_df = results_df.sort_values(by='rmse')

print("Top 5 best RMSE combinations:")
print(results_df.head(5))

# Find the combination of thresholds with the lowest MSE and MAE
best_mse_row = results_df.loc[results_df['mse'].idxmin()]
best_mae_row = results_df.loc[results_df['mae'].idxmin()]

print("Best MSE combination:")
print(best_mse_row)
print("\nBest MAE combination:")
print(best_mae_row)

# Find post filter MAE and MSE results (ground truth and raw wifi reading)
df_clean = df.dropna(subset=['GroundTruthFloor'])
mse = mean_squared_error(df_clean['GroundTruthFloor'], df_clean['Floor'])
mae = mean_absolute_error(df_clean['GroundTruthFloor'], df_clean['Floor'])

print('MSE of raw Wi-Fi and Ground Truth = {}'.format(mse))
print('MAE of raw Wi-Fi and Ground Truth = {}'.format(mae))

#print(results_df)

