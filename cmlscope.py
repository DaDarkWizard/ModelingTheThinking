from typing import List, Tuple, Dict
from cmltokens import *
from cmlclasses import *

class CMLScope:
    def __init__(self):
        self.parent = None
        self.stack: List[Tuple[TokenType, any]] = list()
        #self.base_dimensions
        self.dimensions: Dict[str, Dimension] = dict()
        self.units: Dict[str, Unit] = dict()
