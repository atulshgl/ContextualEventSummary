# Imports the Google Cloud client library
# -*- coding: utf-8 -*-

from google.cloud import language
import argparse
import sys
import textwrap

def extractEntities(document) :
     entity_response = document.analyze_entities()    
     for entity in entity_response.entities:
        print('.' * 5)
        print('name: %s' % (entity.name,))
        print('type: %s' % (entity.entity_type,))
        print('metadata: %s' % (entity.metadata,))

def analyzeSyntax(document):
     analysis = document.annotate_text(include_entities=False,include_sentiment=False)
     return analysis.tokens

def dependents(tokens, head_index):
    """Returns an ordered list of the token indices of the dependents for
    the given head."""
    # Create head->dependency index.
    head_to_deps = {}
    for i, token in enumerate(tokens):
        head = token.edge_index
        if i != head:
            head_to_deps.setdefault(head, []).append(i)
    return head_to_deps.get(head_index, ())

def phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    begin, end = phrase_extent_for_head(tokens, head_index)
    return text[begin:end]


def phrase_extent_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    begin = tokens[head_index].text_begin
    end = begin + len(tokens[head_index].text_content)
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        begin = min(begin, child_begin)
        end = max(end, child_end)
    return (begin, end)

def find_triples(tokens,
                 left_dependency_label= ['NSUBJ', 'NSUBPASS'],
                 head_part_of_speech='VERB',
                 right_dependency_label=['DOBJ','POBJ']):
    """Generator function that searches the given tokens
    with the given part of speech tag, that have dependencies
    with the given labels.  For each such head found, yields a tuple
    (left_dependent, head, right_dependent), where each element of the
    tuple is an index into the tokens array.
    """
    for head, token in enumerate(tokens):
        if token.part_of_speech == head_part_of_speech:
            children = dependents(tokens, head)
            left_deps = []
            right_deps = []
            for child in children:
                child_token = tokens[child]
                child_dep_label = child_token.edge_label
                if child_dep_label in left_dependency_label:
                    left_deps.append(child)
                elif child_dep_label in right_dependency_label:
                    right_deps.append(child)
            for left_dep in left_deps:
                for right_dep in right_deps:
                    yield (left_dep, head, right_dep)


def show_triple(tokens, text, triple):
    """Prints the given triple (left, head, right).  For left and right,
    the entire phrase headed by each token is shown.  For head, only
    the head token itself is shown.
    """
    nsubj, verb, dobj = triple

    # Extract the text for each element of the triple.
    nsubj_text = phrase_text_for_head(tokens, text, nsubj)
    verb_text = tokens[verb].text_content
    dobj_text = phrase_text_for_head(tokens, text, dobj)

    # Pretty-print the triple
    print (nsubj_text)
    print (verb_text) 
    print (dobj_text)

def correctTextBeginPosition(tokens):
    """token begin position is returned incorrectly by the API. It count accent characters as extra character.
    """
    beginning = 0
    for token in tokens:
        token.text_begin = text.find(token.text_content, beginning) 
        beginning += len(token.text_content)
    return tokens

# Instantiates a client
language_client = language.Client()

# The text to analyze
text = u'En el segundo día de la prueba de pretemporada de Barcelona, Fernando Alonso sufrió un accidente en el turno 3. Fue trasladado por aire al Hospital General de Catalunya en Sant Cugat del Vallès, donde se sometió a escáneres que descubrieron que había sufrido una conmoción cerebral. Después de recuperar la conciencia, algunos periódicos informaron que Alonso sufrió una amnesia retrógrada en la que no tenía recuerdos más allá de 1995 y creía que seguía siendo un piloto de karting'
document = language_client.document_from_text(text, language='es', encoding=language.Encoding.UTF8)
extractEntities(document)

tokens = analyzeSyntax(document)
tokens = correctTextBeginPosition(tokens)

for triple in find_triples(tokens):
        show_triple(tokens, text, triple)

