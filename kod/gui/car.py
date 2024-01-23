from typing import List, Union, Dict
import pandas as pd

""" _____________
|  ________  |    o   o
| |  |____|  |    \__/
| |__________|____\ /
|__________________/
"""

class Cars:
    """
    Class representing set of all cars in data base
    Object Cars should be created before important criteria are chosen
    """
    def __init__(self, parameters: Dict[Union[int, str], List[Union[int, float]]], minimalize: List[bool]):
        """
        :param parameters: a dictionary mapping car's id to all its parameters
        :param minimalize: a list specifying if criterion is to be minimalized or not
        """
        self.params = {}

        self.minimalize = minimalize
        self.parameters = parameters
        """
        :param self.params: a dictionary mapping car's id to considered parameters
        """


    def update_parameters(self, criteria: List[bool]):
        """
        Function updates parameters to understandable form for any algortihm
        It should be called after important criteria are chosen
        Function passes parameter to self.params if it is taken into account
        If parameter is to be maximalized, it is multiplied by -1
        :param criteria: a list speciffying if criterion is taken into account
        """
        for id, car in self.parameters.items():
            new_criteria = []

            for idx, crit in enumerate(car):
                if criteria[idx]:
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




