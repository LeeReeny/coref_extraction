import json
import os
import math
import pickle
import random
from collections import defaultdict
import numpy as np
import networkx as nx
import spacy

nlp = spacy.load("en_core_web_sm")

src_file = "train_annotated.json"
save_file = "temp.json"
document_max_length = 512
"""if os.path.exists(save_file):
    with open(file=save_file, mode='rb') as fr:
        info = pickle.load(fr)
        data = info['data']

else:"""
with open(file=src_file, mode='r', encoding='utf_8') as fr:
    ori_data = json.load(fr)

    for i, doc in enumerate(ori_data):
        entity_list = doc['vertexSet']

        pos_id = np.zeros((document_max_length,), dtype=np.int32)
        ner_id = np.zeros((document_max_length,), dtype=np.int32)

        entity2mention = defaultdict(list)
        mention_idx = 1
        already_exist = set()
        for idx, vertex in enumerate(entity_list, 1):
            for v in vertex:
                name, sent_id, (pos0, pos1), ner_type = v['name'], v['sent_id'], v['pos'], v['type']
                if(pos0, pos1) in already_exist:
                    continue
                pos_id[pos0:pos1] = idx
                ner_id[pos0:pos1] = mention_idx
                entity2mention[idx].append(name)
                #entity2mention[idx].append(mention_idx)
                mention_idx += 1
                already_exist.add((pos0, pos1))
print(entity2mention)