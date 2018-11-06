from thinkprice.components.resistor import Resistor
from thinkprice.importer.file_board_importer import FileBoardImporter

schematics = ''
with open('samples/text-sample-newline.txt', 'r') as f:
    schematics = f.read()

importer = FileBoardImporter()
importer.import_board('samples/A1502 820-3476-A.brd')
comps = importer.get_components_list()

for comp in comps:
    if comp.retrieve(schematics):
        print(comp.__dict__)

import sys
sys.exit(0)

from thinkprice.importer.pdf_schematic_importer import PdfSchematicImporter
from time import sleep

schematic_importer = PdfSchematicImporter()
schematic_importer.import_schematic('samples/A1502 820-3476-A.12-15.pdf')

while len(schematic_importer.threads) > 0:
    sleep(1)

with open('out.txt', 'w') as f:
    f.write(schematic_importer.output)

