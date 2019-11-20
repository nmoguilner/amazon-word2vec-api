import matplotlib.pyplot as plt
import Helpers

items_by_reviewer_id = Helpers.load_all_txt_sentences('data/Preprocessed/by_reviewer_id')
count_dict = dict()

for sentence in items_by_reviewer_id:
    for product_asin in sentence:
        if product_asin not in count_dict:
            count_dict[product_asin] = 1
        else:
            count_dict[product_asin] += 1

x, y = zip(*count_dict.items())

plt.bar(list(count_dict.keys())[:50], list(count_dict.values())[:50], color='g')
plt.savefig('reviewers.png')



items_by_categories = Helpers.load_all_txt_sentences('data/Preprocessed/by_categories')
count_dict_categories = dict()

for sentence in items_by_categories:
    for product_asin in sentence:
        if product_asin not in count_dict_categories:
            count_dict_categories[product_asin] = 1
        else:
            count_dict_categories[product_asin] += 1

x, y = zip(*count_dict_categories.items())

plt.bar(list(count_dict_categories.keys())[:50], list(count_dict_categories.values())[:50], color='g')
plt.savefig('categories.png')