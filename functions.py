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
        marker_list = [
            "History of Present Illness:",
            "Past Medical History:",
            "Physical ___:",
            "Pertinent Results:"
        ]
    
        sections = []  # list to store each section as a dictionary
    
        for index in range(len(marker_list)-1):
            start_marker = marker_list[index]
            end_marker = marker_list[index + 1]

            start_index = self.report.find(start_marker)
            end_index = self.report.find(end_marker)
            
            if start_index != -1 and end_index != -1:  # if both markers were found
                section_text = self.report[start_index:end_index].strip()
                sections.append({'text': section_text})
            
            elif start_index != -1 and end_index == -1:  # if only the start marker was found
                section_text = self.report[start_index:].strip()
                sections.append({'text': section_text})
                
        return sections  # return the final cleaned report as a list of dictionaries
    
    def extract_HOPC(self):
        start_keyword = "History of Present Illness:"
        end_keyword = "Past Medical History:"

        # Find the start and end indexes
        start_index = self.report.find(start_keyword)
        end_index = self.report.find(end_keyword)

        if start_index != -1 and end_index != -1:
            # Extract the information
            history_of_present_illness = self.report[start_index + len(start_keyword):end_index]

            # Trim the leading/trailing whitespaces
            history_of_present_illness = history_of_present_illness.strip()

            return {"text": history_of_present_illness}



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
        
