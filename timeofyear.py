
import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta

import matplotlib.pyplot as plt
import seaborn as sns

# 3. How do posts vary by time of year and time of day?
def plot_years(df, date_col='CreationDate', period='7D', **kwargs):
	# Column to count the number of posts in goupby
	df['frequency'] = np.ones(len(df))
	# group post frequency into daily bins
	df['day'] = df[date_col].dt.to_period('1d')
	df = df[['frequency','day']]
	day_bins = df.groupby(df.day).count()['frequency'] # Returns a Series
	# Split the dataframe by year	
	year_groups = list(day_bins.groupby(day_bins.index.year))
	for year, year_data in year_groups:
		year_data.name = year
		# Set all the years to 2016 so I can plot them in same date range on plot
		year_data.index = year_data.index.map(lambda d: datetime(2016, d.month, d.day))
	# Create a new dataframe with years as columns
	years = pd.concat([year_data for year, year_data in year_groups], axis=1)
	# Smooth the plot by the set period
	years = years.resample(period).sum().rolling(window=3).mean()
	ax = years.plot(**kwargs)
	ax.set_ylabel(period + ' ' + 'Frequency')
	return ax

""" This is not especially useful because posts do not have timezone information """
def plot_hourofday(df, date_col='CreationDate', **kwargs):
	df['frequency'] = np.ones(len(df))
	df['hour'] = df[date_col].dt.hour
	hour_of_day = df[['frequency', 'hour']].groupby('hour').sum()['frequency']/len(df)
	ax = hour_of_day.plot(**kwargs)
	ax.set_ylabel('Avg Frequency (per hour)')
	return ax

if __name__ == '__main__':
	posts_df = pd.read_pickle('data/pickle/posts_df.pkl')

	#Exclude year 2009 due to negligable # of posts
	fig, ax = plt.subplots(1,1)
	title='Posting Frequency (questions and answers)'
	plot_years(posts_df[posts_df.CreationDate.dt.year >= 2010], title=title, ax=ax)
	plt.savefig('plots/timeofyear_frequency.png')

	fig, ax = plt.subplots(1,1)
	title='Average Posting Frequency Per Hour (for all time)'
	plot_hourofday(posts_df[posts_df.CreationDate.dt.year >= 2010], title=title, ax=ax)
	plt.savefig('plots/timeofday_frequency.png')