import pandas as pd
from pandas.io.json import json_normalize
import ast
import json

import Helpers

# pandas display config
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 10000)

chunksize = 100000
asin_title_dict = dict()

start = 0
end = chunksize


# remove keys which are not in dict and collections with length < 2. lists are mutable, pass by ref
def clean_flattened_collection(flattened_collection):
    i = 0
    flattened_items_len = len(flattened_collection)
    while i < flattened_items_len:
        items = flattened_collection[i]
        j = 0
        items_len = len(items)
        while j < items_len:
            if items[j] not in asin_title_dict:
                items.remove(items[j])
                j -= 1
                items_len -= 1
            j += 1

        if len(items) < 2:
            flattened_collection.remove(items)
            i -= 1
            flattened_items_len -= 1

        i += 1


def process(chunk, start, end):
    print('start processing batch from %d to %d' % (start, end))
    size = len(chunk)

    meta_reviews = chunk.loc[:, ~chunk.columns.str.contains('^Unnamed')].dropna()  # remove unnamed columns

    # Quick Dict for lookup
    asin_title = meta_reviews[['asin', 'title']]
    asin_title_dict.update(asin_title.set_index('asin')['title'].to_dict())

    items_by_reviewer_id = [items for items in meta_reviews.groupby('reviewerID')['asin'].apply(list).tolist()]

    clean_flattened_collection(items_by_reviewer_id)
    Helpers.save_list_to_file(items_by_reviewer_id,
                              'data/Preprocessed/by_reviewer_id/items_by_reviewer_id_%d_%d.txt' % (
                                  start, end))

    items_by_categories = [items for items in meta_reviews.groupby('categories')['asin'].apply(list).tolist()]

    clean_flattened_collection(items_by_categories)
    Helpers.save_list_to_file(items_by_categories,
                              'data/Preprocessed/by_categories/items_by_categories_%d_%d.txt' % (start, end))

    if len(meta_reviews.query('related.notnull()', engine='python')):

        related_cols = json_normalize(meta_reviews['related'].apply(ast.literal_eval))
        meta_reviews_related = meta_reviews.reset_index().join(related_cols)
        del related_cols

        if 'related' in meta_reviews_related:
            del meta_reviews_related['related']  # not interesting

        if 'related_x' in meta_reviews_related:
            del meta_reviews_related['related_x']  # not interesting

        if 'related_y' in meta_reviews_related:
            del meta_reviews_related['related_y']  # not interesting

        if 'also_viewed' in meta_reviews_related:
            del meta_reviews_related['also_viewed']  # not interesting

        meta_reviews_related = meta_reviews_related.dropna(axis=0, subset=['asin'])

        # add asin item to the related lists
        for index, row in meta_reviews_related.iterrows():
            if 'also_bought' in row and isinstance(row['also_bought'], (list,)):
                row['also_bought'].insert(0, str(row['asin']))
            if 'bought_together' in row and isinstance(row['bought_together'], (list,)):
                row['bought_together'].insert(0, str(row['asin']))
            if 'buy_after_viewing' in row and isinstance(row['buy_after_viewing'], (list,)):
                row['buy_after_viewing'].insert(0, str(row['asin']))

        if 'also_bought' in meta_reviews_related:
            items_by_bought_too = meta_reviews_related.groupby('asin')[
                'also_bought'].apply(list).tolist()
            flattened_items_by_bought_too = Helpers.flatten_collection(items_by_bought_too)
            clean_flattened_collection(flattened_items_by_bought_too)
            Helpers.save_list_to_file(flattened_items_by_bought_too,
                                      'data/Preprocessed/also_bought/flattened_items_by_bought_too_%d_%d.txt' % (
                                          start, end))
            del items_by_bought_too
            del flattened_items_by_bought_too

        if 'bought_together' in meta_reviews_related:
            items_by_bought_together = meta_reviews_related.groupby('asin')['bought_together'].apply(list).tolist()
            flattened_items_by_bought_together = Helpers.flatten_collection(items_by_bought_together)
            clean_flattened_collection(flattened_items_by_bought_together)
            Helpers.save_list_to_file(flattened_items_by_bought_together,
                                      'data/Preprocessed/bought_together/flattened_items_by_bought_together_%d_%d.txt' % (
                                          start, end))
            del items_by_bought_together
            del flattened_items_by_bought_together

        if 'buy_after_viewing' in meta_reviews_related:
            items_by_bought_after_viewing = meta_reviews_related.groupby('asin')[
                'buy_after_viewing'].apply(list).tolist()
            flattened_items_by_bought_after_viewing = Helpers.flatten_collection(items_by_bought_after_viewing)
            clean_flattened_collection(flattened_items_by_bought_after_viewing)
            Helpers.save_list_to_file(flattened_items_by_bought_after_viewing,
                                      'data/Preprocessed/buy_after_viewing/flattened_items_by_bought_after_viewing_%d_%d.txt' % (
                                          start, end))
            del items_by_bought_after_viewing
            del flattened_items_by_bought_after_viewing

        del meta_reviews_related
    else:
        print('no related')

    start += size
    end += size

    del chunk
    del meta_reviews

    print('processing batch from %d to %d finished!' % (start, end))
    return start, end


Helpers.remove_all_from_folder('data/Preprocessed/asin_title_dict/')
Helpers.remove_all_from_folder('data/Preprocessed/also_bought/')
Helpers.remove_all_from_folder('data/Preprocessed/bought_together/')
Helpers.remove_all_from_folder('data/Preprocessed/buy_after_viewing/')
Helpers.remove_all_from_folder('data/Preprocessed/by_categories/')
Helpers.remove_all_from_folder('data/Preprocessed/by_reviewer_id/')

for chunk in pd.read_csv('data/Datasets/merged_amazon_meta_reviews.csv', chunksize=chunksize,
                         dtype={"reviewerID": str, "asin": str, "overall": float, "title": str, "categories": str,
                                "related": str}):
    start, end = process(chunk, start, end)

with open('data/Preprocessed/asin_title_dict/asin_title_dict.json', 'w') as fp:
    json.dump(asin_title_dict, fp)
