import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load data
df = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration\FloorCounts_30min_static.csv')

# Sort data by datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

# Set up plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize bars
bars = [ax.bar3d(x, y, z, dx, dy, dz) for x, y, z, dx, dy, dz in zip([], [], [], [], [], [])]

# Update function for animation
def animate(i):
    ax.clear()
    df_i = df[df['Datetime'] == df['Datetime'].unique()[i]]
    ax.bar3d(df_i['Corrected_Floor'], df_i['Total'], np.zeros(len(df_i)), 1, 1, df_i['Total'])
    ax.set_title('Time: ' + str(df['Datetime'].unique()[i]))
    ax.set_xlabel('Floor')
    ax.set_zlabel('Occupancy')

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(df['Datetime'].unique()), interval=200)

plt.show()