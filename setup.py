from setuptools import setup
from Montpellier_Network import __version__ as current_version

setup(
    name='Montpellier_Network',
    version=current_version,
    packages=["network_montpellier", "network_montpellier.make_map"],
    license='MIT',   
    author='Fanchon Herman, Sahbane Abdesstar, Ryma Lakehal',
    description='Visualisation of a road in Montpellier',
    long_description=open('README.md').read(),
    url='https://github.com/fanchonherman/project_network.git',
    author_email='fanchon.herman974@gmail.com, sahbane.abdesstar@gmail.com '
    zip_safe=False
)