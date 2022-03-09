"""
this file contains the implementation the Document class.
a Document represents the text being processed.
"""
import hashlib

class Document(object):
    def __init__(self,text):
        """Initializes the Document instance
        Args:
            text (str): text content of the file.
        """
        self.text=text.decode()
        self.pseudo_text=None
        self.hash=str(hashlib.md5(text).hexdigest())
        self.ents=None
        self.validated=False
        self.f_name=None
        self.pseudo_f_name=None
    def set_ents(self,ents):
        """sets Document's ents attribute
        Args:
            ents (list): list of tuple describing entities in the text.
        """
        self.ents=ents
    def set_pseudo_text(self,text):
        """sets the pseudonymized text attribute
        Args:
            text (str): pseudonymized text.
        """
        self.pseudo_text=text
    def set_f_names(self,f_name,pseudo_f_name):
        """sets Document f_name and pseudo_f_name attributes
        Args:
            f_name (str): filename in which the original text will be saved in the corpus directory.
            pseudo_f_name (str): filename in which the pseudonymized text will be saved in the corpus directory.
        """
        self.f_name=f_name
        self.pseudo_f_name=pseudo_f_name
    def set_validated(self,validated):
        """sets Document validated attribute
        Args:
            validated (bool): if the user validated the obtained results or not.
        """
        self.validated=validated
    def get_doc_dic(self):
        """ transforms the doc to a dict type
        Returns:
            (dict): dict representing the Document attributes to be saved in the results.csv file.
        """
        return {'file name':self.f_name,
                'hash': self.hash,
                'pseudonymised file': self.pseudo_f_name,
                'validated': self.validated,
                'ents':str(self.ents)}
