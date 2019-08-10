from gensim.models import Word2Vec
import Helpers
import AmazonGetSingleProduct

asin_title_dict = None
model = None

if asin_title_dict is None or model is None:
    asin_title_dict = Helpers.load_json_dict('data/Preprocessed/asin_title_dict/asin_title_dict.json')
    model = Word2Vec.load('static/data/word2vec.model')

# asin_title_dict = Helpers.load_json_dict('data/Preprocessed/asin_title_dict/asin_title_dict.json')
# model = Word2Vec.load('static/data/word2vec.model')


def get_top_n(item_to_search, top_n=5):
    return list(
        asin_title_dict[key] for key in list(tuple[0] for tuple in model.wv.most_similar(item_to_search, topn=top_n)))


def get_top_n_full(item_to_search, top_n=5):
    return list(
        AmazonGetSingleProduct.get_by_asin(key) for key in list(tuple[0] for tuple in model.wv.most_similar(item_to_search, topn=top_n)))



