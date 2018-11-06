import threading
import numpy
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from thinkprice import think_settings
from thinkprice.abstract.abstract_schematic_importer import AbstractSchematicImporter
from thinkprice.importer.pdf_schematic_importer_worker import PdfSchematicImporterWorker


class PdfSchematicImporter(AbstractSchematicImporter):
    def __init__(self):
        self.output = ''
        self.elaborated_pages = 0
        self.pages = 0
        self.threads = []
        self.output_lock = threading.Lock()

    def import_schematic(self, file_path):
        self.pages = self.get_pages_count(file_path)

        threads = think_settings.SCHEMATIC_IMPORTER_THREADS if \
            think_settings.SCHEMATIC_IMPORTER_THREADS <= self.pages else self.pages

        chunks = numpy.array_split(range(1, self.pages + 1), threads)
        self.output_lock.acquire()
        for chunk in chunks:
            new_thread = PdfSchematicImporterWorker(file_path, list(chunk), self)
            new_thread.start()
            self.threads.append(new_thread)
        self.output_lock.release()

    def get_pages_count(self, file_path):
        with open(file_path, 'rb') as pdf_file:
            parser = PDFParser(pdf_file)
            document = PDFDocument(parser, '')
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed(file_path)
            pages = PDFPage.create_pages(document)
            num_pages = 0
            for page_count, value in enumerate(pages, 1):
                num_pages = page_count

            return num_pages

    def retrieve_part_info(self, part):
        pass
