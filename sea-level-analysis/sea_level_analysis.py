google.colab import files

uploaded = files.upload() import pandas as pd

import matplotlib.pyplot as plt

from scipy.stats import linregress

import numpy as np

import io



df_2 = pd.read_csv(io.BytesIO(uploaded['epa-sea-level.csv'])) plt.scatter(df_2['Year'], df_2['CSIRO Adjusted Sea Level'])

slope, intercept, r_value, p_value, std_err = linregress(df_2['Year'], df_2['CSIRO Adjusted Sea Level'])

years_extended = np.arange(df_2['Year'].min(), 2051)

plt.plot(years_extended, intercept + slope*years_extended, color='red', label='Line of Best Fit (All Data)')

df_2000 = df_2[df_2['Year']>=2000]

slope_2000, intercept_2000, r_value_2000, p_value_2000, std_err_2000 = linregress(df_2000['Year'], df_2000['CSIRO Adjusted Sea Level'])

years_extended_2000 = np.arange(2000, 2051)

plt.plot(years_extended_2000, intercept_2000 + slope_2000*years_extended_2000, color='green', label='Line of Best Fit (2000 Onwards)')

plt.xlabel('Year')

plt.ylabel('Sea level (inches)')

plt.title('Rise in Sea Level')

plt.legend()
