import os
import tempfile
from subprocess import  Popen

from django.conf import settings
from django.http import StreamingHttpResponse

class StreamingConvertedPdf:

    def __init__(self, dock_obj, download=True):
        self.doc = dock_obj
        self.download = download
        self.tmp_path = settings.MEDIA_ROOT + 'tmp/'

    def validate_document(self):
        if not self.doc.name.split('.')[-1] in ('doc', 'docm', 'docx'):
            raise Exception('The input file must have one format from this: doc, docm, docx')

    def check_tmp_folder(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    def convert_to_pdf(self):
        self.validate_document()
        self.check_tmp_folder()
        with tempfile.NamedTemporaryFile(prefix=self.tmp_path) as tmp:
            tmp.write(self.doc.read())
            process = Popen(['lowriter', '--convert-to', 'pdf', tmp.name, '--outdir', self.tmp_path])
            process.wait()
            self.tmp_path = tmp.name + '.pdf'

    def get_file_name(self):
        return self.doc.name.split('.')[0] + '.pdf'

    def stream_content(self):
        self.convert_to_pdf()
        res = StreamingHttpResponse(open(self.tmp_path, 'rb'), content_type='application/pdf')
        if self.download:
            res['Content-Disposition'] = 'attachment; filename="{}"'.format(self.get_file_name())
        return res

    def __del__(self):
        try:
            if os.path.exists(self.tmp_path):
                os.remove(self.tmp_path)
        except IOError:
            print('Error deleting file')


class ConvertFileModelField(StreamingConvertedPdf):

    def get_content(self):
        self.convert_to_pdf()
        return {'path': self.tmp_path, 'name': self.get_file_name()}

    def stream_content(self):
        pass
