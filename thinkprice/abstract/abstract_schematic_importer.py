from abc import ABC, abstractmethod


class AbstractSchematicImporter(ABC):
    @abstractmethod
    def import_schematic(self, param):
        pass

    @abstractmethod
    def retrieve_part_info(self, part):
        pass
