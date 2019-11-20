# Author: Nicolás Francisco Moguilner Reh <nicolas.moguilner@endava.com>

import Helpers
import time
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import AmazonModelEpochLogger
import multiprocessing


def plot_loss():
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    plt.scatter(AmazonModelEpochLogger.epochs_list, AmazonModelEpochLogger.historic_loss)
    plt.title('Model Training Loss convergence')
    plt.plot(AmazonModelEpochLogger.epochs_list, AmazonModelEpochLogger.historic_loss, 'xb-')
    plt.savefig('data/model_loss.png')
    plt.show()



start_time = time.time()

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
workers = multiprocessing.cpu_count()
epochs = 50
alpha = 0.025

training_sample = items_by_reviewer_id + items_by_categories + items_by_also_bought + items_by_bought_together \
                  + items_by_buy_after_viewing

print('training started...')
model = Word2Vec(training_sample,
                # alpha = alpha,
                 workers=workers,
                 window=window_context,
                 min_count=min_word_count,
                 size=feature_size,
                 sample=sample,
                 negative=negative_samples,
                 iter=epochs,
                 compute_loss=True,
                 callbacks=[AmazonModelEpochLogger.EpochLogger()])

# save word2vec model to a file
model.save('static/data/word2vec.model')

elapsed_time = time.time() - start_time
print('Training finished. Elapsed time: %d s.' % elapsed_time)

# plot historical loss
plot_loss()

with open('data/Preprocessed/elapsed_time_log', 'a') as f:
    f.write("Training: %d s. (%d min)\n" % (elapsed_time, elapsed_time/60))

