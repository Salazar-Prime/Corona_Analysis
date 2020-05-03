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
covid_file_name = 'state_daily_india.csv'

# get cases in India
cases_df = pd.read_csv(os.path.join(data_dir, covid_file_name))

# rename for easier manipulation
cases_df = cases_df[['Date', 'Status', 'MH', 'GJ', 'DL', 'RJ', 'UP', 'MP', 'TN']]
# cases_df = cases_df.drop('TT', axis=1)
cases_df = cases_df.rename(columns={'Date': 'date',
                                    'Status': 'status'})

# convert first column to date
cases_df['date'] = pd.to_datetime(cases_df['date'], format='%d-%b-%y')

# extract confirmed cases
cases_df = cases_df[cases_df['status'] == 'Confirmed']

# remove status column
cases_df = cases_df.drop('status', axis=1)

# cumulative sums for each states
cases_df['MH'] = cases_df['MH'].cumsum(skipna=True)
cases_df['GJ'] = cases_df['GJ'].cumsum(skipna=True)
cases_df['DL'] = cases_df['DL'].cumsum(skipna=True)
cases_df['RJ'] = cases_df['RJ'].cumsum(skipna=True)
cases_df['UP'] = cases_df['UP'].cumsum(skipna=True)
cases_df['MP'] = cases_df['MP'].cumsum(skipna=True)
cases_df['TN'] = cases_df['TN'].cumsum(skipna=True)

# convert to list
dff = [cases_df.columns.values.tolist()] + cases_df.values.tolist()

# colors
colors = dict(zip(
    ['MH', 'GJ', 'DL', 'RJ', 'UP', 'MP', 'TN'],
    ['#adb0ff', '#ffb3ff', '#90d595', '#e48381',
     '#aafbff', '#f7bb5f', '#eafb50']))

# plot horizontal bar graph and customize
fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(index):
    # create sorted lists
    cases, state = (list(t) for t in zip(*sorted(zip(dff[index][1:], dff[0][1:]))))
    ax.clear()
    ax.barh(state, cases, color=[colors[x] for x in state])
    dx = np.max(cases) / 200
    for i, (value, name) in enumerate(zip(cases, state)):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom') # state
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center') # cases
    ax.text(1, 0.4, dff[index][0].date(), transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
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

# generate animations
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1, len(dff)))
animator.save('./results/animations/india_cases.gif', writer='imagemagick', fps=3)
