import spacy
from spacy.tokens import DocBin
import json
from spacy.cli.train import train 

class ModelTraining:

    def __init__(self) -> None:
        pass

    def load_training_data(self, data_path:str) -> list:
        """
        Creates the training data from the text file as required by the spacy model

        Args:
            data_path: str - Path where the .json/.jsonl files are located
        
        Return:
            training_data: list - List containing all the training data
        """
        
        # Had to create this differentiation as the output from label-studio has changed

        if data_path.endswith(".jsonl"):
            with open(data_path, 'r') as json_file:
                content = list(json_file)
                flag = True
        else:
            with open(data_path, 'r') as json_file:
                content = list(json.load(json_file))
                flag = False
        
        training_data = []

        for json_str in content:
            if flag:
                temp_content = json.loads(json_str)
                text = temp_content["data"]
                label = temp_content["label"]
                s = []
                for l in label:
                    s.append(tuple(l))
            else:
                temp_content = json_str
                text = temp_content["text"]
                label = temp_content["label"]
                s = []
                for l in label:
                    s.append(tuple([l["start"], l["end"], l["labels"][0]]))
            
            training_data.append((text,s))

        return training_data
    
    def create_spacy_data(self, spacy_model, training_data, output_path, flag="train") -> None:
        """
        Method does the following:
            1. Creates the data as required by spacy
            2. Converts the data to a DocBin
            3. Saves the data as a .spacy file to be used by the model
        
        Args:
            spacy_model: SpacyObject - A blank spacy model
            training_data: list - List containing all the training data
            output_path: str - Path where the .spacy file has to be saved
        
        Return:
            None
        """
        db = DocBin()

        for text, annotations in training_data:
            doc = spacy_model(text)
            ents = []
            annotations = set(annotations)
            for start, end, label in annotations:
                span = doc.char_span(start, end, label=label)
                if span != None:
                    ents.append(span)
            doc.ents = ents
            db.add(doc)
        db.to_disk(f"{output_path}/{flag}.spacy")
    
    def train_model(self, model_info:dict) -> None:
        """
        Method trains the spacy model
        
        Args: 
            model_info: dict - Dictionary containing data required by model
                model_info = {'spacy_train_data_path':'',
                              'spacy_train_dev_path':'', 
                              'path_to_save_model':'', 
                              'config_file_path':''}
        
        Return:
            None
        """
        
        config_file_path = model_info.get('config_file_path','')
        training_data = model_info.get('spacy_train_data_path','')
        dev_data = model_info.get('spacy_train_dev_path','')
        output_path = model_info.get('path_to_save_model','')
        train(config_path=config_file_path, 
              overrides={"paths.train": training_data, 
                         "paths.dev": dev_data},
              output_path = output_path)

    def train_model_main(self, info:dict) -> None:
        """
        Wrapper method which orchestrates the following:
            1. Calls the method to create the training and dev data
            2. Loads an empty spacy mode
            3. Calls the method to create train and dev spacy data
            4. Calls the method to initiate training

        Args: 
            info: dict - Dictionary having the data required by the method 
                info = {
                    "training_data_path":"",
                    "dev_data_path":"",
                    "train_flag":"",
                    "dev_flag":"",
                    "model_path":"",
                    "spacy_output_path":"",
                    "config_file_path":""
                }
        
        Return:
            None
        """

        training_data = self.load_training_data(info.get("training_data_path",""))
        dev_data = self.load_training_data(info.get("dev_data_path",""))
        spacy_model = spacy.blank("en")
        
        self.create_spacy_data(spacy_model, training_data,
                               output_path=info.get("spacy_output_path",""), 
                               flag=info.get("train_flag",""))
        
        self.create_spacy_data(spacy_model, dev_data,
                               output_path=info.get("spacy_output_path",""), 
                               flag=info.get("dev_flag",""))
        
        model_info = {'spacy_train_data_path': f'{info.get("spacy_output_path","")}{info.get("train_flag","")}.spacy',
                      'spacy_dev_data_path': f'{info.get("spacy_output_path","")}{info.get("dev_flag","")}.spacy',
                      'config_file_path': info.get("config_file_path",""),
                      'path_to_save_model': info.get("model_path","")}
        
        self.train_model(model_info)



if __name__=="__main__":
    obj = ModelTraining()
    info = {
            "training_data_path":"data/train_data/json_files/train/training_data_2.json",
            "dev_data_path":"data/train_data/json_files/dev/dev_data_2.json",
            "train_flag":"train_2",
            "dev_flag":"dev_2",
            "model_path":"synthetic_model/",
            "spacy_output_path":"data/spacy_files/",
            'config_file_path': 'config/custom_config.cfg'
        }
    obj.train_model_main(info)