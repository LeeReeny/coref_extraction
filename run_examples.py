import spacy
from spacy.language import Language
from spacy.tokens import Span
import networkx as nx

nlp = spacy.load("en_core_web_sm")
"""
@Language.component("expand_person_entities")
def expand_person_entities(doc):
    new_ents = []
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.start != 0:
            prev_token = doc[ent.start - 1]
            if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
                new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
                new_ents.append(new_ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

# Add the component after the named entity recognizer
nlp.add_pipe("expand_person_entities", after="ner")

doc = nlp("Dr. Alex Smith chaired first board meeting of Acme Corp Inc.")
print([(ent.text, ent.label_) for ent in doc.ents])"""

# doc = nlp('JingBo who dresses a green T-shirt was instructed by Chen.')
doc = nlp('11 operated as 11 (formerly 11) , was a low-cost airline based at the 22 in 33, 44 in the Philippines.')

for token in doc:
    print((token.head.text, token.text, token.dep_))

edges = []
for token in doc:
    for child in token.children:
        edges.append(('{0}'.format(token.lower_), '{0}'.format(child.lower_)))

graph = nx.Graph(edges)

"""entity1 = 'JingBo'.lower()
entity2 = 'Chen'.lower()"""

entity1 = '11'
entity2 = '22'

print(nx.shortest_path_length(graph, source=entity1, target=entity2))
print(nx.shortest_path(graph, source=entity1, target=entity2))