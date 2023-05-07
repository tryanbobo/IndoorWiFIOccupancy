import pandas as pd

# Load data from CSV file into a pandas DataFrame
data = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\sampleData\Stack-testData_2022_ytd.csv')

# Apply dynamic mobility filter to the DataFrame
filtered_data = dynamic_mobility_filter(data)

# Define the lookup table for estimated mobility values
mobility_thresholds = {
    (1, 'student'): 5,
    (1, 'staff'): 15,
    (1, 'faculty'): 5,
    (2, 'student'): 5,
    (2, 'staff'): 15,
    (2, 'faculty'): 5,
    (3, 'student'): 10,
    (3, 'staff'): 15,
    (3, 'faculty'): 5,
    (4, 'student'): 10,
    (4, 'staff'): 10,
    (4, 'faculty'): 5,
    (5, 'student'): 15,
    (5, 'staff'): 5,
    (5, 'faculty'): 15,
    (6, 'student'): 15,
    (6, 'staff'): 5,
    (6, 'faculty'): 15,
    (7, 'student'): 10,
    (7, 'staff'): 10,
    (7, 'faculty'): 10,
}

# Define a function to filter stays based on dynamic time threshold
def filter_stays_by_role_floor(stays, roles, floors):
    filtered_stays = []
    for stay in stays:
        if stay['role'] in roles and stay['floor'] in floors:
            threshold = mobility_thresholds[(stay['floor'], stay['role'])]
            if stay['end'] - stay['start'] >= threshold:
                filtered_stays.append(stay)
    return filtered_stays