import pandas as pd
import Helpers
import time

start_time = time.time()

all_meta_reviews = pd.DataFrame()
min_score = 3
files = [
    ('reviews_Electronics_5.json.gz', 'meta_Electronics.json.gz'),
    ('reviews_Musical_Instruments_5.json.gz', 'meta_Musical_Instruments.json.gz'),
    ('reviews_Movies_and_TV_5.json.gz', 'meta_Movies_and_TV.json.gz'),
    ('reviews_Grocery_and_Gourmet_Food_5.json.gz', 'meta_Grocery_and_Gourmet_Food.json.gz'),
    ('reviews_Home_and_Kitchen_5.json.gz', 'meta_Home_and_Kitchen.json.gz')
]

for tuple in files:
    print('Preprocessing: %s - %s...' % (tuple[0], tuple[1]))
    amazon_reviews_df = Helpers.get_df('data/Datasets/%s' % tuple[0])[['reviewerID', 'asin', 'overall']]

    is_higher_than = amazon_reviews_df['overall'] >= min_score
    good_reviews_df = amazon_reviews_df[is_higher_than]

    amazon_metadata_df = Helpers.get_df('data/Datasets/%s' % tuple[1])[['asin', 'title', 'categories', 'related']]
    joined_meta_reviews = pd.merge(good_reviews_df, amazon_metadata_df, on='asin', how='outer')

    all_meta_reviews = all_meta_reviews.append(joined_meta_reviews)

# Remove Rows with any NaN and Save to CSV
all_meta_reviews.dropna().to_csv('data/Datasets/merged_amazon_meta_reviews.csv')

elapsed_time = time.time() - start_time
print('Preprocessing finished. Elapsed time: %d s.' % elapsed_time)
with open('data/Preprocessed/elapsed_time_log', 'w+') as f:
    f.write("ELAPSED TIME FOR:\n---------------\n")
    f.write("Preprocessing: %d s. (%d min)\n" % (elapsed_time, elapsed_time/60))
