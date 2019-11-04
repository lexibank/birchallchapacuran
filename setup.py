from setuptools import setup
import sys
import json

with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)

setup(
    name='lexibank_birchallchapacuran',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_birchallchapacuran'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'birchallchapacuran=lexibank_birchallchapacuran:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=2.0',
    ]
)
