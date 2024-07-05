from setuptools import setup, find_packages

setup(
    name= 'anonymity_api',
    version= '1.0.0',
    packages= find_packages(),
    description= ('A Python library offering conventional anonymity functions, as well as Workload-Aware anonymity.'),
    url = 'https://github.com/farosilva0/anonymity_api',
    keywords= 'anonymity privacy',
    long_description=open('README.md').read(),
    license= 'MIT',
    long_description_content_type='text/markdown',
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Security'
    ]
)
