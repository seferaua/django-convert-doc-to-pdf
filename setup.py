from setuptools import setup, find_packages

setup(
    name='djangoconvertvdoctopdf',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['django>=1.5'],
    url='https://github.com/seferaua/django-convert-doc-to-pdf',
    long_description="This package allows you to convert .doc, .docm, .docx to pdf document."
                "You can find detailed information here: https://github.com/seferaua/django-convert-doc-to-pdf",
    author="Sergey Savchenko"
)
