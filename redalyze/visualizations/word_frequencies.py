# Count word frequencies in title
import nltk
import pandas as pd
from itertools import chain
from collections import Counter
from nltk.corpus import stopwords

nltk.download('stopwords')
  
def word_frequencies(transformed_df):
  all_titles = transformed_df['title'].dropna()
  
  # Title cleansing: removing punctiation, stopwords, special characters
  all_titles = all_titles.str.lower()
  all_titles = all_titles.str.replace(r'[^\w\s]', '', regex=True)
  
  stop_words = set(stopwords.words('english'))
  all_titles = all_titles.apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
  
  # Tokenize: spliting each title into individual words
  tokenized_words = list(chain.from_iterable(all_titles.str.split()))
  
  # Counting word frequencies
  word_counts = Counter(tokenized_words)
  filtered_counts = {word: count for word, count in word_counts.items() if count >= 3}
  
  frequency_df = pd.DataFrame(list(filtered_counts.items()), columns=["word", "frequency"])

  return frequency_df
