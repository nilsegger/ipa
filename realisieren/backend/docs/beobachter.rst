==========
Beobachter
==========

.. contents:: :local:

Einführung
==========

Ein Beobachter kontrolliert, ob ein Sensor einen definierten Wert überschritten hat.
Es gibt drei verschieden Arten von Beobachter.

- Zählerstand
    Der Zählerstand Beobachter misst jeweils, wie oft ein Sensor sich meldet und gibt eine Meldung aus, wenn sich dieser genug oft gemeldet hat.
- Richtwert darüber
    Beim Richtwert darüber kann ein Wert definiert werden, welcher nicht überschritten werden darf.
- Richtwert darunter
    Beim Richtwert darunter kann ein Wert definiert werden, welcher nicht unterschritten werden darf.

Klassen
=======

-----------
Interface
-----------

.. autoclass:: bbbapi.beobachter.beobachter.BeobachterInterface
    :members:


-----------
Zählerstand
-----------

.. autoclass:: bbbapi.beobachter.beobachter.ZaehlerstandBeobachter
    :members:

-----------------
Richtwert darüber
-----------------

.. autoclass:: bbbapi.beobachter.beobachter.RichtwertDarueberBeobachter
    :members:

-----------------
Richtwert darunter
-----------------

.. autoclass:: bbbapi.beobachter.beobachter.RichtwertDarunterBeobachter
    :members:
