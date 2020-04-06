===========
Controllers
===========

.. contents:: :local:

Einführung
==========

Bei den Controllers wird zwischen Form und List Controller unterschieden.
Ein Form Controller kann Models validieren, erstellen, aktualisiern und löschen.
Die List Controller sind lediglich zum erstellen von Auflistungen.

Form Controller
===============

--------
Personal
--------

.. autoclass:: bbbapi.controller.personal_controller.PersonalController
    :members:

--------
Gebäude
--------

.. autoclass:: bbbapi.controller.gebaeude_controller.GebaeudeController
    :members:

---------
Stockwerk
---------

.. autoclass:: bbbapi.controller.stockwerk_controller.StockwerkController
    :members:

---------
Raum
---------

.. autoclass:: bbbapi.controller.raum_controller.RaumController
    :members:

---------
Sensor
---------

.. autoclass:: bbbapi.controller.sensor_controller.SensorController
    :members:

---------
Material
---------

.. autoclass:: bbbapi.controller.material_controller.MaterialController
    :members:

----------
Beobachter
----------

.. autoclass:: bbbapi.controller.beobachter_controller.BeobachterController
    :members:

----------
Meldung
----------

.. autoclass:: bbbapi.controller.meldung_controller.MeldungController
    :members:

List Controller
===============

----------
Beobachter
----------

.. autoclass:: bbbapi.controller.beobachter_list_controller.BeobachterListController
    :members:

----------------------
Beobachter Materialien
----------------------

.. autoclass:: bbbapi.controller.beobachter_materalien_list_controller.BeobachterMateralienListController
    :members:

----------------------
Gebäude
----------------------

.. autoclass:: bbbapi.controller.gebaeude_list_controller.GebaeudeListController
    :members:

----------------------
Stockwerke
----------------------

.. autoclass:: bbbapi.controller.stockwerke_list_controller.StockwerkeListController
    :members:


----------------------
Räume
----------------------

.. autoclass:: bbbapi.controller.raeume_list_controller.RaeumeListController
    :members:


----------------------
Materialien
----------------------

.. autoclass:: bbbapi.controller.materialien_list_controller.MaterialienListController
    :members:

----------------------
Meldungen
----------------------

.. autoclass:: bbbapi.controller.meldung_list_controller.MeldungListController
    :members:

----------------------
Personal
----------------------

.. autoclass:: bbbapi.controller.personal_list_controller.PersonalListController
    :members:

----------------------
Sensorenen
----------------------

.. autoclass:: bbbapi.controller.sensoren_list_controller.SensorenListController
    :members:

----------------------
Sensoren Beobachter
----------------------

.. autoclass:: bbbapi.controller.sensor_beobachter_list_controller.SensorBeobachterListController
    :members:

----------------------
Sensoren Werte
----------------------

.. autoclass:: bbbapi.controller.sensor_werte_list_controller.SensorWertListController
    :members:
