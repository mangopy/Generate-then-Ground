import math
import sys
sys.path.append('../../')
import pickle
import multiprocessing
import json
import torch
import random
import os
import numpy as np
from tqdm import tqdm
from scipy import stats
from nltk import word_tokenize
import torch.multiprocessing as mp
import re
import string
import warnings
import functools

def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"Function '{func.__name__}' is deprecated and will be removed in a future version.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper

def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def filter(text: str, left: int = 256, right: int = 512, rate: float = 0.8):
    if text.isascii() == False:
        return False
    a = word_tokenize(text)
    if len(a) < left or len(a) > right:
        return False
    r = len([word for word in a if word.isalnum()]) / (len(a) + 1)
    if r < rate:
        return False
    return True


def mode(nums):
    """

    :param nums: list(int/float)
    :return:
    """
    return stats.mode(nums)[0][0].item()


def seed_torch(seed=1048):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)  # disable the hash random
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if you are using multi-GPU.
    # torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def read_jsonl(ids, filename):
    with open(filename, 'r') as f:
        data = [json.loads(line) for line in tqdm(f)]
    return ids, data


def pickle_load(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def multi_load_jsonlfolder(folder, num_processes=10):
    """

    :param folder: folder
    :param num_processes:
    :return:
    """
    filelist = os.listdir(folder)
    num_processes = max(len(filelist), num_processes)
    pool = multiprocessing.Pool(processes=num_processes)
    collects = []
    for ids, filename in enumerate(filelist):
        collects.append(pool.apply_async(read_jsonl, (ids, os.path.join(folder, filename))))

    pool.close()
    pool.join()
    results = []
    for i, result in enumerate(collects):
        ids, res = result.get()
        assert ids == i
        results.extend(res)
    return results


def unique_json(data_path, feature):
    tmp = load_data(data_path)
    for line in tmp:
        assert feature in line
    s = set()
    data = []
    for line in tmp:
        if line[feature] not in s:
            data.append(line)
    return data


def load_jsonl(ids, data):
    data = [json.loads(line) for line in tqdm(data)]
    return ids, data


def multi_clean(data, num_processes=10, func=None):
    """

    :param num_processes:
    :return:
    """
    length = len(data) // num_processes + 1
    pool = multiprocessing.Pool(processes=num_processes)
    collects = []
    for ids in range(num_processes):
        collect = data[ids * length:(ids + 1) * length]
        collects.append(pool.apply_async(func, (collect, ids)))

    pool.close()
    pool.join()
    results = []
    for i, result in enumerate(collects):
        ids, res = result.get()
        assert ids == i
        results.extend(res)
    return results


def multi_load_jsonl(filename, num_processes=10):
    """

    :param filename: the jsonl file with big size
    :param num_processes:
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = [line.strip() for line in f]
        if len(data) <= 20000:
            _, data = load_jsonl(0, data)
            return data

    length = len(data) // num_processes + 1
    pool = multiprocessing.Pool(processes=num_processes)
    collects = []
    for ids in range(num_processes):
        collect = data[ids * length:(ids + 1) * length]
        collects.append(pool.apply_async(load_jsonl, (ids, collect)))

    pool.close()
    pool.join()
    results = []
    for i, result in enumerate(collects):
        ids, res = result.get()
        assert ids == i
        results.extend(res)
    return results


def write_file(data, filename, num_processes=20, default_name='train', indent=4):
    if filename.endswith('.json'):
        json.dump(data, open(filename, 'w'), indent=indent)
    elif filename.endswith('.jsonl'):
        with open(filename, 'w') as f:
            for line in data:
                f.write(json.dumps(line) + '\n')
    elif filename.endswith('.txt'):
        with open(filename, 'w') as f:
            for line in data:
                f.write(str(line) + '\n')
    elif filename.endswith('.pkl'):
        pickle.dump(data, open(filename, 'wb'))
    elif '.' not in filename:
        multi_write_jsonl(data, filename, num_processes=num_processes, default_name=default_name)
    else:
        raise "no suitable function to write data"


def write_jsonl(data, filename, ids=None):
    with open(filename, 'w') as f:
        for line in tqdm(data):
            f.write(json.dumps(line) + '\n')
    return ids, len(data)


def multi_write_jsonl(data, folder, num_processes=10, default_name='train'):
    """

    :param filename:
    :param num_processes:
    :return:
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    length = len(data) // num_processes + 1
    pool = multiprocessing.Pool(processes=num_processes)
    collects = []
    for ids in range(num_processes):
        filename = os.path.join(folder, f"{default_name}{ids}.jsonl")
        collect = data[ids * length:(ids + 1) * length]
        collects.append(pool.apply_async(write_jsonl, (collect, filename, ids)))

    pool.close()
    pool.join()
    cnt = 0
    for i, result in enumerate(collects):
        ids, num = result.get()
        assert ids == i
        cnt += num
    print(f"** total {cnt}  examples have been writen to {folder} **")
    return cnt


def load_data(filename, num_processes=10, folder=False, custom_load='json'):
    if filename.endswith('.jsonl'):
        return multi_load_jsonl(filename, num_processes)
    elif filename.endswith('.json'):
        return json.load(open(filename, 'r'))
    elif filename.endswith('.pkl'):
        return pickle.load(filename)
    elif filename.endswith('.txt'):
        with open(filename, 'r') as f:
            data = [line.strip() for line in f]
            return data
    elif folder == True and custom_load != None:
        data = []
        for line in os.listdir(filename):
            if line.endswith(custom_load):
                data.extend(load_data(line))
        return data
    else:
        try:
            data = multi_load_jsonlfolder(filename)
            return data
        except BaseException:
            raise "no suitable function to load data"


def multi_process_cuda(data_path, ranks, func, **kwargs):
    """

    :param data_path: data path
    :param ranks: gpu device id
    :param func: the function for batch
    :param kwargs: the 'dict', indicating the parameter to pass into the 'func'
    :return:
    """
    torch.multiprocessing.set_start_method('spawn', force=True)
    cuda_pool = mp.Pool(processes=len(ranks))
    data = load_data(data_path)
    length = math.ceil(len(data) // len(ranks))
    collects = []
    for ids, rank in enumerate(ranks):
        collect = data[ids * length:(ids + 1) * length]
        collects.append(cuda_pool.apply_async(func, (rank, collect, kwargs)))
    cuda_pool.close()
    cuda_pool.join()
    results = []
    for rank, result in zip(ranks, collects):
        r, res = result.get()
        assert r == rank
        results.extend(res)
    return results


def multi_process_cuda_data(data, ranks, func, **kwargs):
    """

    :param data_path: the data path
    :param ranks: gpu device ids
    :param func:
    :param kwargs:
    :return:
    """
    torch.multiprocessing.set_start_method('spawn', force=True)
    cuda_pool = mp.Pool(processes=len(ranks))
    length = math.ceil(len(data) // len(ranks))
    collects = []
    for ids, rank in enumerate(ranks):
        collect = data[ids * length:(ids + 1) * length]
        collects.append(cuda_pool.apply_async(func, (rank, collect, kwargs)))
    cuda_pool.close()
    cuda_pool.join()
    results = []
    for rank, result in zip(ranks, collects):
        r, res = result.get()
        assert r == rank
        results.extend(res)
    return results
