import spacy
import networkx as nx

nlp = spacy.load('en_core_web_sm')
doc = nlp('Zest Airways , Inc. operated as AirAsia Zest ( formerly Asian Spirit and Zest Air ) , was a low - cost '
          'airline based at the Ninoy Aquino International Airport in Pasay City , Metro Manila in the Philippines .')
for token in doc:
    print((token.head.text, token.text, token.dep_))

edges = []
for token in doc:
    for child in token.children:
        edges.append(('{0}'.format(token.lower_), '{0}'.format(child.lower_)))
graph = nx.Graph(edges)

entity1 = 'Airways'.lower()    # Zest Airways , Inc.
entity2 = 'City'.lower()    #  Pasay City

print(nx.shortest_path_length(graph, source=entity1, target=entity2))  # 2
print(nx.shortest_path(graph, source=entity1, target=entity2))   # ['airways', ',', 'city']