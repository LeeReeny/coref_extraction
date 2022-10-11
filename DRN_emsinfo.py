import json
import os
import math
import pickle
import random
from collections import defaultdict
import numpy as np

ems_file = "ems_file.json"
document_max_length = 512
ner2id = json.load(open('data/ner2id.json', 'r'))
with open(file="data/train_annotated.json", mode='r', encoding='utf-8') as fr:
    ori_data = json.load(fr)
    print('loading...')

    for i, doc in enumerate(ori_data):
        title, entity_list, labels, sentences = doc['title'], doc['vertexSet'], doc.get('labels', []), doc['sents']

        ner_id = np.zeros((document_max_length,), dtype=np.int32)
        pos_id = np.zeros((document_max_length,), dtype=np.int32)
        sentence_id = np.zeros((document_max_length,), dtype=np.int32)
        ems_info = np.zeros((130, 7), dtype=np.int32)

        Ls = [0]
        L = 0
        for x in sentences:
            L += len(x)
            Ls.append(L)
        for j in range(len(entity_list)):
            for k in range(len(entity_list[j])):
                sent_id = int(entity_list[j][k]['sent_id'])
                entity_list[j][k]['sent_id'] = sent_id

                dl = Ls[sent_id]
                pos0, pos1 = entity_list[j][k]['pos']
                entity_list[j][k]['global_pos'] = (pos0 + dl, pos1 + dl)

        mention_idx = len(entity_list)
        already_exist = set()
        for idx, vertex in enumerate(entity_list):
            ems_info[idx] = np.array([1, ner_id[vertex[0]["type"]], -1, -1, idx, idx, -1])
            for v in vertex:
                sent_id, (pos0, pos1), ner_type = v['sent_id'], v['global_pos'], v['type']
                if (pos0, pos1) in already_exist:
                    continue
                if pos0 >= document_max_length:
                    continue
                ner_id[pos0, pos1] = ner2id["type"]
                pos_id[pos0, pos1] = idx + 1
                ems_info[mention_idx] = np.array([2, ner2id[ner_type], pos0, pos1, idx, mention_idx, sent_id])
                mention_idx += 1
                already_exist.add((pos0, pos1))

        for i in range(1, len(Ls)):
            sentence_id[Ls[i-1]:Ls[i]] = i
            ems_info[mention_idx] = np.array([3, -1, Ls[i-1], Ls[i]-1, -1, mention_idx, i-1])
            mention_idx += 1

    with open(ems_file, "w") as f:
        json.dump(ems_info, f)
    print('finish recording the ems info.')
