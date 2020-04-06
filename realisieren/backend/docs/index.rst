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
   beobachter
   models
   controllers
   resources


Oft benutzte Typen in diesem Projekt
====================================

------
Rollen
------

Bei den Rollen wird lediglich zwischen einem Adminitrator und einer Person aus dem Personal unterschieden.

.. autoclass:: bbbapi.common_types.Roles
   :members:

--------
Sensoren
--------

Es gibt vordefinierte Sensoren, möchte man einen Neuen hinzufügen, so muss
für diesen einen :class:`~decoder.Decoder` erstellt werden und einen
Eintrag in die folgende Enumerierung eingetragen werden.

.. autoclass:: bbbapi.common_types.SensorArt
   :members:

----------
Beobachter
----------

Bei den Sensoren gibt es drei verschiedene Arten.

.. autoclass:: bbbapi.common_types.BeobachterArt
   :members:

---------
Meldungen
---------

Eine Meldung wird entweder automatisch von einem Beobachter erstellt oder manuell eines Personal.

.. autoclass:: bbbapi.common_types.MeldungsArt
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
