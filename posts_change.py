import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def get_post_tags_df(df):
	"""Pull out tags into seperate dataframe with Id as join index"""
	b = pd.DataFrame(df.Tags.map(lambda tags: tags.strip('<>').split('><')).tolist(), \
		index=df.Id).stack()
	b = b.reset_index()[[0, 'Id']] # Tags variable is currently labeled 0
	b.columns = ['Tag', 'Id'] # renaming Tags
	return b

def get_tag_metrics_df(posts_df, tags_df):
	""" Join tags with posts on post id to get metrics"""
	tags_df['Count'] = np.ones(len(tags_df))
	columns = ['Id', 'CreationDate', 'ViewCount', 'Score', \
			   'AnswerCount', 'CommentCount', 'FavoriteCount']
	return pd.merge(posts_df[columns], tags_df, on='Id')

def plot_change(tags_df, metric='Count',tag_column='Tag', \
	date_col='CreationDate', period='7d', window=14, **kwargs):
	"""Plot the yearly frequency of OS tagged questions.
	metric: Tag metric to plot (i.e. Count, ViewCount, FavoriteCount ...)
	period: period to bin counts
	window: sliding average for smoothing
	"""
	tags_df = tags_df.copy().set_index(date_col)
	# Bin by day
	tags_df = tags_df.groupby([tags_df.index.to_period('1d'), tag_column]).sum().reset_index()
	# create a column with each os release
	tags_df = tags_df.pivot(index=date_col, columns=tag_column, values=metric)
	ax = tags_df.resample(period).sum().fillna(0).rolling(window=window).mean().plot(**kwargs)
	ax.set_ylabel('Frequency ({})'.format(period))
	return ax

def get_yearly_top_tags_df(df, k=4):
	""" Returns a DataFrame with the union of the top tags for each year, with OS
	tags removed."""
	# Strip out OS tags
	df = df[tags_df.Tag.str.match('^[0-9]{2}\.[0-9]{2}$')^1]
	tags = set() # Union of the top tags for each year
	for year, data in df.groupby(df.CreationDate.dt.year):
		data = data.reset_index()
		# Top tags for each year
		tags = tags.union(set(data.groupby('Tag').sum().reset_index().sort_values(by='Count')[-k:].Tag))

	df = df.set_index('Tag')
	return df.ix[tags].reset_index()



if __name__ == '__main__':
	posts_df = pd.read_pickle('data/pickle/posts_df.pkl')
	# Only Question posts
	posts_df = posts_df[posts_df.PostTypeId == 1]
	# Extract tags from posts
	tags_df = get_tag_metrics_df(posts_df, get_post_tags_df(posts_df))[['Tag','Count','CreationDate']]

	# Plot OS tagged questions over time
	# Get only yearly os releases
	fig, ax = plt.subplots(1,1)
	title='OS Tagged Question Posts'
	tag_column='OS Releases'

	os_mask = tags_df.Tag.str.match('^[0-9]{2}\.[0-9]{2}$')
	os_tags_df = tags_df[os_mask]
	os_tags = set(os_tags_df.index)
	os_tags_df[tag_column] = os_tags_df.Tag.str[:3]

	plot_change(os_tags_df, tag_column=tag_column, title=title, ax=ax)
	fig.savefig('plots/os_questions_yearly.png')


	# Top Year Tags Plot
	fig, ax = plt.subplots(1,1)
	title='Yearly Top Tag Change'

	top_tags_df = tags_df[tags_df.CreationDate.dt.year > 2010]
	top_tags_df = get_yearly_top_tags_df(top_tags_df, k=1)

	plot_change(top_tags_df, title=title, tag_column='Tag', ax=ax)
	fig.savefig('plots/tag_questions_yearly.png')	