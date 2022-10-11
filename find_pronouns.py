import json
import math
import os
import pickle
import numpy as np

pronouns = ['it', 'its', 'he', 'him', 'his', 'she', 'her', 'they', 'them', 'their', 'we', 'us', 'our']
src_file = "/result/raw_sentens.json"


with open(file=src_file, mode='r', encoding='utf-8') as fr:
    ori_sents = json.load(fr)
    print("loading...")

for i, docu in enumerate(ori_sents):
    L = 0
    Ls = [0]
    for j, sent in enumerate(docu):
        L += len(sent)
        Ls.append(L)
        for k in range(len(sent)):
            print(sent[k])
            break