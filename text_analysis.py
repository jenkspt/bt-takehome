import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LinearRegression

from sklearn.pipeline import Pipeline, make_pipeline

if __name__ == '__main__':
	posts_df = pd.read_pickle('data/pickle/posts_df.pkl')
	q_df = posts_df[posts_df.PostTypeId == 1]

	y = q_df['FavoriteCount']
	X = q_df['Title'] + '\n' + q_df['Body']
	vectors = TfidfVectorizer(stop_words='english').fit_transform(X)
