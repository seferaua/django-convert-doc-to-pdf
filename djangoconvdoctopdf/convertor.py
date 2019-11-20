import os
import tempfile
from subprocess import  Popen

from django.conf import settings
from django.http import StreamingHttpResponse

class ValidReceivedContent(object):

    def __set__(self, instance, value):
        if not value.name.split('.')[1] in ['doc', 'docm', 'docx']:
            raise Exception('The input file must have one format from this: doc, docm, docx')
        instance.__dict__['doc'] = value

class StreamingConvertedPdf(object):

    doc = ValidReceivedContent()

    def __init__(self, dock_obj, download=True):
        self.doc = dock_obj
        self.download = download
        self.tmp_path = settings.MEDIA_ROOT

    def convert_to_pdf(self):
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

    def __init__(self, dock_obj, model, field_name, download=True):
        super().__init__(dock_obj, download)
        self.model = model
        self.field_name = field_name

    def stream_content(self):
        pass

    def get_content(self):
        self.convert_to_pdf()
        custom_path = self.model._meta.get_field(self.field_name).upload_to
        if custom_path:
            self.tmp_path + custom_path
        return {'path': self.tmp_path, 'name': self.get_file_name()}