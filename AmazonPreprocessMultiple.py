import pandas as pd
import Helpers

all_meta_reviews = pd.DataFrame()

files = [
    ('reviews_Electronics_5.json.gz', 'meta_Electronics.json.gz'),
    ('reviews_Musical_Instruments_5.json.gz', 'meta_Musical_Instruments.json.gz'),
    ('reviews_Movies_and_TV_5.json.gz', 'meta_Movies_and_TV.json.gz')
]

for tuple in files:
    print('Preprocessing: %s - %s...' % (tuple[0], tuple[1]))
    amazon_reviews_df = Helpers.get_df('data/Datasets/%s' % tuple[0])[['reviewerID', 'asin', 'overall']]

    is_higher_3 = amazon_reviews_df['overall'] >= 3
    good_reviews_df = amazon_reviews_df[is_higher_3]

    amazon_metadata_df = Helpers.get_df('data/Datasets/%s' % tuple[1])[['asin', 'title', 'categories', 'related']]
    joined_meta_reviews = pd.merge(good_reviews_df, amazon_metadata_df, on='asin', how='outer')

    all_meta_reviews = all_meta_reviews.append(joined_meta_reviews)

# Remove Rows with any NaN and Save to CSV
all_meta_reviews.dropna().to_csv('data/Datasets/merged_amazon_meta_reviews.csv')
