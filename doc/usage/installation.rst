Commands to install network_montpellier package 
=================================

.. role:: bash(code)
   :language: bash


To install this package, you just need to type the following command in the prompt.

.. code-block:: bash

    $ pip install git+https://https://github.com/fanchonherman/project_network

However, you will need to have installed the osmnx package beforehand.
You need just to put :

.. code-block:: bash

    $ conda install osmnx=0.10
    Or, 
    $ pip install osmnx=0.10


For Windows users there might be some trouble with installing the fiona package.
So, follow the next step in order : 

.. code-block:: bash

    $ pip install osmnx
    $ pip install Rtree
    $ conda install -c conda forge libspatialindex=1.9.3
    $ pip install osmnx
    Install all the packages required up to fiona.
    $ conda install -c conda-forge geopandas
    Say yes to everything.
    Once done, lauch :
    $ pip install osmnx=0.10