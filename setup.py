from setuptools import setup, find_packages

setup(
    name='montpellier_network',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    author='Fanchon Herman, Sahbane Abdesstar, Ryma Lakehal',
    description='Visualisation of a road in Montpellier ',
    long_description=open('README.txt').read(),
    install_requires=['numpy', 'osmnx'],  # on va rajouter d'autre après
    url='https://github.com/fanchonherman/project_network.git',
    author_email='fanchon.herman974@gmail.com, sahbane.abdesstar@gmail.com '

)
