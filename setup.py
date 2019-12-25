from setuptools import setup, find_packages

kwargs = {
    'name': 'sotools',
    'version': '1.2.0',
    'description': 'Tools and ',
    'author': 'Dave Vieglais',
    'url': 'https://github.com/datadavev/sotools',
    'license': 'Apache License, Version 2.0',
    #'packages': ['sotools', 'binder_setup'],
    'packages': find_packages(),
    'package_data': {},
    'install_requires': [
        'rdflib','rdflib-jsonld'
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    'keywords': (
        'schema.org', 'data', 'dataset',
    ),
    'entry_points': {
        'console_scripts': [
        ],
    }
}
setup(**kwargs)
