import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

# Function to determine if given time is within operating hours
def within_hours(dt):
    weekday_open, weekday_close = 6.5, 25  # Monday to Thursday, 6:30 am to 1 am next day
    friday_open, friday_close = 6.5, 20  # Friday, 6:30 am to 8 pm
    saturday_open, saturday_close = 9, 19  # Saturday, 9 am to 7 pm
    sunday_open, sunday_close = 9, 25  # Sunday, 9 am to 1 am next day

    if dt.dayofweek == 0:  # Monday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 1:  # Tuesday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 2:  # Wednesday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 3:  # Thursday
        return weekday_open <= dt.hour < weekday_close
    elif dt.dayofweek == 4:  # Friday
        return friday_open <= dt.hour < friday_close
    elif dt.dayofweek == 5:  # Saturday
        return saturday_open <= dt.hour < saturday_close
    else:  # dt.dayofweek == 6, Sunday
        return sunday_open <= dt.hour < sunday_close

# Load datasets
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\agg\aggDuration"
df_static = pd.read_csv(path + "\FloorCounts_30min_static.csv")
df_dynamic = pd.read_csv(path + "\FloorCounts_30min_dynamic.csv")

# convert Datetime column to datetime object and remove timezone information
df_static['Datetime'] = pd.to_datetime(df_static['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)
df_dynamic['Datetime'] = pd.to_datetime(df_dynamic['Datetime']).dt.tz_convert('US/Central').dt.tz_localize(None)

# Filter data according to the opening hours
df_static = df_static[df_static['Datetime'].apply(within_hours)]
df_dynamic = df_dynamic[df_dynamic['Datetime'].apply(within_hours)]

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

# Set font family to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot the 'Total' field from the wifi data
plt.plot(df_merged['Datetime'], df_merged['Total_Static'],
         label='Wi-Fi (Static)', marker='o', markersize=2, linewidth=.5)

# Plot the 'Ins' field from the RFID dataset
plt.plot(df_merged['Datetime'], df_merged['Total_Dynamic'],
         label='Wi-Fi (Dynamic)', marker=7, markersize=2, linewidth=.5)

# Customize the plot
plt.xlabel('Datetime', fontname='Times New Roman')
plt.ylabel('Count', fontname='Times New Roman')
plt.title('Comparison of Static and Dynamic Wi-Fi Counts', fontname='Times New Roman')
plt.legend()
plt.grid()

# Display the plot
plt.show()

# Set font family to Times New Roman
sns.set(font='Times New Roman')

# Create a scatter plot with a line of best fit.
sns.lmplot(x='Total_Static', y='Total_Dynamic', data=df_merged, line_kws={'color': 'red'})

# Customize the plot
plt.subplots_adjust(top=0.924)
plt.xlabel('Total Static Count', fontname='Times New Roman')
plt.ylabel('Total Dynamic Count', fontname='Times New Roman')
plt.title('Correlation Between Static and Dynamic Counts', fontname='Times New Roman')

# Display the plot
plt.show()

# Set font family to Times New Roman
sns.set(font='Times New Roman')

# Create a scatter plot with a non-linear line of best fit
sns.jointplot(x='Total_Static', y='Total_Dynamic', data=df_merged, kind='reg', joint_kws={'line_kws': {'color': 'red'}})
plt.subplots_adjust(hspace=0.465)
plt.xlabel('Total Static Count', fontname='Times New Roman')
plt.ylabel('Total Dynamic Count', fontname='Times New Roman')
plt.title('Correlation Between Static and Dynamic Counts', fontname='Times New Roman')

# Display the plot
plt.show()