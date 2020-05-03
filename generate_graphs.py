import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from utils import *
import datetime

# specify parameters
data_dir = './data'
covid_file_name = 'covid_19_cases_european.csv'

# get total global cases
cases_df = pd.read_csv(os.path.join(data_dir, covid_file_name))

# retain useful columns and rename for easier manipulation
cases_df = cases_df[['dateRep', 'cases', 'deaths', 'countriesAndTerritories', 'geoId', 'countryterritoryCode', 'popData2018', 'continentExp']]
cases_df = cases_df.rename(columns={'dateRep': 'date',
								    'countriesAndTerritories': 'country',
								    'countryterritoryCode': 'countryCode',
								    'continentExp': 'continent'})

# convert first column to date
cases_df['date'] = pd.to_datetime(cases_df['date'], format='%d/%m/%Y')

# date to date string
cases_df['date_str'] = cases_df.date.dt.strftime('%Y%m%d')
cases_df = cases_df.sort_values(by=['date_str'])

# data quality check
cases_df = data_quality_check(cases_df)
cases_df = cases_df.dropna()

# cumulative cases and deaths
cases_df['cum_cases'] = cases_df.groupby(['country'])['cases'].apply(lambda x: x.cumsum())
cases_df['cum_deaths'] = cases_df.groupby(['country'])['deaths'].apply(lambda x: x.cumsum())

# dates for 2020 - february
cases_df = cases_df[cases_df['date'].dt.year == 2020]
cases_df = cases_df[cases_df['date'].dt.month > 1]


# USA dataframe
usa_df = cases_df[cases_df['geoId'] == 'US']
print(usa_df[usa_df['date'] == '2020-04-09'])

# India dataframe
india_df = cases_df[cases_df['geoId'] == 'IN']
print(india_df[india_df['date'] == '2020-04-09'])


########################### Plotting #############################################
## First we create the plot and add to trace
## Then we create a drop down list to set 
## visibility of traces

# Initialize figure
fig = go.Figure()

# Add Traces - USA Cases
fig.add_trace(
    go.Bar( x=usa_df['date'],
           		y=usa_df['cum_cases'],
                name="USA Cases",
                showlegend=True,
                visible=True))

# Add Traces - USA Deaths positive
fig.add_trace(
    go.Bar( x=usa_df['date'],
           		y=usa_df['cum_deaths'],
                name="USA Deaths",
                marker_color='rgb(255,0,0)',
                showlegend=True,
                visible=False))

# Add Traces - USA Deaths negative
fig.add_trace(
    go.Bar( x=usa_df['date'],
           		y=-1*usa_df['cum_deaths'],
                name="USA Deaths",
                marker_color='rgb(255,0,0)',
                showlegend=True,
                visible=False))

# Add Traces - India Cases
fig.add_trace(
    go.Bar( x=india_df['date'],
           		y=india_df['cum_cases'],
                name="India Cases",
                showlegend=True,
                visible=False))

# Add Traces - India Deaths positive
fig.add_trace(
    go.Bar( x=india_df['date'],
           		y=india_df['cum_deaths'],
                name="India Deaths",                
                marker_color='rgb(255,0,0)',
                showlegend=True,
                visible=False))

# Add Traces - India Deaths negative
fig.add_trace(
    go.Bar( x=india_df['date'],
           		y=-1*india_df['cum_deaths'],
                name="India Deaths",                
                marker_color='rgb(255,0,0)',
                showlegend=True,
                visible=False))


# this tool toggles the graphs 
fig.update_layout(barmode='relative', title_text="USA - Cases",
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="USA - cases",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False]},
                           {"title": "USA - Cases",
                            "annotations": []}]),
                dict(label="USA - Deaths",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False]},
                           {"title": "USA - Deaths",
                            "annotations": []}]),
                dict(label="USA - cases and deaths",
                     method="update",
                     args=[{"visible": [True, False, True, False, False, False]},
                           {"title": "USA - Cases and Deaths",
                            "annotations": []}]),
                dict(label="India - cases",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False]},
                           {"title": "India - Cases",
                            "annotations": []}]),
                dict(label="India - Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False]},
                           {"title": "India - Deaths",
                            "annotations": []}]),
                dict(label="India - Cases and Deaths",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, True]},
                           {"title": "India - Cases and Deaths",
                            "annotations": []}])
            ]),
        )
    ])

# save figure
fig.write_html("./results/graphs/India_USA_cases_deaths.html")
