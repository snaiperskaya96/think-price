from thinkprice.components.component import Component
import re
from thinkprice.utils.utils import is_number

class Resistor(Component):
    def __init__(self, *args, **kwargs):
        super(Resistor, self).__init__(*args, **kwargs)
        self.resistance = ''
        self.tolerance = ''
        self.power_rating = ''

    # This will soon become a shitter
    def retrieve(self, schematic):
        schematics = schematic.split('\n')
        for i in range(len(schematics)):
            try:
                line = schematics[i]
                if line.startswith(self.name):
                    offset = self.get_offset(schematics[i:i+4])
                    if offset != -1:
                        self.resistance = schematics[offset + i + 1]
                        self.tolerance = schematics[offset + i + 2]
                        self.power_rating = schematics[offset+ i + 3]
                        self.line = i
                        return True
            except IndexError:
                pass
        return False
    
    def get_offset(self, schematics):
        if re.match(r'\d\%', schematics[2]):
            return 0
        if re.match(r'\d\%', schematics[3]):
            return 1
        return -1
