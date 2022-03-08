import spacy
from spacy.matcher import Matcher

def reindex(ent,start,end):
    if ent[0]>start:
        steps=end-start
        return ([ent[0]+steps,ent[1]+steps,ent[2]])
    else: return ent

class Model(object):
    def __init__(self,path,patterns):
        self.nlp=spacy.load("fr_core_news_lg")
        self.matcher = Matcher(self.nlp.vocab)
        self.ner_model=spacy.load(path)
        self.matcher.add("cleaning", patterns,greedy="LONGEST")
    def update(self, new_path, new_patterns):
        self.matcher = Matcher(self.nlp.vocab)
        self.ner_model=spacy.load(new_path)
        self.matcher.add("cleaning", new_patterns,greedy="LONGEST")
    def predict_ner(self,text):
        doc=self.nlp(text)
        matches = self.matcher(doc,as_spans=True)
        indexs=[]
        for span in matches:
            indexs.append((span.start_char,span.end_char,span.text))
        indexs=sorted(indexs, key=lambda idx: idx[0],reverse=True)
        for idx in indexs:
            text=text[:idx[0]]+text[idx[1]:]
        ents=[]
        doc=self.ner_model(text)
        for ent in doc.ents:
            if ent.label_ in ['PER','LOC','ORG']:
                ents.append((ent.start_char,ent.end_char,ent.label_))
        indexs=sorted(indexs, key=lambda idx: idx[0],reverse=False)
        for idx in indexs:
            text=text[:idx[0]]+idx[2]+text[idx[0]:]
            ents=[reindex(ent,idx[0],idx[1]) for ent in ents]
        return ents
    def pseudonymise(self,doc):
        return doc.text
