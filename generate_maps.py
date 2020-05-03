import pandas as pd
import numpy as np
import plotly.express as px
import plotly
import os
from utils import *

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



###### create a bubble plots on map with plotly express ####

# daily cases
fig1 = px.scatter_geo(cases_df, 
				    size='cases',
				    locations='countryCode',
				    projection='natural earth',
				    title='World COVID-19 Daily Cases',
				    hover_name='country',
				    color='continent',
				    animation_frame='date_str')
fig1.write_html("./results/interactive_maps/daily_cases.html")

# cumulative cases
fig2 = px.scatter_geo(cases_df, 
				    size='cum_cases',
				    locations='countryCode',
				    projection='natural earth',
				    title='World COVID-19 Cumulative Cases',
				    hover_name='country',
				    color='continent',
				    animation_frame='date_str')
fig2.write_html("./results/interactive_maps/cumulative_cases.html")

# daily deaths
fig3 = px.scatter_geo(cases_df, 
				    size='deaths',
				    locations='countryCode',
				    projection='natural earth',
				    title='World COVID-19 Daily Deaths',
				    hover_name='country',
				    color='continent',
				    animation_frame='date_str')
fig3.write_html("./results/interactive_maps/daily_deaths.html")

# cumulative deaths
fig4 = px.scatter_geo(cases_df, 
				    size='cum_deaths',
				    locations='countryCode',
				    projection='natural earth',
				    title='World COVID-19 Cumulative Deaths',
				    hover_name='country',
				    color='continent',
				    animation_frame='date_str')
fig4.write_html("./results/interactive_maps/cumulative_deaths.html")


# debug
print(cases_df.tail(10))