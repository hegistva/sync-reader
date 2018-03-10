import os
from translate.libs import align
from translate.libs import mapper_lib
from translate.libs import utils

def mapSentence(lang_source, lang_target, sent_source, sent_target):
    # get spacy models for language processing
    sp_source = utils.getSpacy(lang_source)
    sp_target = utils.getSpacy(lang_target)
    # parse documents
    doc_source = sp_source(sent_source)
    doc_target = sp_target(sent_target)
    # initalized alignment model    
    align.init(doc_source, lang_source, doc_target, lang_target)
    # map named entities
    mapper_lib.mapNamedEntities(confidence=0.5, sourceDoc=doc_source, targetDoc=doc_target)
    # map numbers
    mapper_lib.mapNumbers(confidence=0.5)
    # structural mapping with exact dictionary match
    scores = [0.05, 0.01, 0.005]
    for score in scores:
        mapper_lib.mapBaseStructure(minScore=score)
    # map in dependents
    for score in scores:
        mapper_lib.mapDependents(minScore=score)
    # TODO map base structure using translation + glove

    # map base strutcure if the word is not in the dictionary
    mapper_lib.mapBaseNoTranslate(minScore=0.3)

    # map dependents again
    for score in scores:
        mapper_lib.mapDependents(minScore=score)

    # map all translatables
    for score in [0.5, 0.1]:
        mapper_lib.mapTranslatables(minScore=score)

    # map using word vectors
    for score in [0.5, 0.4]:
        mapper_lib.mapGlove(minScore=score)

    # display source
    print('SOURCE')
    for m in align.MAPPING.source.tokens:
        print(m)
