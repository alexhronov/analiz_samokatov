import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


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
df['start_district'] = df['start_district'].str.lower().str.replace('_', '-').str.replace(' ', '-')

plot_data = {'District': [],
             'Average cost': []}

for district in df['start_district'].unique():
    plot_data['District'].append(district)
    plot_data['Average cost'].append(df[df['start_district'] == district]['drive_cost'].sum() / df[df['start_district'] == district].shape[0])

sns.barplot(x='District', y='Average cost', data=plot_data)
plt.show()