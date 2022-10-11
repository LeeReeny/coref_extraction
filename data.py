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

save_path = "/result"
src_file = "data/train_annotated.json"
save_file = save_path + "sentence.json"
eIns_file = save_path + "ents_in_sent.json"
raw_file = save_path + "raw_sentens.json"
entity_file = save_path + "entity.json"
entityID_file = save_path + "entityID.json"
sentencewithID_file = save_path + "sentencewithID.json"
paths = []
docu = []  # all the sentences without ""
docu_ents = []  # the entities in every sentences
raw_docu = []  # sentences with original ""
entity_info = []  # extract all the entity info from original data
entity_ID = []  # generated entity ID

# for generating entity_ID
width_of_doc = 5
width_of_ent = 2
width_of_type = 6

print('Reading data from {}.'.format(src_file))
if os.path.exists(save_file):
    with open(file=save_file, mode='rb') as fr:
        info = pickle.load(fr)
        data = info['data']
    print('load preprocessed data from {}.'.format(save_file))

else:
    with open(file=src_file, mode='r', encoding='utf_8') as fr:
        ori_data = json.load(fr)
    print("loading...")

    for i, doc in enumerate(ori_data):
        sents, entity_list, labels, title = doc['sents'], doc['vertexSet'], doc.get('labels', []), doc['title']

        # extract all the entity info from original data
        entity_info.append(entity_list)

        # deal the sentences
        L = 0
        Ls = []
        sentences = []
        raw_sentences = []
        for sentence in sents:
            L += len(sentence)
            Ls.append(L)     # for location
            raw_sentences.append(sentence)
            str = ''
            for word in sentence:
                str += word
                str += " "
            sentences.append(str.strip())  # eliminate the " "
        docu.append(sentences)
        raw_docu.append(raw_sentences)

        # record the entities in every sentences
        entsInsent = [[] for _ in range(len(sents))]
        for j in range(len(entity_list)):
            for k in range(len(entity_list[j])):
                sent_id = int(entity_list[j][k]['sent_id'])
                entity_list[j][k]['sent_id'] = sent_id
                ents_name = entity_list[j][k]['name'].strip('"')
                entsInsent[sent_id].append(entity_list[j][k]['name'])
        docu_ents.append(entsInsent)

    # generate the entity ID
    for i, doc in enumerate(entity_info):
        ents_ID = []
        idx_of_doc = str(i).rjust(width_of_doc, '0')  # ID的第一部分是该entity所在的doc的序号，扩充成5位，右侧对齐左侧补零
        for j, ent in enumerate(doc):
            idx_of_ent = str(j).rjust(width_of_ent, '0')  # ID的第二部分是该entity在doc中的序号，扩充成2位，右侧对齐左侧补零
            Type = ent[0].get('type')
            Type = Type.rjust(width_of_type, 'X')  # ID的第三部分是该entity的类型，扩充成6位，右侧对齐左侧补'X'
            the_ID = idx_of_doc + idx_of_ent + Type
            ents_ID.append(the_ID)
        entity_ID.append(ents_ID)

    # wirte the sentences
    with open(save_file, "w") as f:
        json.dump(docu, f)
    print('finish reading {} and save preprocessed data to {}.'.format(src_file, save_file))

    # replace the mention name with generated entity ID
    for i, doc in enumerate(entity_info):
        for j, ent in enumerate(doc):
            ent_ID = entity_ID[i][j]
            for mention in ent:
                sent_id = mention.get('sent_id')
                name = mention.get('name')
                sent = docu[i][sent_id]
                sent = sent.replace(name, ent_ID)
                docu[i][sent_id] = sent


    # write the raw sentences
    with open(raw_file, "w") as f:
        json.dump(raw_docu, f)
    print('finish recording raw sentences')

    # write the entities in every sentence
    with open(eIns_file, "w") as f:
        json.dump(docu_ents, f)
    print('finish entities classification by sentence.')

    # write the entity info
    with open(entity_file, "w") as f:
        json.dump(entity_info, f)
    print('finish recording the entity info.')

    # write the entity ID
    with open(entityID_file, "w") as f:
        json.dump(entity_ID, f)
    print('finish generating the entity ID.')

    # write the sentence with entity ID
    with open(sentencewithID_file, 'w') as f:
        json.dump(docu, f)
    print('finish replacing the mention names in sentences with entity ID')



"""for sent in sentences:
    doc = nlp(sent)
    edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token.lower_), '{0}'.format(child.lower_)))
    graph = nx.Graph(edges)"""



