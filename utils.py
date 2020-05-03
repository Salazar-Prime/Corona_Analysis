import pandas
import numpy as np
def dataframe_for_day(df, date):
	# Get a data frame only for today
	return df[df.date == date]

def data_quality_check(df):
	# replace values with NaN for each column
	df['cases'][(df['cases'] <  0)] = np.NaN
	df['deaths'][(df['deaths'] <  0)] = np.NaN
	return df