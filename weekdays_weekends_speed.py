import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, mannwhitneyu


def is_weekend(arg):
    arg = datetime.datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
    return 'weekend' if arg.weekday() >= 5 else 'weekday'


df = pd.read_csv('rides_final.csv', sep=',', encoding='utf-8',
                 skipinitialspace=True, keep_default_na=False, na_values=('', ' '), decimal=',').fillna('NaN')

df['speed'] = df['speed'].astype(float)
df['is_weekend'] = df['start_date'].apply(lambda arg: is_weekend(arg))


lower_bound = df['speed'].quantile(q=0.01)
upper_bound = df['speed'].quantile(q=0.99)
df = df[(lower_bound < df['speed']) & (df['speed'] < upper_bound)]

weekdays = df[df['is_weekend'] == 'weekday']
weekends = df[df['is_weekend'] == 'weekend']

plt.figure(0)
sns.distplot(weekdays['speed'], hist_kws={'color': 'r'}).set(title='weekdays')

plt.figure(1)
sns.distplot(weekends['speed'], hist_kws={'color': 'b'}).set(title='weekends')

plt.figure(2)
sns.boxplot(x='is_weekend', y='speed', data=df)
plt.show()

weekdays_test = weekdays['speed'].sample(20000)
weekends_test = weekends['speed'].sample(20000)

print(shapiro(weekdays_test))
print(shapiro(weekends_test))

print(mannwhitneyu(weekdays_test, weekends_test, alternative='two-sided'))