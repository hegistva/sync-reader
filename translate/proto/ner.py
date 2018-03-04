
import spacy
import os
import Levenshtein
import numpy as np
from translate.libs import dico


eng = spacy.load('en_core_web_md') # 'en_core_web_md'
fra = spacy.load('fr_core_news_md') # 'fr_core_news_md'

text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny accepting the existence of such monsters, then the Norwegian stories of Bishop Pontoppidan, the narratives of Paul Egede, and finally the reports of Captain Harrington-- whose good faith is above suspicion--in which he claims he saw, while aboard the Castilian in 1857, one of those enormous serpents that, until then, had frequented only the seas of France's old extremist newspaper, The Constitutionalist."""
# text_eng = """They even reprinted reports from ancient times:  the views of Aristotle and Pliny"""
text_eng = """A Runaway Reef    THE YEAR 1866 was marked by a bizarre development, an unexplained and downright inexplicable phenomenon that surely no one has forgotten. Without getting into those rumors that upset civilians in the seaports and deranged the public mind even far inland, it must be said that professional seamen were especially alarmed."""

text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline, qui admettaient l'existence de ces monstres, puis les récits norvégiens de l'évêque Pontoppidan, les relations de Paul Heggede, et enfin les rapports de M. Harrington, dont la bonne foi ne peut être soupçonnée, quand il affirme avoir vu, étant à bord du _Castillan_, en 1857, cet énorme serpent qui n'avait jamais fréquenté jusqu'alors que les mers de l'ancien _Constitutionnel_."""
# text_fra = """On reproduisit même les procès-verbaux des temps anciens les opinions d'Aristote et de Pline"""
text_fra = """UN ÉCUEIL FUYANT  L'année 1866 fut marquée par un événement bizarre, un phénomène inexpliqué et inexplicable que personne n'a sans doute oublié. Sans parler des rumeurs qui agitaient les populations des ports et surexcitaient l'esprit public à l'intérieur des continents les gens de mer furent particulièrement émus."""

doc_eng = eng(text_eng)
doc_fra = fra(text_fra)

initAlignment()

# named entity mappings
eng_names = [sp_eng.text.lower() for sp_eng in doc_eng.ents]


# for sp_fra in doc_fra.ents:    
#     text_fra = sp_fra.text.lower()
#     print(text_fra)
#     print(eng_names)
#     dists = [Levenshtein.distance(text_fra, eng_name) for eng_name in eng_names]
#     idx_min = np.argmin(dists)
#     eng_ent = doc_eng.ents[idx_min]
#     prob = 1 - dists[idx_min] / len(text_fra)
#     if  prob >= 0.3:
#         del eng_names[idx_min]
#         for idx_fr in range(sp_fra.start, sp_fra.end):
#             for idx_en in range(eng_ent.start, eng_ent.end):
#                 Alignment.s2t[idx_fr].mapTo(MapTarget(doc_eng[idx_en], prob))

# number mapping
for mf in Alignment.s2t:
    if mf.token.is_digit:
        for token_eng in doc_eng:
            if token_eng.is_digit:
                d = Levenshtein.distance(mf.token.text, token_eng.text)                
                prob = 1 - d / len(mf.token.text)
                if prob >= 0.5:
                    mf.mapTo(MapTarget(token_eng, prob))

# translation based mapping

dico.setDefault('fra', 'eng')

