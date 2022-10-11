import string
import os
import pickle
import json


src_file = "entity.json"
save_file = "entityID.json"
entity_ID = []

with open(src_file, mode='r', encoding='utf_8') as fr:
    entity_list = json.load(fr)  # list

width_of_doc = 5
width_of_ent = 2
width_of_type = 6
for i, doc in enumerate(entity_list):
    ents_ID = []
    idx_of_doc = str(i).rjust(width_of_doc, '0')  # ID的第一部分是该entity所在的doc的序号，扩充成5位，右侧对齐左侧补零
    for j, ent in enumerate(doc):
        idx_of_ent = str(j).rjust(width_of_ent, '0')  # ID的第二部分是该entity在doc中的序号，扩充成2位，右侧对齐左侧补零
        Type = ent[0].get('type')
        Type = Type.rjust(width_of_type, 'X')  # ID的第三部分是该entity的类型，扩充成6位，右侧对齐左侧补'X'
        the_ID = idx_of_doc + idx_of_ent + Type
        ents_ID.append(the_ID)
    entity_ID.append(ents_ID)

with open(save_file, "w") as f:
    json.dump(entity_ID, f)
print('finish generating the entity ID.')