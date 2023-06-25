from prodigy.components.db import connect
import os

class ProdigyFunctions:
    def __init__(self, dir, label_list, dataset_name, model):
        self.dir = dir # directory to read / write files
        self.label_list = label_list # labels for annotations
        self.n = 5 # number of sentences per card
        self.dataset_name = dataset_name
        self.model = model # path to spaCy model to use for Prodigy recipe
    
    def label_processor(self):
        return(",".join(self.label_list))

    def database_connect(self, new_database = False):
        db = connect()
        if new_database == True: # option to make new database
            db.add_dataset(self.dataset_name)
            assert self.dataset_name in db
        return db.get_dataset(self.dataset_name)
    
    def prodigy_connect(self, recipe, file):
        labels = self.label_processor()
        cmd = f"prodigy {recipe} {self.dataset_name} {self.model} {file} --label {labels}"
        os.system(cmd)
    
class AnnotationProcess:
    def __init__(self, report):
        self.report = report
    
    def clean_report(self):
        # cuts out pieces of the discharge summary that's not relevant to the use case
        start_marker = "History of Present Illness:"
        marker_list = [
            "History of Present Illness:"
            "Past Medical History:",
            "Social History:",
            "Physical ___:",
            "Pertinent Results:",
            "Brief Hospital Course:",
            "Medications on Admission:",
            "Discharge Disposition:"
        ]
        start_index = self.report.find(start_marker)
        final_report = ""
        index = 0
        for i in marker_list:
            new_index = self.report.find(i)
            if new_index == -1:
                new_index = len(self.report)
            
            
        end_index = self.report.find(end_marker)
        if start_index == -1:
            start_index = 0
        if end_index == -1:
            end_index = len(self.report)
        return self.report[start_index:end_index].strip()

    def card_generator(self, n=5):
        input_string = self.clean_report(self.report)
        # reformats text breaks to make annotation cards more consistent in length
        sentences = input_string.replace("\n", "")
        sentences = sentences.split(".")
        result = ""
        for i in range(len(sentences)):
            result += sentences[i]
            if (i+1) % n == 0 and i < len(sentences)-1:
                result += ". \n"
            else:
                result += ". "
        result += "\n"
        return result 
        