for mf in Alignment.s2t:
    if not mf.isMapped and mf.token.is_alpha:
        tr = dico.translateLemma(mf.token.text.lower())
        if not tr:
            tr = dico.translateLemma(mf.token.lemma_.lower())
        # there translations in the dictionary
        tokens_found = []
        target_matches = [] # possible english target tokens
        for mt in Alignment.t2s: 
            if not mt.isMapped and mt.token.is_alpha:
                lemma_eng = mt.token.lemma_.lower()
                target_matches.append(mt)
                if lemma_eng in tr:
                    tokens_found.append(mt)            
        if tokens_found:
            if len(tokens_found) <= 3:
                # if there are fewer than three exact matches, map the closest
                closest = min(tokens_found, key = lambda x: abs(mf.ratio - x.ratio))
                mf.mapTo(MapTarget(closest.token,  1.0-abs(mf.ratio-closest.ratio)))
        else: # no translation, try to map by distance
            min_dist = 1000
            min_token = None
            source_lemma = mf.token.lemma_.lower()
            for tm in target_matches:
                target_lemma = tm.token.lemma_.lower()                
                dist = Levenshtein.distance(source_lemma, target_lemma)
                if dist < min_dist:
                    min_dist = dist
                    min_token = tm.token
            rel_dist = min_dist / len(source_lemma)
            if  rel_dist < 0.5:
                mf.mapTo(MapTarget(min_token,  1.0-rel_dist))

for mf in Alignment.s2t:
    if not mf.isMapped and mf.token.is_alpha:
        tr = dico.translateLemma(mf.token.text.lower())
        if not tr:
            tr = dico.translateLemma(mf.token.lemma_.lower())
        if tr:
            # there translations in the dictionary
            target_matches = [] # possible english target tokens
            for mt in Alignment.t2s:
                if not mt.isMapped and mt.token.is_alpha:
                    target_matches.append(mt)
            # no exact matches, try using word2wec
            # print("Trying to find word2vec for word %s [%s] translations %s" % (mf.token.text, mf.token.pos_, tr))
            tr_tokens = eng(" ".join(tr), disable=['tagger', 'parser', 'ner'])
            max_sim = -1000.0
            best_match = None
            for tm in target_matches:
                max_sim_tr = -1000.0
                best_match_tr = None
                for trt in tr_tokens:
                    try:
                        sim = tm.token.similarity(trt)
                        if tm.token.pos_ == mf.token.pos_:
                            sim *= 1.5 # reward similar part of speach
                        sim *= (1 - abs(mf.ratio - tm.ratio)) # revard those that are "close" TODO POS
                        if sim > max_sim_tr:
                            max_sim_tr = sim
                            best_match_tr = trt
                    except Exception:
                        # print('ERROR: No similarity between "%s" and "%s"' % (tm.token.text, trt.text))
                        pass # similarity is not available
                # print('For english token %s [%s] the best translation is %s with similarity: %.2f' % (tm.token.text, tm.token.pos_, best_match_tr.text, max_sim_tr))
                if max_sim_tr > max_sim:
                    max_sim = max_sim_tr
                    best_match = tm.token                
            # print('For french token %s [%s] the best english token is %s [%s] with similarity: %.2f' % (mf.token.text, mf.token.pos_, best_match.text, best_match.pos_, max_sim))
            if max_sim > 0.3:
                mf.mapTo(MapTarget(best_match,  max_sim))

# Structural
for m in Alignment.s2t:
    if not m.isMapped:
        mapped = False
        for child in m.token.children:
            child_map = Alignment.s2t[child.i]
            if child_map.isMapped: # child is mapped, map to the parent
                m.mapTo(MapTarget(child_map.mapped.target.head, child_map.mapped.confidence))                
                mapped = True            
                break
        if not mapped:
            h = m.token.head
            if not h == m.token:
                parent_map = Alignment.s2t[h.i]
                if parent_map.isMapped: # parent is mapped for now map to parent
                    m.mapTo(MapTarget(parent_map.mapped.target, parent_map.mapped.confidence))

# display alignment
for m in Alignment.s2t:
    print(m)

# visualize the POS tagging resutls

html_fra = spacy.displacy.render(doc_fra, style='dep', options={'compact': True}, page=True)
html_eng = spacy.displacy.render(doc_eng, style='dep', options={'compact': True}, page=True)

VISUAL = 'cache/visual'

os.makedirs(VISUAL, exist_ok=True)

with open(os.path.join(VISUAL, 'fra.html'), 'w') as f:
    f.write(html_fra)

with open(os.path.join(VISUAL, 'eng.html'), 'w') as f:
    f.write(html_eng)


