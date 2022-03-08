from configparser import ConfigParser
import ast

class Config(object):
    def __init__(self):
        self.config=ConfigParser()
        self.config.read('config.ini')
        self.model_path=self.config['NER_model']['path']
        self.patterns=ast.literal_eval(self.config['Cleaning']['patterns'])
    def update(self, new_path, new_patterns):
        self.model_path=new_path
        self.config.set('NER_model','path',new_path)
        self.patterns=new_patterns
        self.config.set('Cleaning','patterns',str(new_patterns))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
