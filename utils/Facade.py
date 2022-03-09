"""
this file contains the implementation of the Facade class.
this class represents the facade between other defined classes in utlis directory and the main dash app.
"""
from utils.Writer import Writer
from utils.Config import Config
from utils.Model  import Model
from utils.Document import Document
import ast

class Facade(object):
    def __init__(self):
        """
        Initializes facade instances attributes
        """
        self.writer=Writer()
        self.conf=Config()
        self.current_doc=None
        self.model=Model(self.conf.model_path,self.conf.patterns)
    def update(self, new_path, new_patterns):
        """updates model and conf attributes based in the new settings inputs
        Args:
            new_path (str): a new path to ner spacy model.
            new_patterns (str): a new patterns used to clean text.
        Returns:
            (bool): whether the attributes are successfully updated or not.
        """
        try:
            self.model.update(new_path,ast.literal_eval(new_patterns))
            self.conf.update(new_path,ast.literal_eval(new_patterns))
            return True
        except:
            return False
    def set_document(self,text):
        """ sets Facade current_doc attributes
        Args:
            text (str): file content used the initlaize the DOucment instance.
        """
        self.current_doc=Document(text)
    def run_model(self):
        """ runs the ner model and sets current_doc entities.
        """
        if self.current_doc.ents is None:
            self.current_doc.set_ents(self.model.predict_ner(self.current_doc.text))
    def is_file_in(self):
        """ verifies if the current_doc is already traited.
        """
        return self.writer.is_file_in(self.current_doc.hash)
    def pseudonymise_doc(self):
        """pseudonimses the original text.
        """
        if self.current_doc.pseudo_text is None:
            self.current_doc.set_pseudo_text(self.model.pseudonymise(self.current_doc))
    def save_doc(self):
        """Save files and results.
        """
        try:
            self.writer.save_doc(self.current_doc)
            return True
        except:
            return False
