from abc import ABC, abstractmethod


class AbstractBoardImporter(ABC):
    @abstractmethod
    def import_board(self, param):
        pass
    
    @abstractmethod
    def get_components_list(self):
        pass

    @abstractmethod
    def export_to(self, to):
        pass
