import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
# Load datasets
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
df_static = pd.read_csv(path + "\FloorCounts_30min_static.csv")
df_dynamic = pd.read_csv(path + "\FloorCounts_30min_dynamic.csv")

# convert Datetime column to datetime object and remove timezone information
df_static['Datetime'] = pd.to_datetime(df_static['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)
df_dynamic['Datetime'] = pd.to_datetime(df_dynamic['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)
## sort both dfs
#df_static = df_static.sort_values(["Datetime", "Corrected_Floor"])
#df_dynamic = df_dynamic.sort_values(["Datetime", "Corrected_Floor"])

# Rename columns to distinguish between static and dynamic counts.
df_static = df_static.rename(columns={"Guest": "Guest_Static", "Staff:": "Staff_Static", "Student": "Student_Static", "Total": "Total_Static"})
df_dynamic = df_dynamic.rename(columns={"Guest": "Guest_Dynamic", "Staff:": "Staff_Dynamic", "Student": "Student_Dynamic", "Total": "Total_Dynamic"})

# Merge static and dynamic datasets
#df_merged = pd.merge(df_static, df_dynamic, on='Datetime')
#print(df_merged)
# Merging df1 and df2 on 'Datetime' and 'Corrected_Floor'
df_merged = pd.merge(df_static[['Datetime', 'Corrected_Floor', 'Total_Static']], df_dynamic[['Datetime', 'Corrected_Floor', 'Total_Dynamic']],
                     on=['Datetime', 'Corrected_Floor'], how='inner')
# remove rows where Total_Static or Total_Dynamic is zero
#df_merged = df_merged.query('Total_Static != 0 and Total_Dynamic != 0')

df_merged.to_csv(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\Analysis\RQ1_static-dynamic\static-dynamic-merged.csv")

# extract columns of interest
static_count = df_merged["Total_Static"]
dynamic_count = df_merged["Total_Dynamic"]

# Perform Wilcoxon test between static and dynamic counts.
stat, p_value = wilcoxon(static_count, dynamic_count)
# Print results
if p_value <= 0.5:
    print(f"Wilcoxon Test Statistic: {stat}\nP-value: {p_value} \nThe difference between the Static and Dynamic counts is significant."
          f"\nThe null hypothesis is rejected.")
else:
    print(f"Wilcoxon Test Statistic: {stat}\nP-value: {p_value} \nThe difference between the Static and Dynamic counts is not significant."
          f"\nThe null hypothesis accepted.")

# Perform Spearmans's Correlation
correlation, correlation_p_value = spearmanr(static_count, dynamic_count)

print(f"Spearman's correlations: {correlation}\nP-value: {correlation_p_value}")

##########################Plotting#############################

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot the 'Total' field from the wifi data
plt.plot(df_merged['Datetime'], df_merged['Total_Static'],
         label='Wi-Fi (Static)', marker='o', markersize=2, linewidth =.5)

# Plot the 'Ins' field from the RFID dataset
plt.plot(df_merged['Datetime'], df_merged['Total_Dynamic'],
         label='Wi-Fi (Dynamic)', marker=7, markersize=2, linewidth =.5)

# Customize the plot
plt.xlabel('Datetime')
plt.ylabel('Count')
plt.title('Comparison of Static amd Dynamic Wi-Fi Counts')
plt.legend()
plt.grid()

# Display the plot
plt.show()

# Create a scatter plot with a line of best fit.
sns.lmplot(x='Total_Static', y='Total_Dynamic', data=df_merged, line_kws={'color': 'red'})

# Customize the plot
plt.xlabel('Total Static Count')
plt.ylabel('Total Dynamic Count')
plt.title('Correlation between Static and Dynamic Counts')


# Display the plot
plt.show()

# Create a scatter plot with a non-linear line of best fit
sns.jointplot(x='Total_Static', y='Total_Dynamic', data=df_merged, kind='reg', joint_kws={'line_kws':{'color':'red'}})
plt.xlabel('Total Static Count')
plt.ylabel('Total Dynamic Count')
plt.title('Correlation between Static and Dynamic Counts')
# Display the plot
plt.show()