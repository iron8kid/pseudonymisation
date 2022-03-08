from utils.Writer import Writer
from utils.Config import Config
from utils.Model  import Model
from utils.Document import Document
import ast

class Facade(object):
    def __init__(self):
        self.writer=Writer()
        self.conf=Config()
        self.current_doc=None
        self.model=Model(self.conf.model_path,self.conf.patterns)
    def update(self, new_path, new_patterns):
        try:
            self.model.update(new_path,ast.literal_eval(new_patterns))
            self.conf.update(new_path,ast.literal_eval(new_patterns))
            return True
        except:
            return False
    def set_document(self,text):
        self.current_doc=Document(text)
    def run_model(self):
        if self.current_doc.ents is None:
            self.current_doc.set_ents(self.model.predict_ner(self.current_doc.text))
    def is_file_in(self):
        return self.writer.is_file_in(self.current_doc.hash)
    def pseudonymise_doc(self):
        if self.current_doc.pseudo_text is None:
            self.current_doc.set_pseudo_text(self.model.pseudonymise(self.current_doc))
    def save_doc(self):
        try:
            self.writer.save_doc(self.current_doc)
            return True
        except:
            return False
