import pandas as pd
import functions as fn

### initialise database
dir = "./data"
label_list = [
   "irAE_symptoms",
   "irAE_investigations"
]
database = "irAE"
model = "en_core_web_sm"
annotate = fn.ProdigyFunctions(dir, label_list, database, model)
annotate.database_connect(new_database=True)
annotate.prodigy_connect("ner.manual", "./data/cards.json")