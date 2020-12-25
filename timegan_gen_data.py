import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from scipy import stats

# file_size = input('Single or file sequence:')
# if file_size == 'single':
data = pd.read_csv(f'denorm_internet4259wk1().csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])

# for j in range(1, 2):
#     path = f'/home/haris/TimeGAN/generated data/Week_{j}/lstm24'
#     dirListing = os.listdir(path)
#     print(len(dirListing))
#     for i in range(1, len(dirListing)):
#         df = pd.read_csv(f'generated data/Week_{j}/lstm24/lstm24_wk{j}_{i}.csv', usecols=[1, 2, 3, 4, 5, 6])
#         data = data.append(df)
data[['tweets', 'conditions', 'coverage', 'Days', 'Hours', 'dayofyear']] = data[['tweets',
                                                                                 'conditions', 'coverage', 'Days',
                                                                                 'Hours', 'dayofyear']].round(decimals=1).astype(int)
# data[['tweets', 'conditions', 'coverage', 'Days']] = data[['tweets', 'conditions',
#                                                            'coverage', 'Days']].apply(np.rint)
# data['dayofyear_rounded'] = data['dayofyear'].apply(np.rint)
# data['doy_error'] = data['dayofyear'] - data['dayofyear_rounded']
# mask = data.where((abs(data['doy_error']) >= 0.4) & (abs(data['doy_error']) <= 0.6))
# data_d = data[mask]
# data = data.drop(data_d.index, axis=0)
data.reset_index(drop=True, inplace=True)
data['datetime'] = [pd.to_datetime(f"2013{j[0]} {j[1]}:00:00", format="%Y%j %H:%M:%S") for j in zip(data['dayofyear'], data['Hours'])]
# data.sort_values('datetime', inplace=True)
data_t = data.groupby('datetime').agg(np.mean)

real_dat = pd.read_csv('data/internet_timegan_4259_dates.csv', usecols=[2, 3, 4], parse_dates=['datetime'])
real_dat = real_dat.assign(datetime=real_dat.datetime.dt.floor('H'))
real_dat = real_dat.groupby('datetime').mean()
real_dat = real_dat['2013-11-01 00:00:00': '2013-11-08 00:00:00']

# real_dat['tweets_scaled'] = stats.zscore(real_dat['tweets'])
# plt.plot(real_dat['tweets_scaled'])
# plt.show()

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
ax1.plot(data_t.index, data_t['internet'])
ax2.plot(real_dat.index, real_dat['internet'])
fig.autofmt_xdate(ha='center', rotation=30)
fig.suptitle('Generated vs Real (internet) Week 1', fontsize=18)
plt.xlabel('Date time', fontsize=16)
ax1.set_title('Generated', fontsize=13)
ax2.set_title('Real', fontsize=13)
ax1.set_ylabel('Number of connections', fontsize=14)
ax2.set_ylabel('Number of connections', fontsize=14)
plt.show()
print(-1)
