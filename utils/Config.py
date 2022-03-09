"""
This file contains the implementation of the class Config.
This class is responsible for reading and updating the config.ini file.
"""

from configparser import ConfigParser
import ast

class Config(object):
    def __init__(self):
        """Initializes the config instance by reading the config.ini file.
        """
        self.config=ConfigParser()
        self.config.read('config.ini')
        self.model_path=self.config['NER_model']['path']
        self.patterns=ast.literal_eval(self.config['Cleaning']['patterns'])
    def update(self, new_path, new_patterns):
        """updates Config.ini file
        Args:
            new_path (str): new path to ner spacy model.
            new_patterns (list): new patterns used to clean text.
        """
        self.model_path=new_path
        self.config.set('NER_model','path',new_path)
        self.patterns=new_patterns
        self.config.set('Cleaning','patterns',str(new_patterns))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
