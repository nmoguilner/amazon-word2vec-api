import Helpers
import pandas as pd


# full_metadata_df = Helpers.get_df('data/Datasets/meta_Movies_and_TV.json.gz')

metadata_files = [
    'meta_Electronics.json.gz',
    'meta_Musical_Instruments.json.gz',
    'meta_Movies_and_TV.json.gz'
]


full_metadata_df = pd.DataFrame()
if full_metadata_df.empty:
    for metadata_f in metadata_files:
        full_metadata_df = full_metadata_df.append(Helpers.get_df('data/Datasets/%s' % metadata_f))

# for metadata_f in metadata_files:
#     full_metadata_df = full_metadata_df.append(Helpers.get_df('data/Datasets/%s' % metadata_f))

def get_by_asin(asin: str):
    product = full_metadata_df.loc[full_metadata_df['asin'] == asin][
        ['asin', 'title', 'categories', 'brand', 'price', 'imUrl', 'description']]
    return product.to_json(orient='records')
