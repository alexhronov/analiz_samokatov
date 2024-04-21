import  datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy


def hour_counter(arg):
    return int(datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').hour)


df = pd.read_csv('rides_final.csv', sep=',', encoding='utf-8',
                 skipinitialspace=True, keep_default_na=False, na_values=('', ' '), decimal=',').fillna('NaN')

df['day'] = df['start_date'].apply(lambda arg: str(datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').month) + str(
    datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').day))
df['hour'] = df['start_date'].apply(lambda arg: hour_counter(arg))

starts_n_ends = {}
res = {}

for loc in df['start_location'].unique():
    starts_n_ends[loc] = []
    data_loc_start = df[df['start_location'] == loc]['hour'].value_counts()
    data_loc_end = df[df['end_location'] == loc]['hour'].value_counts()
    for hour in range(24):
        try:
            starts_n_ends[loc].append(data_loc_end[hour] - data_loc_start[hour])
        except KeyError as exp:
            pass
    try:
        starts_n_ends[loc] = numpy.cumsum(starts_n_ends[loc])
        res[loc] = min(starts_n_ends[loc])
    except Exception as exp:
        pass

plt.bar(res.keys(), res.values())
plt.title('Трафик самокатов по точкам')
plt.savefig('scooters_per_point.png')
