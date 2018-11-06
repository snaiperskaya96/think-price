from thinkprice.importer.pdf_schematic_importer import PdfSchematicImporter
from time import sleep

schematic_importer = PdfSchematicImporter()
schematic_importer.import_schematic('samples/A1502 820-3476-A.pdf')

while len(schematic_importer.threads) > 0:
    sleep(1)

import sys
sys.exit(0)

importer = FileBoardImporter()
importer.import_board('samples/A1502 820-3476-A.brd')
#importer.export_to('/tmp/test.brd')

comps = importer.get_components_list()
print(comps[0].name)
