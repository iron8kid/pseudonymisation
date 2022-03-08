
import pandas as pd
import datetime
import os
import ast

class Writer(object):
    def __init__(self):
        self._dict_results = {'file name':-1,
                                'hash': -1,
                                'pseudonymised file': -1,
                                'validated': -1,
                                'ents':-1
                                   }
        self.f_path='interview.txt'
        self.pseudo_f_path='interview_pseudonymised.txt'
        self._data_path='data'
        if not os.path.exists('data'):
            os.mkdir('data')

        self._results_file=os.path.join('data','results.csv')
        if not os.path.exists(self._results_file):
            pd.DataFrame(columns=self._dict_results.keys()).to_csv(self._results_file,index=False)

        self._corpus_path = os.path.join('data','corpus')
        if not os.path.exists(self._corpus_path):
            os.mkdir(self._corpus_path)
        self.f_name='interview.txt'
        self.pseudo_f_name='interview_pseudonymised.txt'
        self.df=None
        self.read_check_files()

    def read_check_files(self):
        df=pd.read_csv(self._results_file)
        files=os.listdir(self._corpus_path)
        df=df[(df['file name'].isin(files)) & (df['pseudonymised file'].isin(files))]
        df.to_csv(self._results_file,index=False)
        self.df=df
        df_files=set(self.df['file name']).union(set(self.df['pseudonymised file']))
        f_to_remove=set(files)-df_files
        for file in f_to_remove:
            filename, file_extension = os.path.splitext(file)
            if file_extension=='.txt':
                tmp_path=os.path.join(self._corpus_path,file)
                os.remove(tmp_path)


    def is_file_in(self,hash):
        return (hash in self.df.hash.tolist())

    def set_doc_instances(self,doc,override=True):
        def get_non_existent_path(f_name):
            """
            Get the path to a filename which does not exist by incrementing path.
            """
            f_path=os.path.join(self._corpus_path,f_name)
            if not os.path.exists(f_path):
                return f_name
            filename, file_extension = os.path.splitext(f_name)
            i = 1
            new_f_name = "{}-{}{}".format(filename, i, file_extension)
            new_f_path=os.path.join(self._corpus_path,new_f_name)
            while os.path.exists(new_f_path):
                i += 1
                new_f_name = "{}-{}{}".format(filename, i, file_extension)
                new_f_path=os.path.join(self._corpus_path,new_f_name)
            return new_f_name
        if override:
            doc.set_f_names(get_non_existent_path(self.f_name),get_non_existent_path(self.pseudo_f_name))

        else:
            row=self.df[self.df.hash==doc.hash].iloc[-1]
            doc.set_f_names(row['file name'],row['pseudonymised file'])
            doc.set_validated(row.validated)
            doc.set_ents(ast.literal_eval(row.ents))
            with open(os.path.join(self._corpus_path,doc.pseudo_f_name), 'r',encoding="utf-8") as f:
                doc.set_pseudo_text(f.read())
    def save_doc(self,doc):
        self.df.drop(self.df[(self.df['file name']==doc.f_name) & (self.df['pseudonymised file']==doc.pseudo_f_name)].index,inplace=True)
        self.df=self.df.append(doc.get_doc_dic(),ignore_index=True)
        self.df.to_csv(self._results_file,index=False)
        with open(os.path.join(self._corpus_path,doc.f_name), 'w',encoding="utf-8") as f:
            f.write(doc.text)
        with open(os.path.join(self._corpus_path,doc.pseudo_f_name), 'w',encoding="utf-8") as f:
            f.write(doc.pseudo_text)
