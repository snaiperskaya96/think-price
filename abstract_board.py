from abc import ABC, abstractmethod

class AbstractBoard(ABC):
    @abstractmethod
    def import_board(self, param):
        pass
    
    @abstractmethod
    def get_components_list(self):
        pass