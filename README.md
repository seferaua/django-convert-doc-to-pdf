**Django convert .doc file to pdf**

This package allows you to convert .doc, .docm, .docx to pdf document.
It is based on libreoffice which allows you to convert .doc files.

This package could be return converted .pdf like new file or or immediately file in view mode.
Also you can convert .doc for Django model. Just pass the file from the request, model object and model field.

**Installation instruction**
- Install library Libreoffice

`sudo apt-get install -y libreoffice`

- Install library

`pip install djangoconvertvdoctopdf`

Inside a code:

Input parameters for StreamingConvertedPdf:
- Required: `dock_obj`
- No mandatory: `download`
    - If you want to receive the file after conversion, set: `download=True` by default.
    - if you want to get a view after conversion, set: `download=False`.

`djangoconvertvdoctopdf.convertor import StreamingConvertedPdf`

```python
def custom_view(request):
    form = forms.MyCustomFrom(request.POST, request.FILES)
    if form.is_valid():
        r_file = request.FILES['my_file']
        inst = StreamingConvertedPdf(r_file)
        return inst.stream_content()
    # return something
```

Input parameters for ConvertFileModelField:
- Required: `dock_obj`

`djangoconvertvdoctopdf.convertor import ConvertFileModelField`

```python
from django.core.files import File

def custom_view(request):
    form = forms.MyCustomFrom(request.POST, request.FILES)
    if form.is_valid():
        r_file = request.FILES['my_file']
        inst = ConvertFileModelField(r_file)
        r_file = inst.get_content()
        doc_obj = models.Document()
        doc_obj.pdf_doc = File(open(r_file.get('path'), 'rb'))
        doc_obj.pdf_doc.name = r_file.get('name')
        doc_obj.save()
        return HttpResponse('ok')
    # return something
```
