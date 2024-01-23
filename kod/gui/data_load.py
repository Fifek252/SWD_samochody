from typing import Dict,Union,List
import pandas as pd

def read_as_dict(path: str) -> Dict[Union[int, float], List[Union[int, float]]]:
        dataframe = pd.read_excel(path)
        database = {}

        m, _ = dataframe.values.shape
        elems = dataframe.values

        for i in range(m-1):
            database[elems[i+1,1]] = [elems[i+1, j+2] for j in range(8)] 
        return database