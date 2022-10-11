import spacy
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
from spacy.pipeline import DependencyParser
from spacy.tokens import Doc
from spacy.pipeline import EntityRuler
from spacy.language import Language
from spacy.tokens import Span
from spacy.symbols import ORTH

nlp = spacy.load("en_core_web_sm")

entities = ["Zest Airways, Inc.", "Asian Spirit and Zest Air", "AirAsia Zest", "Ninoy Aquino International Airport",
            "Pasay City", "Metro Manila", "Philippines"]

"""text = ("Zest Airways, Inc. operated as AirAsia Zest (formerly Asian Spirit and Zest Air) , was a low-cost airline "
        "based at the Ninoy Aquino International Airport in Pasay City, Metro Manila in the Philippines.")"""

text = ("11 operated as 11 (formerly 11) , was a low-cost airline "
        "based at the 22 in 33, 44 in the Philippines.")

doc = nlp(text)
for token in doc:
    print((token.head.text, token.text, token.dep_))

"""for chunk in doc.noun_chunks:
        print(chunk)
        # output: Zest Airways
        # Inc.
        # AirAsia Zest
        # formerly Asian Spirit
        # Zest Air
        # a low-cost airline
        # the Ninoy Aquino International Airport
        # Pasay City
        # Metro Manila
        # the Philippines
"""
# without parser
"""print("Noun phrase:",[chunk.text for chunk in doc.noun_chunks])
print("Verb:", [token.lemma_ for token in doc if token.pos_ == "VERBS"])
for entity in doc.ents:
    print(entity.text, entity.label_)"""

# a new way to generate the sentence
"""words = ["hello", "world", "!"]
spaces = [True, False, False]
doc1 = Doc(nlp.vocab, words=words, spaces=spaces)
doc2 = nlp(str(doc1))
for chunk in doc2.noun_chunks:
        print(chunk.text)
print(doc1)
print(type(doc1))"""

"""words = ["The", "band", "released", "two", "albums", "and", "numerous", "singles", ",", "with", "their", "debut", "single", "\"", "Ballerina", "\"", ",", "produced", "by", "former", "Europe", "guitarist", "Kee", "Marcello", "."]
spaces = [True, True,    True,       True,    True,   True,   True,       False,   True,  True,   True,    True,    True,    False, False,     False, True, True,     True,    True,     True,     True,     True,   False, True, ]
doc1 = Doc(nlp.vocab, words=words, spaces=spaces)
doc2 = nlp(str(doc1))
print(doc2)
print(type(doc2))"""

