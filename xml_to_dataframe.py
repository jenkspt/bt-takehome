"""
Convert xml to dataframes and save as pickle files in 'data/pickle/'
"""

import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

from datetime import datetime
from collections import defaultdict

# 1. What are the top topics that users post about?
def get_tags_dataframe(posts):
	"""The tags of each post are used as topics. Each post has several metrics for evaluating the topic"""
	topics = dict()
	# Topic metrics to grap from each post
	fields = ['ViewCount', 'Score', 'CommentCount', 'AnswerCount', 'FavoriteCount'] # Need list (not set) so order is as shown
	for post in posts:
		attr = post.attrib
		# '1' is a question post. Only questions have tags
		if attr['PostTypeId'] == '1':
			# Some of the fields are missing from certain posts -> replace missing values with 0
			# first element of 'update' is the frequency count of the tag
			update = (1, *(int(attr[field]) if field in attr else 0 for field in fields))
			# A typical tags field  	'Tags': '<power-management><notification>'
			for tag in attr['Tags'].strip('<>').split('><'):
				if tag in topics:
					# update the (count, FavoriteCount, CommentCount, Score , ViewCount) for each tag
					topics[tag] = tuple(old + new for old, new in zip(topics[tag], update))
				else:
					topics[tag] = update
	return pd.DataFrame(topics, index=['Count']+fields).T # Transpose so tags are the index

def docs_to_dataframe(docs, field_types):
	"""input:
			docs: flat xml document tree object (posts, comments or users)
			field_types: mapping of field name to function which returns correct datatype
	"""
	# Apply datatype mapping if key exists or return None
	dtype_map = lambda doc, key, dtype: dtype(doc[key]) if key in doc else None
	data = defaultdict(list)
	for doc_object in docs:
		doc = doc_object.attrib
		# Converts fields to appropriate datatypes and sets field as 'None' if it doesn't exist in document
		iterator = ((key, dtype_map(doc, key, dtype)) for key, dtype in field_types.items())
		for k, v in iterator:
			data[k].append(v)
	return pd.DataFrame(data)

if __name__ == '__main__':
	# The format that is used in all the xml files
	format_date = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f')
	root = ET.parse('data/xml/Posts.xml').getroot()

	get_tags_dataframe(root).to_pickle('data/pickle/topics_df.pkl')

	# key -> dtype mapping
	post_fields = {'CreationDate':format_date, 'LastActivityDate':format_date, 
		'LastEditDate':format_date, 'ClosedDate':format_date, 'DeletionDate':format_date,
		'CommunityOwnedDate':format_date, 'Id':int, 'PostTypeId':int, 'ParentId':int, 
		'OwnerUserId':int, 'LastEditorUserId':int, 'AcceptedAnswerId':int, 
		'AnswerCount':int, 'CommentCount':int, 'FavoriteCount':int, 'ViewCount':str, 
		'Score':int, 'Title':str, 'Tags':str, 'Body':str,   
		'LastEditorDisplayName':str, 'OwnerDisplayName':str}
	docs_to_dataframe(root, post_fields).to_pickle('data/pickle/posts_df.pkl')
	# del root
	# root = ET.parse('data/xml/Comments.xml').getroot()
	# comment_fields = {'CreationDate':format_date, 'Id':int, 'PostId':int, 'Score':int, 'Text':str, 'UserId':int}
	# docs_to_dataframe(root, comment_fields).to_pickle('data/pickle/comments_df.pkl')
