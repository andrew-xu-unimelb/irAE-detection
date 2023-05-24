import os

class model_training:
    def __init__(self, config_dir, output_dir):
        self.config_dir = config_dir
        self.output_dir = output_dir

    def train(self):
        cmd = f"spacy train {self.config_dir} --output {self.output_dir}"
        os.system(cmd)