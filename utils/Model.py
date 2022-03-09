"""
This file contains the implementation of the class Model.
This class is responsible for cleaning text, detecting NER, and text pseudonymization.
"""

import spacy
from spacy.matcher import Matcher

def reindex(ent,start,end):
    """A helper function used by predict_ner function; it updates entity attributes, if needed, when inserting a new word in the text starting at index start.
    Args:
        ent (tuple,list): a tuple describing an entity (start_index,end_index,ent_label)
        start (int): the index where to insert the new word.
        end (int): the index of the last character in the new word after inserting.
    Returns:
        tuple: a tuple defining the new updated entity (new_start_index,new_end_index,ent_label) .
    """

    if ent[0]>start:
        steps=end-start
        return ([ent[0]+steps,ent[1]+steps,ent[2]])
    else: return ent

class Model(object):
    def __init__(self,path,patterns):
        """Initializes Model instance.
        Args:
            path (str): the path to a spacy model which will be used for NER.
            patterns (list): list of list of patterns used for text cleaning.
        """
        self.nlp=spacy.load("fr_core_news_lg")
        self.matcher = Matcher(self.nlp.vocab)
        self.ner_model=spacy.load(path)
        self.matcher.add("cleaning", patterns,greedy="LONGEST")

    def update(self, new_path, new_patterns):
        """Updates Model instances.
        Args:
            new_path (str): a new path to a spacy model which will be used for NER.
            new_patterns (int): list of list of patterns that will be used for text cleaning.
        """
        self.matcher = Matcher(self.nlp.vocab)
        self.ner_model=spacy.load(new_path)
        self.matcher.add("cleaning", new_patterns,greedy="LONGEST")
    def predict_ner(self,text):
        """Predicts Named Entity recognition in a text.
        Args:
            text (str): text used in the ner
        Returns:
                list: list of tuples describing the recognized entities.
        """
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
        """pseudonymizes text.
        Args:
            doc (Document): the Document object to be pseudonimised.
        Returns:
            (str): pseudonymized text.
        """
        return doc.text
