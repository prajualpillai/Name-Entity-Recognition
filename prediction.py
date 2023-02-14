import os
import spacy
import pandas as pd
from pre_process import PreProcess


class Prediction:

    def __init__(self) -> None:
        self.clean_obj = PreProcess()

    def predict(self, model_path:str, test_data_path:str) -> dict:
        """
        Function performs the following:
            1. Loads the spacy model
            2. Lists all the files in the test directory
            3. Reads each file one by one
            4. Pre-processes the data as required by the model
            5. Performs NER on all the files
            6. Return the extracted values
        
        Args:
            model_path: str - Path where the spacy model is saved
            test_data_path: str - Path where the test_data files are located
        
        Return:
            output_dict: dict - Dictionary having all the Label-Key values

        """
        model = spacy.load(model_path)
        
        file_list = os.listdir(test_data_path)
        
        output_dict = {"Labels": [],
        "Key":[]}

        for file in file_list:
            temp = f"{test_data_path}/{file}"
            with open(temp) as f:
                text = f.readlines()
            text = self.clean_obj.clean_data(text)
            doc = model(text)
            for ent in doc.ents:
                output_dict["Labels"].append(ent.label_)
                output_dict["Key"].append(ent.text)
        
        return output_dict

if __name__=="__main__":

    obj = Prediction()
    out = obj.predict('synthetic_model/model-best','/Users/prajualpillai/Desktop/prajual/pelican_ner/data/test_data/')
    out_df = pd.DataFrame(out)
    out_df.to_csv("output/test_2.csv", index=False)