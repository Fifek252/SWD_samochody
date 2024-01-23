from typing import List, Union, Dict
import pandas as pd
from MainWindow import Ui_MainScreen


""" ___________
|  ______  |    o   o
| |  |____|  |    \__/
| |__________|____\ /
|__________________/
"""

class Cars:
    """
    Class representing set of all cars in data base
    Object Cars should be created before important criteria are chosen
    """
    def __init__(self, path):#, minimalize: List[bool]):
        """
        :param parameters: a dictionary mapping car's id to all its parameters
        :param minimalize: a list specifying if criterion is to be minimalized or not
        """
        self.params = {}

        self.minimalize = [False, False, False, False, True, True, True]
        self.parameters = self.read_as_dict(path)
        """
        :param self.params: a dictionary mapping car's id to considered parameters
        """


    def update_parameters(self,criteria):
        """
        Function updates parameters to understandable form for any algortihm
        It should be called after important criteria are chosen
        Function passes parameter to self.params if it is taken into account
        If parameter is to be maximalized, it is multiplied by -1
        :param criteria: a list speciffying if criterion is taken into account
        """ 

        self.criteria = [True if elem in criteria else False for elem in ['Maksymalna prędkość', 'Pojemność bagażnika', 'Moc silnika', 'Pojemność silnika', 'Przebieg', 'Średnie spalanie', 'Cena']]
        for id, car in self.parameters.items():
            new_criteria = []
            if len(self.criteria) != len(car): print(f"len(car) = {len(car)}, len(criteria) = {len(self.criteria)}")
            for idx, crit in enumerate(car):
                if self.criteria[idx]:
                    if self.minimalize[idx]:
                        new_criteria.append(crit)
                    else:
                        new_criteria.append(-crit)

            self.params[id] = new_criteria


    def get_parameters(self):
        """
        :return: dict mapping car's id to considered parameters
        """
        return self.params
    
    def get_all_parameters(self):
        """
        :return: dict mapping car's id to all its parameters
        """
        return self.parameters

    def read_as_dict(self,path: str) -> Dict[Union[int, float], List[Union[int, float]]]:
            dataframe = pd.read_excel(path)
            database = {}

            m, _ = dataframe.values.shape
            elems = dataframe.values

            for i in range(m-1):
                database[elems[i+1,1]] = [elems[i+1, j+3] for j in range(7)] 
            return database


