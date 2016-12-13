
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

def get_top_tags(df, k=15):
	"""Find all the topics that are present in the top k topics for each column"""
	topics_lst = []
	for col in df.columns:
		top_k = set(df.sort_values(by=col, ascending=False).head(k).index)
		topics_lst.append(top_k)

	# Return the topics the appear in the top 20 for each column(metric)
	return list(set.intersection(*topics_lst))

def get_os_tags(df):
	"""Returns all Ubuntu release tags tags (i.e. 14.04)"""
	mask = df.index.str.match('^[0-9]{2}\.[0-9]{2}$')
	return list(df[mask].index)

def group_os_release(df):
	"""returns dataframe
		grouped by major version release, 
		i.e. 14.04, 14.10 becomes 14"""
	os = get_os_tags(df)
	df = df.ix[os]
	return df.groupby([df.index.str[:2]]).sum()


def plot_top_tags(df, sort_by=None, **kwargs):
	"""input: Dataframe of tags (index) to plot as bar chart"""
	# ex. if mean = 4320, then scale = 100
	get_scale = lambda x : 10**(len(str(int(x.max()))) - 1)
	# scale all columns to a similar range
	scales = [get_scale(df[col]) for col in df.columns]
	# Add scale factor to column names so it will be included in plot legend
	if sort_by:
		df = df.sort_values(by=sort_by, ascending=False)
	df = df.rename(columns={col:'{} x {:.0E}'.format(col, 1/scale) for col, scale in zip(df.columns, scales)})
	return (df/scales).plot.bar(**kwargs)


if __name__ == '__main__':
	df = pd.read_pickle('data/pickle/topics_df.pkl')

	# 1. What are the top topics that users post about?
	columns = ['Count', 'ViewCount']
	top_topics = get_top_tags(df[columns])
	fig, ax1 = plt.subplots(1,1)
	ax1 = plot_top_tags(df.ix[top_topics, columns], sort_by='ViewCount', title='Top Topics', ax=ax1)
	fig.savefig('plots/top_topics.png')

	# OS related posts
	fig, ax2 = plt.subplots(1,1)
	ax2 = plot_top_tags(group_os_release(df), title='Major Ubuntu Releases', ax=ax2)
	fig.savefig('plots/os_releases.png')

	# Top Activity Bar Chart: Activity metrics = 'CommentCount', 'AnswerCount', 'FavoriteCount'
	columns = ['CommentCount', 'AnswerCount', 'FavoriteCount']
	top_activity = get_top_tags(df[columns])
	fig, ax3 = plt.subplots(1,1)
	title = 'Topics Generating The Most Activity'
	ax3 = plot_top_tags(df.ix[top_activity, columns], sort_by='CommentCount', title=title, ax=ax3)
	fig.savefig('plots/top_activity.png')
	
