import os
from utils import *
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation

# specify parameters
data_dir = './data'
covid_file_name = 'state_daily_usa.csv'

# get cases in India
cases_df = pd.read_csv(os.path.join(data_dir, covid_file_name))

# rextract necessary columns
cases_df = cases_df[['date', 'state', 'cases']]

# convert first column to date
cases_df['date'] = pd.to_datetime(cases_df['date'], format='%Y-%m-%d')
cases_df = cases_df

# dates for 2020 - march
# cases_df = cases_df[cases_df['date'].dt.year == 2020]
# cases_df = cases_df[cases_df['date'].dt.month > 2]
cases_df = cases_df[cases_df['date'] > '2020-03-09']

# extract confirmed cases for each state
cases_ny = cases_df[cases_df['state'] == 'New York']
cases_nj = cases_df[cases_df['state'] == 'New Jersey']
cases_ma = cases_df[cases_df['state'] == 'Massachusetts']
cases_il = cases_df[cases_df['state'] == 'Illinois']
cases_ca = cases_df[cases_df['state'] == 'California']
cases_pa = cases_df[cases_df['state'] == 'Pennsylvania']
cases_mi = cases_df[cases_df['state'] == 'Michigan']


# colors
colors = dict(zip(
    ['New York', 'New Jersey', 'Massachusetts', 'Illinois', 'California', 'Pennsylvania', 'Michigan'],
    ['#adb0ff', '#ffb3ff', '#90d595', '#e48381',
     '#aafbff', '#f7bb5f', '#eafb50']))

# plot horizontal bar graph and customize
fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(index):
    # create sorted lists
    state = ['New York', 'New Jersey', 'Massachusetts', 'Illinois', 'California', 'Pennsylvania', 'Michigan']
    cases = [int(cases_ny.iloc[index].cases), int(cases_nj.iloc[index].cases), int(cases_ma.iloc[index].cases), 
            int(cases_il.iloc[index].cases), int(cases_ca.iloc[index].cases), int(cases_pa.iloc[index].cases), int(cases_mi.iloc[index].cases)]   
    cases, state = (list(t) for t in zip(*sorted(zip(cases, state))))

    ax.clear()
    ax.barh(state, cases, color=[colors[x] for x in state])
    dx = np.max(cases) / 200
    for i, (value, name) in enumerate(zip(cases, state)):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom') # state
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center') # cases
    ax.text(1, 0.4, cases_ny.iloc[index].date.date(), transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Cases', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.1, 'Corona Virus cases in India in top 7 States', transform=ax.transAxes, size=24, weight=600, ha='left')
    plt.box(False)

# print(len(cases_ny)-7)
# print(cases_ny.head())

# # generate animations
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(0, len(cases_ny)))
animator.save('./results/animations/usa_cases.gif', writer='imagemagick', fps=3)

# # ref: https://towardsdatascience.com/bar-chart-race-in-python-with-matplotlib-8e687a5c8a41