from pip.req import parse_requirements
from pip.download import PipSession

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=PipSession())
from setuptools import setup, find_packages

# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name             = 'pyyamlschema',
    version          = '0.9',
    description      = 'Easy to Make JSON-Schema With YAML',
    author           = 'Deokyu Lim',
    author_email     = 'hong18s@gmail.com',
    url              = 'https://github.com/RavenKyu/YAML_Schema',
    download_url     = 'https://github.com/RavenKyu/YAML_Schema/archive/0.9.tar.gz',
    install_requires = reqs,
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['yaml', 'json', 'json-schema', 'converter', 'yaml-schema'],
    python_requires  = '>=3',
    package_data     = {},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)