"""
This file contains the implementation of the class Model.
This class is responsible for cleaning text, detecting NER, and text pseudonymization.
"""

import spacy
from spacy.matcher import Matcher
import pandas as pd

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

    def pseudonymise(self, doc):
        """pseudonymizes text.
        Args:
            doc (Document): the Document object to be pseudonimised.
        Returns:
            (str): pseudonymized text.
        """
        # PER part

        pseudonyms = []
        # this list stores the indices of the start / end of text that doesn't contain PER
        pseudonyms_indices = [0]
        text = ''
        for ent in doc.ents:
            if ent[2] == 'PER':
                name = doc.text[ent[0]:ent[1]]
                pseudonym = self.pseudo_name(name)
                pseudonyms.append(pseudonym)
                pseudonyms_indices.append(ent[0])
                pseudonyms_indices.append(ent[1])
        pseudonyms_indices.append(len(doc.text))
        for i, pseudonym in enumerate(pseudonyms):
            text = text + doc.text[pseudonyms_indices[2*i]:pseudonyms_indices[2*i+1]] + pseudonym
        # add the last part
        text = text + doc.text[pseudonyms_indices[-2]:pseudonyms_indices[-1]]

        doc.text = text
        return doc.text

    def pseudo_name(self, name):
        """
        Pseudonymizes the name.
        Args:
            name: the name to be replaced
        Returns:
            the pseudonym
        """
        # source: https://www.data.gouv.fr/fr/datasets/liste-de-prenoms/#community-resources
        df_names_data_base = pd.read_csv('utils/analyses-trails-in-france-prenoms-hf.csv', header=[
            0])
        # pseudonyms.csv is a subset of analyses-trails-in-france-prenoms-hf.csv, all the names
        # start with a capital letter, and it is shuffled
        df_pseudonums = pd.read_csv('utils/pseudonyms.csv', header=[0])
        df_used_names = pd.read_csv('utils/used_names.csv', header=[0])
        df_indices = pd.read_csv('utils/indices.csv', header=[0])
        # if this name has been replaced before
        if df_used_names['name'].isin([name]).any():
            row_used_names = df_used_names[df_used_names['name'] == name]
            return row_used_names.pseudonym.item()

        # if this name appears for the first time
        else:
            for i, row in df_names_data_base.iterrows():
                if row['01_prenom'] == name:
                    gender = row['02_genre']
                    if gender == 'm':
                        index = df_indices['current_m_index'][0] + 1
                        # find the next male name, and it can't be the same name
                        while df_pseudonums['02_genre'][index] != 'm' or df_pseudonums['01_prenom'][index] == name:
                            index += 1
                        pseudonym = df_pseudonums['01_prenom'][index]
                        df_used_names = df_used_names.append({'name': name, 'pseudonym': pseudonym}, ignore_index=True)
                        df_indices['current_m_index'] = index
                        df_used_names.to_csv('utils/used_names.csv', index=False)
                        df_indices.to_csv('utils/indices.csv', index=False)
                        return pseudonym
                    # if the gender is female or m/f or f/m
                    else:
                        index = df_indices['current_f_index'][0] + 1
                        # find the next female name, and it can't be the same name
                        while df_pseudonums['02_genre'][index] == 'm' or df_pseudonums['01_prenom'][index] == name:
                            index += 1
                        pseudonym = df_pseudonums['01_prenom'][index]
                        df_used_names = df_used_names.append({'name': name, 'pseudonym': pseudonym}, ignore_index=True)
                        df_indices['current_f_index'] = index
                        df_used_names.to_csv('utils/used_names.csv', index=False)
                        df_indices.to_csv('utils/indices.csv', index=False)
                        return pseudonym

            # if the name doesn't exist in the data base, it will be replaced with "$PER$"
            df_used_names = df_used_names.append({'name': name, 'pseudonym': '$PER$'}, ignore_index=True)
            df_used_names.to_csv('utils/used_names.csv', index=False)
            return '$PER$'
