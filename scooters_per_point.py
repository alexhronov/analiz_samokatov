import pandas as pd
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('rides_final.csv', sep=',', encoding='utf-8',
                 skipinitialspace=True, keep_default_na=False, na_values=('', ' '), decimal=',').fillna('NaN')

df['day'] = df['start_date'].apply(lambda arg: str(datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').month) + str(datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').day))

data_start = df['start_location'].str.lower().str.replace(" ", "-").value_counts()
data_end = df['end_location'].str.lower().str.replace(" ", "-").value_counts()

starts_n_ends = {}

for i in df['start_location'].unique():
    try:
        starts_n_ends[i] = data_end[i] - data_start[i]
        days = []
        data = df[df['start_location'] == i]['day']
        for j in data:
            if j not in days:
                days.append(j)
        starts_n_ends[i] /= len(days)
    except KeyError as exp:
        pass

plt.bar(starts_n_ends.keys(), starts_n_ends.values())

plt.show()