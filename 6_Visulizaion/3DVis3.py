import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load data
df = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration\FloorCounts_30min_static.csv')

# Sort data by datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

# Filter out floor 8
df = df[df['Corrected_Floor'] != 8]

# Offset floor numbers by 0.5
df['Corrected_Floor'] = df['Corrected_Floor'] - 0.5

# Set up plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define a colormap
colors = plt.cm.viridis(np.linspace(0, 1, df['Corrected_Floor'].nunique()))

# Initialize bars
bars = [ax.bar3d(x, y, z, dx, dy, dz, color=c) for x, y, z, dx, dy, dz, c in zip([], [], [], [], [], [], [])]

# Set y and z limits
ax.set_ylim([0, 8])  # Update y-axis limit to 8
ax.set_zlim([0, df['Total'].max()])

# Update function for animation
def animate(i):
    ax.clear()

    # Reset y and z limits after clearing the axes
    ax.set_ylim([0, 8])  # Update y-axis limit to 8
    ax.set_zlim([0, df['Total'].max()])

    df_i = df[df['Datetime'] == df['Datetime'].unique()[i]]
    for j in df_i['Corrected_Floor'].unique():
        df_j = df_i[df_i['Corrected_Floor'] == j]
        ax.bar3d(df_j['Corrected_Floor'], df_j['Total'], np.zeros(len(df_j)), 1, 1, df_j['Total'], color=colors[int(j)])
    ax.set_title('Time: ' + str(df['Datetime'].unique()[i]))
    ax.set_xlabel('Floor')
    ax.set_zlabel('Occupancy')


# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(df['Datetime'].unique()), interval=200)

plt.show()