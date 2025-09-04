from google.colab import files

uploaded = files.upload()import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

import io



df = pd.read_csv(io.BytesIO(uploaded['fcc-forum-pageviews.csv']), parse_dates=['date'])

df.set_index('date', inplace=True) df = df[(df['value']>=df['value'].quantile(0.025)) &

        (df['value']<=df['value'].quantile(1-0.025))] def draw_line_plot():

  fig, ax = plt.subplots(figsize=(15, 6))

  ax.plot(df.index, df['value'], color='red', linewidth=1)

  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

  ax.set_xlabel("Date")

  ax.set_ylabel("Page Views")


draw_line_plot() 

def draw_bar_plot():

  df_bar = df.copy()

  df_bar['year']=df_bar.index.year

  df_bar['month']=df_bar.index.month

  df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

  df_bar['month']= pd.to_datetime(df_bar['month'], format='%m').dt.strftime('%B')



  month_order= ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']

  df_bar['month']= pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

  df_bar = df_bar.sort_values('month')



  fig = sns.catplot(x='year', y='value', hue='month', data=df_bar, kind='bar', height=6, aspect=1.5)



  fig.set_axis_labels("Years", "Average Page Views")

  fig._legend.set_title("Months")


draw_bar_plot()

def draw_box_plot():

  df_box = df.copy()

  df_box['year']=df_box.index.year

  df_box['month']=df_box.index.month



  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))



  sns.boxplot(x='year', y='value', data=df_box, ax=ax1)

  ax1.set_title("Year-wise Box Plot (Trend)")

  ax1.set_xlabel("Year")

  ax1.set_ylabel("Page Views")



  df_box['month']= pd.to_datetime(df_box['month'], format='%m').dt.strftime('%b')



  month_order= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']



  sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)

  ax2.set_title("Month-wise Box Plot (Seasonality")

  ax2.set_xlabel("Month")

  ax2.set_ylabel("Page Views")

draw_box_plot()
