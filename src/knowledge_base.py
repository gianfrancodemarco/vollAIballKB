from typing import List

from pyswip import Prolog


# Singleton
class KnowledgeBase:

    def __init__(self):
        self.prolog = Prolog()
        
    def assertz(self, fact: str):
        self.prolog.assertz(fact)
        
    def query(self, query: str) -> List:
        return self.prolog.query(query)