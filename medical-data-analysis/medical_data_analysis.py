uploaded = files.upload() 
import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

import io

df = pd.read_csv(io.BytesIO(uploaded['medical_examination.csv'])) height_in_meters = df['height']/100

bmi=df['weight']/(height_in_meters**2)

df['overweight'] = (bmi>25).astype(int)


df['cholesterol'] = (df['cholesterol'] >1).astype(int)

df['gluc'] = (df['gluc'] >1).astype(int)


df_cat = pd.melt(df, id_vars = ['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco','active','overweight'])

df_cat = df_cat.rename(columns={'variable': 'categories'})

fig = sns.catplot(x='categories', hue='value', col= 'cardio', data=df_cat, kind = 'count')

fig = fig.fig df_heat = df[(df['ap_lo']<=df['ap_hi']) &

              (df['height']>=df['height'].quantile(0.025)) &

              (df['height']<=df['height'].quantile(0.975)) &

              (df['weight']>=df['weight'].quantile(0.025)) &

              (df['weight']<=df['weight'].quantile(0.975))

]

corr = df_heat.corr()

mask = np.triu(corr)



fig, ax = plt.subplots(figsize=(12,12))

sns.heatmap(corr, linewidths=1, mask=mask, fmt= ".1f", square = True, cbar_kws={"shrink": .5}, annot=True, center=0)
