from prodigy.components.db import connect
import os


class annotation_preprocessor:
    def __init__(self, input_dir, output_dir, label_list, n):
        self.input_dir = input_dir # directory to read in raw data
        self.output_dir = output_dir # path to save processed data
        self.label_list = label_list
        self.n = n
    
    ### pre-processing functions
    def file_reader(self):
        """
        The function opens the file at the specified file path using the "open" function, 
        reads all the lines in the file using the "readlines" method, and returns the 
        resulting list of lines.
        """
        return open(self.input_dir).readlines()
    
    def card_generator(self, data):
        """
        Description: A function that takes a list of medical text as input, and returns a 
        modified list of medical text where a page break is added at the end of every n 
        sentences.

        Syntax: card_generator(data: List[str], n: int) -> List[str]

        Parameters:
        - data (List[str]): A list of strings where each string represents a sentence or a paragraph 
        of the medical text.
        - n (int): An integer that represents the number of sentences after which a page break needs 
        to be added.
        
        Returns:
        A modified list of medical text where a page break is added at the end of every n sentences.

        """
        # currently assuming medical text is in a list format
        for i in range(len(data)):
            sentences = data[i].split(". ")
            result = ""
            # creates a page break at the end of every n sentences
            for j in range(len(sentences)):
                result += sentences[j]
                if (j+1) % self.n == 0 and j < len(sentences)-1: # check if this is the nth sentence
                    result += ". \n" # add a new line character at the end of the sentence
                else:
                    result += ". "
            data[i] = result
        return data
    
    def card_concatenator(self, data):
        result = []
        for i, line in enumerate(data):
            if i % self.n == 0:  # keep every 5th line
                result.append(line)
            else:
                # remove page breaks
                result.append(line.replace('\n', ' '))
        return result

    def write_to_file(self, data):
        """
        This function takes in two arguments: file_path and data. file_path is a string representing 
        the path of the file to which the data is to be written and data is the list of strings that 
        needs to be written to the file. The function opens the file in write mode, writes the lines 
        of data to the file, and then closes it.
        """
        with open(self.output_dir, "w") as f:
            f.writelines(data)
    
    def label_processor(self):
        """
        This is a Python function that takes in a single parameter, annotation_list, 
        which is expected to be a list of string values. The purpose of the function 
        is to convert this list into a single comma-separated string of annotations 
        that can be consumed by the Prodigy tool.

        The body of the function consists of a single line that uses the built-in join() 
        method of strings to concatenate all of the elements in the input annotation_list 
        into a single string with each element separated by a comma. This new string is 
        then returned by the function.
        """
        return(",".join(self.label_list))

class database_connection:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
    
    def connect(self, new_database = False):
        db = connect()
        if new_database == True: # option to make new database
            db.add_dataset(self.dataset_name)
            #check of database was added
            assert self.dataset_name in db
        return db.get_dataset(self.dataset_name)

class annotation_module:
    def __init__(self, input_dir, prod_source, model, label, output_dir):
        self.input_dir = input_dir # directory for data to be annotated
        self.prod_source = prod_source # name of dataset from Prodigy to use/create to store all annotations
        self.model = model # path to the spaCy model to use for Prodigy recipe
        self.label = label # labels for annotation tasks
        self.output_dir = output_dir # directory to save converted spaCy files

    def prodigy_connection(self, recipe):
        """
        Inputs:
        - recipe (string): the name of the Prodigy recipe to use
        - data_name (string): the name of the dataset in Prodigy to use or create
        - data_source (string): the path to the data file or directory to use as input
        - model (string): the path to the spaCy model to use for the Prodigy recipe
        - label (string): the label for the annotation task

        The function returns the result of the os.system() function, which runs a command 
        in the system shell. The command being executed is a Prodigy command, which uses 
        the parameters provided to run an annotation task on the specified data source 
        using the specified model and label. The resulting annotations are added to the 
        specified dataset in Prodigy.
        """
        cmd = f"prodigy {recipe} {self.prod_source} {self.model} {self.input_dir} --label {self.label}"
        os.system(cmd)
        
    ###problem - keeps generating a base config file despite linking the desired one in the command, unsure how to fix atm
    ###TODO - fix above
    def data_to_spacy(self, dataset, config_path):
        """
        Inputs:
        - dataset: data to convert to .spacy format
        - output_dir: a string representing the directory path where the data files are saved
        - config_path: a string representing the path of the config file that will be used by Prodigy.

        The function then builds the Prodigy command based on the input arguments and runs it using os.system().
        """
        cmd = f"prodigy data-to-spacy {self.output_dir} --ner {dataset} --config {config_path}"
        os.system(cmd)

    def data_to_json(self, dataset):
        """
        Inputs:
        - dataset: data to convert to .json format
        - output_dir: a string representing the directory path where the data files are saved
        """
        cmd = f"prodigy db-out {dataset} > {self.output_dir}"
        os.system(cmd)
