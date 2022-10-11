import string
import json

sentence_file = 'sentence.json'
entity_file = 'entity.json'
entityID_file = 'entityID.json'
sentencewithID_file = "sentencewithID.json"

with open(sentence_file, mode='r', encoding='utf_8') as fr:
    docu = json.load(fr)

with open(entity_file, mode='r', encoding='utf_8') as fr:
    entity_info = json.load(fr)

with open(entityID_file, mode='r', encoding='utf_8') as fr:
    entity_ID = json.load(fr)

for i, doc in enumerate(entity_info):
    for j, ent in enumerate(doc):
        ent_ID = entity_ID[i][j]
        for mention in ent:
            sent_id = mention.get('sent_id')
            name = mention.get('name')
            sent = docu[i][sent_id]
            sent = sent.replace(name, ent_ID)
            docu[i][sent_id] = sent

with open(sentencewithID_file, 'w') as f:
    json.dump(docu, f)
print('finish replacing the mention names in sentences with entity ID')