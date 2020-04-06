========
Decoders
========

.. contents:: :local:

Einführung
==========

Das Decoders Modul enthält die verschiedenen Sensor Dekodierer.
Die Aufgabe eines Dekodierers ist einen Sensor Wert entgegenzunehmen und
diesen in die verschiedenen Werte, wie zum Beispiel Temperatur, Licht und
CO2 aufzuteilen und diese wieder zurückzugeben.

Klassen
=======

---------
Interface
---------

.. autoclass:: bbbapi.decoders.decoder.Decoder
    :members:

-------------
Elsys ERS CO2
-------------

.. autoclass:: bbbapi.decoders.elsys.ElsysDecoder
    :members:

----------
Adeunis RF
----------

.. autoclass:: bbbapi.decoders.adeunis.AdeunisDecoder
    :members:

----
Tabs
----

.. autoclass:: bbbapi.decoders.tabs.TabsDecoder
    :members:
