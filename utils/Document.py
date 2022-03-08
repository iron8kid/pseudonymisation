import hashlib

class Document(object):
    def __init__(self,text):
        self.text=text.decode()
        self.pseudo_text=None
        self.hash=str(hashlib.md5(text).hexdigest())
        self.ents=None
        self.validated=False
        self.f_name=None
        self.pseudo_f_name=None
    def set_ents(self,ents):
        self.ents=ents
    def set_pseudo_text(self,text):
        self.pseudo_text=text
    def set_f_names(self,f_name,pseudo_f_name):
        self.f_name=f_name
        self.pseudo_f_name=pseudo_f_name
    def set_validated(self,validated):
        self.validated=validated
    def get_doc_dic(self):
        return {'file name':self.f_name,
                'hash': self.hash,
                'pseudonymised file': self.pseudo_f_name,
                'validated': self.validated,
                'ents':str(self.ents)}
