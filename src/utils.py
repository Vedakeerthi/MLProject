import os
import sys
import pandas as pd

from src import exception 
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path,'wb') as file_obj:
            pd.dump(obj, file_obj)
    
    except Exception as e:
        raise exception.CustomException(e,sys)