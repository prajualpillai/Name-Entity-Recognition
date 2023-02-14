import os
import re
import pdfplumber
import pandas as pd
import json


class PreProcess:

    def __init__(self) -> None:
        pass

    def clean(self, text:str) -> str:
        """
        Removes \n from the string and lowers all the string values

        Args:
            text: str - String which has to be cleaned
        
        return:
            modified_text: str - Modeified string
        """
        modified_text = re.sub('\n'," ",text)
        modified_text = modified_text.lower()
        return modified_text
    
    def clean_data(self, text_file:list) -> str:
        """
        Cleans the data, multiple operations can be added as required

        Args: 
            text_file: lits - List containing all the string values
        
        return:
            final: str - Combined string from all the values in the list
        """
        final = " "
        for text in text_file:
            text = self.clean(text)
            final += text

        return final


    def save_txt(self, output_path:str, text:str, file:str, index="") -> None:
        """
        Saves the file in .txt format in the specified path

        Args:
            output_path: str - Output path of the text file
            text: str - The string value to be saved
            file: str - Portion of the filename
            index(Optional): str - The index of the data in a .csv file
        """

        with open(f"{output_path}{file[:-4]}{index}.txt",'w') as f:
                    print(text,file=f)

    
    
    def csv_to_text(self, input_path:str, output_path:str) -> None:
        """
        Converts csv data to text

        Args:
            input_path: str - Path where all the .csv data is stored
            output_path: str - Path where all the .txt files have to be stored
        
        """
        file_list = os.listdir(input_path)

        for file in file_list:
            temp_path = f"{input_path}/{file}"
            if temp_path.lower().endswith(".csv"):
                import pdb; pdb.set_trace()
                data = pd.read_csv(temp_path)
                for index, row in data.iterrows():
                    temp_text = row["data"]
                    temp_text = self.clean(temp_text)
                    self.save_txt(output_path, temp_text, file, f"_{index}")


    
    def pdf_to_text(self, input_path, output_path):
        """
        Converts pdf data to text

        Args:
            input_path: str - Path where all the .pdf data is stored
            output_path: str - Path where all the .txt files have to be stored
        """        
        file_list = os.listdir(input_path)

        for file in file_list:
            temp = f"{input_path}/{file}"
            if temp.endswith(".pdf") or temp.endswith(".PDF"):
                temp_text = ""
                with pdfplumber.open(temp) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        temp_text += " "+text
                
                temp_text = self.clean(temp_text)
                self.save_txt(output_path, temp_text, file)
    
    

if __name__=="__main__":
    
    obj = PreProcess()

    # obj.pdf_to_text("data/pdf_data", "data/text_data/")
    
    obj.csv_to_text("data/csv_data", "data/text_data/")
            