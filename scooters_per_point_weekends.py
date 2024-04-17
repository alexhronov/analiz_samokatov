import pandas as pd
import matplotlib.pyplot as plt
import datetime


def day_maker(arg):
    arg = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
    return str(arg.month) + str(arg.day)


def is_weekend(arg):
    arg = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
    return arg.weekday()


df = pd.read_csv('rides_final.csv', sep=',', encoding='utf-8',
                 skipinitialspace=True, keep_default_na=False, na_values=('', ' '), decimal=',').fillna('NaN')

df['day'] = df['start_date'].apply(lambda arg: day_maker(arg))
df['week_day'] = df['start_date'].apply(lambda arg: is_weekend(arg))

starts_n_ends_weekends = {}
starts_n_ends_weekday = {}

data_start_weekends = df[df['week_day'] >= 5]['start_location'].str.lower().str.replace(' ', '-').value_counts()
data_start_weekday = df[df['week_day'] < 5]['start_location'].str.lower().str.replace(' ', '-').value_counts()

data_end_weekends = df[df['week_day'] >= 5]['end_location'].str.lower().str.replace(' ', '-').value_counts()
data_end_weekday = df[df['week_day'] < 5]['end_location'].str.lower().str.replace(' ', '-').value_counts()

for i in df['start_location'].unique():
    try:
        data = df[(df['start_location'] == i) | (df['end_location'] == i)]
        starts_n_ends_weekends[i] = (data_end_weekends[i] - data_start_weekends[i]) / data[data['week_day'] >= 5]['day'].unique().shape[0]
        starts_n_ends_weekday[i] = (data_end_weekday[i] - data_start_weekday[i]) / data[data['week_day'] < 5]['day'].unique().shape[0]
    except KeyError as exp:
        pass

plt.bar(starts_n_ends_weekends.keys(), starts_n_ends_weekends.values())
plt.bar(starts_n_ends_weekday.keys(), starts_n_ends_weekday.values())

plt.show()