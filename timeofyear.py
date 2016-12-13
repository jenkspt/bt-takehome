
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
	df['hours'] = df[date_col].dt.hour
	hour_of_day = df[['frequency', 'hours']].groupby('hours').sum()['frequency']
	return hour_of_day.plot(**kwargs)



# def dayofyear_to_date(series):
# 	return datetime(2016, 1, 1) - series.apply(lambda d: timedelta(d-1))

# def dayofweek_frequency(df, date_col='CreationDate'):
# 	df = df.set_index(date_col)
# 	df['frequency'] = np.zeros(len(df))
# 	return df.groupby(by=df.index.dayofweek).count()['frequency']

# def plot_week(df, title=None, **kwargs):
# 	days={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
# 	series = dayofweek_frequency(df)
# 	week_avg, weekend_avg = series.ix[:4].mean(), series.ix[5:].mean()
# 	series = series.rename(index=days)
# 	series.name = title
# 	# Percent decrease of frequency for weekends
# 	percent_decrease = ((week_avg-weekend_avg)/week_avg)*100
# 	ax = series.plot(**kwargs)
# 	ax.legend()
# 	ax.text(.5, .5, '{:.2f}% less on average weekends'.format(percent_decrease))


if __name__ == '__main__':
	posts_df = pd.read_pickle('data/pickle/posts_df.pkl')
	# Comments
	# c_df = pd.read_pickle('data/pickle/comments_df.pkl')
	# c_df = c_df.set_index('CreationDate')
	# Just questions posts
	# q_df = posts_df[posts_df.PostTypeId == 1]
	# q_df = q_df.set_index('CreationDate')
	# # Just answer posts
	# a_df = posts_df[posts_df.PostTypeId == 2]
	# a_df = a_df.set_index('CreationDate')

	# fig, axs = plt.subplots(3, 1)
	# plt.suptitle('Day Of Year Frequency')
	# plot_time_bin(q_df, q_df.CreationDate.dt.dayofyear, index_map = title='Questions', ax=axs[0], color='darkorange')
	# # plot_time_bin(a_df, a_df.index.year, title='Answers', ax=axs[1], color='darkgreen')
	# # plot_time_bin(c_df, c_df.index.date, title='Comments', ax=axs[2], color='darkblue', )
	# plt.show()

	# Exclude year 2009 due to negligable # of posts
	fig, ax = plt.subplots(1,1)
	title='Posting Frequency (questions and answers)'
	plot_years(posts_df[posts_df.CreationDate.dt.year >= 2010], title=title, ax=ax)
	plt.savefig('plots/timeofyear_frequency.png')