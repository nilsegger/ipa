.. BBB Building Management documentation master file, created by
   sphinx-quickstart on Mon Mar 16 11:15:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BBB Building Management's documentation
=======================================

Dies ist die technische Dokumentation für den Python Quellcode im Backend.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   decoder


Sensoren
========

Es gibt vordefinierte Sensoren, möchte man einen Neuen hinzufügen, so muss
für diesen einen :class:`~decoder.Decoder` erstellt werden und einen
Eintrag in die folgende Enumerierung eingetragen werden.

.. autoclass:: common_types.SensorTypes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
