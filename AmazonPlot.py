from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import Helpers

model = asin_title_dict = None;
if model is None and asin_title_dict is None:
    asin_title_dict = Helpers.load_json_dict('data/Preprocessed/asin_title_dict/asin_title_dict.json')
    model = Word2Vec.load('static/data/word2vec.model')


def plot(model, voc_dict):
    X = model.wv[model.wv.vocab]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # create a scatter plot of the projection
    plt.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        try:
            plt.annotate(voc_dict[word], xy=(result[i, 0], result[i, 1]))
        except:
            print('bad word')
    plt.show()


plot(model, asin_title_dict)
