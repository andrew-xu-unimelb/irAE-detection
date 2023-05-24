from prodigy.components.db import connect
import os

class AnnotationProcess:
    def __init__(self, dir, label_list, dataset_name, model):
        self.dir = dir # directory to read / write files
        self.label_list = label_list # labels for annotations
        self.n = 5 # number of sentences per card
        self.dataset_name = dataset_name
        self.model = model # path to spaCy model to use for Prodigy recipe

    def card_generator(self, input_string):
        # reformats text breaks to make annotation cards more consistent in length
        sentences = input_string.replace("\n", "")
        sentences = sentences.split(". ")
        result = ""
        for i in range(len(sentences)):
            result += sentences[i]
            if (i+1) % self.n == 0 and i < len(sentences-1):
                result += ". \n"
            else:
                result += ". "
        return result 
    
    def label_processor(self):
        return(",".join(self.label_list))

    def database_connect(self, new_database = False):
        db = connect()
        if new_database == True: # option to make new database
            db.add_dataset(self.dataset_name)
            assert self.dataset_name in db
        return db.get_dataset(self.dataset_name)
    
    def prodigy_connect(self, recipe):
        labels = self.label_processor()
        cmd = f"prodigy {recipe} {self.dataset_name} {self.model} {self.dir} --label {labels}"
        os.system(cmd)
    
