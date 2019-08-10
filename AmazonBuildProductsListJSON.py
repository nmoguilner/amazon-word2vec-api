import Helpers
import json
import numpy as np
import pandas as pd
from functools import reduce


asin_title_dict = Helpers.load_json_dict('data/Preprocessed/asin_title_dict/asin_title_dict.json')

metadata_files = [
    'meta_Electronics.json.gz',
    'meta_Musical_Instruments.json.gz',
    'meta_Movies_and_TV.json.gz'
]

full_metadata_df = pd.DataFrame()

for metadata_f in metadata_files:
    full_metadata_df = full_metadata_df.append(Helpers.get_df('data/Datasets/%s' % metadata_f))

# full_metadata_df = Helpers.get_df('data/Datasets/meta_Movies_and_TV.json.gz')

meta_electronics_df = full_metadata_df[full_metadata_df['asin'].isin(asin_title_dict)][
    ['asin', 'title', 'categories', 'brand', 'price', 'imUrl', 'description']]

meta_electronics_df = meta_electronics_df.replace(np.nan, '', regex=True)

with open('static/data/products_list.json', 'w') as fp:
    json.dump(meta_electronics_df.to_dict('records'), fp)

categories_list = meta_electronics_df['categories'].apply(list).tolist()
flattened_categories = Helpers.flatten_collection(categories_list)

categories_dict_list = []
for line in flattened_categories:
    categories_dict_list.append(Helpers.list_to_dict(line))

categories_dict = reduce(Helpers.merge_dicts, categories_dict_list)

with open('static/data/categories.json', 'w') as fp:
    json.dump(categories_dict, fp)
