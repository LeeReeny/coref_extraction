import os
import json
import pickle
import numpy as np

src_file = "/home/test2/lilei/spacy_practice/data/train_annotated.json"
save_file = "/home/test2/lilei/spacy_practice/result/mention_pronouns.json"
entitylist_file = "/home/test2/lilei/spacy_practice/result/entitylist.json"
pronouns = ['it', 'its', 'he', 'him', 'his', 'she', 'her', 'they', 'them', 'their', 'we', 'us', 'our']

print('Reading data from {}.'.format(src_file))
with open(file=src_file, mode='r', encoding='utf_8') as fr:
    ori_data = json.load(fr)
print("loading...")

entities = []
mens_pros = []
for i, doc in enumerate(ori_data):  # the i-th document
    sentences, entity_list, labels, title = doc['sents'], doc['vertexSet'], doc.get('labels', []), doc['title']

    L = 0
    Ls = [0]
    pro_pos = []
    men_pro = []
    for j, sent in enumerate(sentences):  # the j-th sentence
        L += len(sent)
        Ls.append(L)
        for k in range(len(sent)):
            if sent[k] in pronouns:
                pos = Ls[j] + k
                pro_pos.append([pos, sent[k]])
    pro_pos = sorted(pro_pos, key=lambda x: x[1])

    for ent in range(len(entity_list)):
        for men in range(len(entity_list[ent])):
            sent_id = int(entity_list[ent][men]['sent_id'])
            entity_list[ent][men]['sent_id'] = sent_id
            pos0, pos1 = entity_list[ent][men]['pos']
            entity_list[ent][men]['global_pos'] = (Ls[sent_id] + pos0, Ls[sent_id] + pos1)
            men_name = entity_list[ent][men]['name']
    entities.append(entity_list)

    if pro_pos:
        for pp in pro_pos:
            men_pro_info = []
            pos = pp[0]
            pro = pp[1]
            dist = 500
            ent_idx = 0
            men_idx = 0
            men_name = ""
            men_pos = [0, 0]
            for x in range(len(entity_list)):
                for y in range(len(entity_list[x])):
                    name = entity_list[x][y]['name']
                    global_pos0, global_pos1 = entity_list[x][y]['global_pos']
                    if global_pos1 < pos and pos - global_pos1 < dist:
                        dist = pos - global_pos1
                        ent_idx = x
                        men_idx = y
                        men_name = name
                        men_pos = [global_pos0, global_pos1]
            men_pro_info.append(i)
            men_pro_info.append(ent_idx)
            men_pro_info.append([men_idx, men_name, men_pos])
            men_pro_info.append(pp)
            men_pro.append(men_pro_info)

    if men_pro:
        mens_pros.append(men_pro)

with open(file=save_file, mode='w') as f:
    json.dump(mens_pros, f)
print("finish finding the pronouns")


