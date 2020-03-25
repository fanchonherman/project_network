
from setuptools import setup, find_packages

setup(
    name='my_module',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Animation on osmnx graphs',
    long_description=open('README.txt').read(),
    install_requires=['numpy', 'osmnx'],## on va rajouter d'autre après
    url='https://github.com/fanchonherman/project_network',
    author='Sahbane Abdesstar, Fanchon Herman, Rima ..',
    author_email='sahbane.abdesstar@gmail.com, '
)
