from setuptools import setup
import os

with open(os.path.join(os.getcwd(), 'VERSION')) as version_file:
    version = version_file.read().strip()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    author='Marcus V.',
    author_email='mvrp21@inf.ufpr.br',
    name='clikan',
    url='https://github.com/mvrp21/clikan',
    version=version,
    description='A fork of clikan - for improved personal use',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['clikan'],
    install_requires=[
        'Click',
        'click-default-group',
        'pyyaml',
        'rich'
    ],
    entry_points='''
        [console_scripts]
        clikan=clikan:clikan
    ''',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Environment :: Console'
    ]
)
