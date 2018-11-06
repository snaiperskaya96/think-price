import threading
import pdfminer.settings
pdfminer.settings.STRICT = False

import pdfminer.high_level
import pdfminer.layout
from io import StringIO


class PdfSchematicImporterWorker(threading.Thread):
    def __init__(self, file_path, pages, parent):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.pages = pages
        self.parent = parent
        self.out_io = StringIO()
        self.output = ''

    def run(self):
        for page in self.pages:
            print('parsing page', str(page))
            self.out_io.truncate(0)
            self.out_io.seek(0)
            self.output = ''
            self.extract_text([self.file_path], maxpages=1, page_numbers=[page - 1])
            self.parent.output_lock.acquire()
            self.parent.output += self.output
            self.parent.elaborated_pages += 1
            self.parent.output_lock.release()
            print('page', str(page), 'parsed')
        self.parent.output_lock.acquire()
        self.parent.threads.remove(self)
        self.parent.output_lock.release()

    def extract_text(self, files=[], outfile='-',
                     _py2_no_more_posargs=None,  # Bloody Python2 needs a shim
                     no_laparams=False, all_texts=None, detect_vertical=None,  # LAParams
                     word_margin=None, char_margin=None, line_margin=None, boxes_flow=None,  # LAParams
                     output_type='text', codec='utf-8', strip_control=False,
                     maxpages=0, page_numbers=None, password="", scale=1.0, rotation=0,
                     layoutmode='normal', output_dir=None, debug=False,
                     disable_caching=False, **other):
        if _py2_no_more_posargs is not None:
            raise ValueError("Too many positional arguments passed.")
        if not files:
            raise ValueError("Must provide files to work upon!")

        # If any LAParams group arguments were passed, create an LAParams object and
        # populate with given args. Otherwise, set it to None.
        if not no_laparams:
            laparams = pdfminer.layout.LAParams()
            for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
                paramv = locals().get(param, None)
                if paramv is not None:
                    setattr(laparams, param, paramv)
        else:
            laparams = None

        if output_type == "text" and outfile != "-":
            for override, alttype in ((".htm", "html"),
                                      (".html", "html"),
                                      (".xml", "xml"),
                                      (".tag", "tag")):
                if outfile.endswith(override):
                    output_type = alttype

        outfp = self.out_io

        for fname in files:
            with open(fname, "rb") as fp:
                pdfminer.high_level.extract_text_to_fp(fp, **locals())

        # squash everything into a non-spaced string
        self.output = ''.join(self.out_io.getvalue().split())


