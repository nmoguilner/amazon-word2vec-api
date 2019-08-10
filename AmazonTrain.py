# Author: Nicolás Francisco Moguilner Reh <nicolas.moguilner@endava.com>

from gensim.models import Word2Vec
import Helpers

items_by_reviewer_id = Helpers.load_all_txt_sentences('data/Preprocessed/by_reviewer_id')
items_by_categories = Helpers.load_all_txt_sentences('data/Preprocessed/by_categories')
items_by_also_bought = Helpers.load_all_txt_sentences('data/Preprocessed/also_bought')
items_by_bought_together = Helpers.load_all_txt_sentences('data/Preprocessed/bought_together')
items_by_buy_after_viewing = Helpers.load_all_txt_sentences('data/Preprocessed/buy_after_viewing')
asin_title_dict = Helpers.load_json_dict('data/Preprocessed/asin_title_dict/asin_title_dict.json')

feature_size = 300  # Word vector dimensionality
window_context = 6  # Context window size
min_word_count = 1  # Minimum word count
sample = 1e-2  # Downsample setting for frequent words
negative_samples = 10
workers = 10
epochs = 50

training_sample = items_by_reviewer_id + items_by_categories + items_by_also_bought + items_by_bought_together \
                  + items_by_buy_after_viewing

print('training started...')
model = Word2Vec(training_sample,
                 workers=workers,
                 window=window_context,
                 min_count=min_word_count,
                 size=feature_size,
                 sample=sample,
                 negative=negative_samples,
                 iter=epochs)

model.save('static/data/word2vec.model')
print('model saved!')
