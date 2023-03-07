import os, spacy, pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# read spacy model
nlp = spacy.load('en_core_web_trf')

# read input data
with open('data/keywords.txt', encoding='utf8') as w:
    kw = w.read().splitlines()

db = pd.read_excel('data/nlp_db.xlsx')

# summarization function
def spacy_summarization(txt):
    doc = nlp(txt)
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():  
        freq_word[word] = (freq_word[word]/max_freq)
    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
    summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary


# data processing
def processing():
    people = []
    companies = []
    others = []
    named_keywords = []
    summarization = []

    for arc in list(db['Content']):
        PERSON = []
        ORG = []
        OTHER = []
        NKW = []
        summarization.append(spacy_summarization(arc))
        for en in nlp(arc).ents:
            if en.label_ == 'PERSON':
                PERSON.append(str(en).replace(',', '').replace('”', '').strip())
            elif en.label_ == 'ORG':
                ORG.append(str(en).replace(',', '').replace('”', '').strip())
            else:
                OTHER.append(str(en).replace(',', '').replace('”', '').strip())
        for k in kw:
            if len(k) < 3:
                if k in arc:
                    NKW.append(k)
            else:
                if k.lower() in arc.lower():
                    NKW.append(k)
        people.append(list(set(PERSON)))
        companies.append(list(set(ORG)))
        others.append(list(set(OTHER)))
        named_keywords.append(NKW)

    db['people'] = people
    db['companies'] = companies
    db['named keywords'] = named_keywords
    db['others'] = others
    db['summarization'] = summarization

    db.to_excel('data/nlp_db.xlsx', index=False)

if __name__ == '__main__':
    processing()
