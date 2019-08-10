import os
import json
import pandas as pd
import gzip
import ast
import glob
from collections import OrderedDict
import itertools

def parse(path, limit):
    g = gzip.open(path, 'rb')
    for index, line in enumerate(g):
        if limit != 0 and index == limit:
            break
        yield eval(line)


def get_df(path, limit=0):
    i = 0
    df = {}
    for d in parse(path, limit):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def save_list_to_file(list, path):
    with open(path, 'w') as f:
        for item in list:
            f.write("%s\n" % item)


def remove_all_from_folder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def load_json_dict(path):
    with open(path, 'r') as file:
        return json.load(file)


def load_all_txt_sentences(folder_path):
    sentences_list = list()
    for filename in glob.glob('%s/*.txt' % folder_path):
        with open(filename, 'r') as file:
            for line in file:
                line_to_list = ast.literal_eval(line)
                sentences_list.append(line_to_list)
    return sentences_list


def get_unique_values_from_col(df: pd.DataFrame, col_identifier: str):
    return df[col_identifier].unique()


def flatten_collection(collection):
    return list(OrderedDict((tuple(items), items) for items in
                            [items for items in itertools.chain(*collection)
                             if str(items) != 'nan']).values())


def list_to_dict(data):  # https://stackoverflow.com/questions/48936869/nested-list-to-nested-dict-python3
    if data:
        head, *tail = data  # This is a nicer way of doing head, tail = data[0], data[1:]
        return {head: list_to_dict(tail)}
    else:
        return {}


def merge_dicts(a, b, path=None):  # https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
