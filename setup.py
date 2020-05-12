from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines()]

setup(
    name='Montpellier_Network',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Visualisation of a road in Montpellier',
    long_description=open('README.md').read(),
    install_requires=INSTALL_REQUIRES,
    url='https://github.com/fanchonherman/project_network.git',
    author='Fanchon Herman, Sahbane Abdesstar, Ryma Lakehal',
    author_email='sahbane.abdesstar@gmail.com'
)
