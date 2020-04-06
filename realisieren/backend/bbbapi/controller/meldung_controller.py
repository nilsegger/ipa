from datetime import datetime
from typing import Tuple, Dict, Any, List

from bbbapi.controller.beobachter_controller import BeobachterController

from bbbapi.util import sanitize_fields

from bbbapi.controller.raum_controller import RaumController

from bbbapi.controller.sensor_controller import SensorController

from bbbapi.common_types import Roles, MeldungsArt, BeobachterArt
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface


class MeldungController(ModelController):
    """Controller für die Erstellung, Aktualisierung und Löschung von Meldungen."""

    def __init__(self):
        super().__init__('meldungen', 'id')
        self.sensor_controller = SensorController()
        self.raum_controller = RaumController()
        self.beobachter_controller = BeobachterController()

    async def _select_stmt(self, model: Model, join_foreign_keys=False):

        if not join_foreign_keys:
            return """SELECT 
                    art, datum, beschreibung, bearbeitet,
                    dev_euiSensor as "sensor.dev_eui",
                    idRaum as "raum.id",
                    uuidPersonal as "personal.uuid",
                    idBeobachter as "beobachter.id"
                    FROM meldungen
                    WHERE id=$1
                    """
        else:
            return """SELECT 
                    meldungen.art, meldungen.datum, meldungen.beschreibung, meldungen.bearbeitet,
                    sensoren.dev_eui as "sensor.dev_eui",
                    sensoren.name as "sensor.name",
                    sensoren.art as "sensor.art",
                    sensoren.art as "sensor.art",
                    beobachter.id as "beobachter.id",
                    beobachter.name as "beobachter.name",
                    beobachter.stand as "beobachter.stand",
                    beobachter.wertName as "beobachter.wertName",
                    beobachter.ausloeserWert as "beobachter.ausloeserWert",
                    raeume.id as "raum.id",
                    raeume.name as "raum.name",
                    stockwerke.id as "stockwerk.id",
                    stockwerke.name as "stockwerk.name",
                    stockwerke.niveau as "stockwerk.niveau",
                    gebaeude.id as "gebaeude.id",
                    gebaeude.name as "gebaeude.name",
                    personal.uuid as "personal.uuid",
                    personal.name as "personal.name",
                    logins.role as "personal.rolle"
                    FROM meldungen
                    LEFT JOIN sensoren ON meldungen.dev_euisensor = sensoren.dev_eui
                    LEFT JOIN beobachter ON meldungen.idBeobachter = beobachter.id
                    LEFT JOIN raeume ON meldungen.idRaum = raeume.id
                    LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
                    LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                    LEFT JOIN personal ON meldungen.uuidpersonal = personal.uuid
                    LEFT JOIN logins ON personal.uuid = logins.uuid
                    WHERE meldungen.id=$1
                    """

    async def _insert_stmt(self):
        return "INSERT INTO meldungen(dev_euisensor, idbeobachter, idraum, uuidpersonal, art, datum, beschreibung) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id"

    async def _insert_values(self, model: Model):
        return model["sensor"]["dev_eui"].value, model["beobachter"]["id"].value, model["raum"]["id"].value, model["personal"]["uuid"].value, model["art"].value.value, datetime.now(), model["beschreibung"].value

    async def _update_stmt(self):
        return "UPDATE meldungen SET dev_euisensor=coalesce($2, dev_euisensor), idraum=coalesce($3, idraum), uuidpersonal=coalesce($4, uuidpersonal), beschreibung=coalesce($5, beschreibung), bearbeitet=coalesce($6, bearbeitet) WHERE id=$1"

    async def _update_values(self, model: Model):
        return model["id"].value, model["sensor"]["dev_eui"].value, model["raum"]["id"].value, model["personal"]["uuid"].value, model["beschreibung"].value, model["bearbeitet"].value

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt Meldung und setzt die neue ID."""

        if model["art"].value == MeldungsArt.MANUELL:

            if not model["beobachter"]["id"].empty:
                await self.beobachter_controller.get(connection, model["beobachter"], join_foreign_keys=True)
                print(model["beobachter"]["raum"]["id"].value)
                model["raum"]["id"].value = model["beobachter"]["raum"]["id"].value

        await self.validate(connection, model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), *await self._insert_values(model))

        if model["art"].value == MeldungsArt.MANUELL and not model["beobachter"]["id"].empty:
            if model["beobachter"]["art"].value == BeobachterArt.ZAEHLERSTAND:
                model["beobachter"]["stand"].value = 0
                await self.beobachter_controller.update(connection, model["beobachter"])

        return model

    @property
    def identifiers(self) -> List[str]:
        """Die ID identifiziert eine Meldung"""
        return ["id"]

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[
        ManipulationPermissions, Dict[str, Any]]:
        """Administratoren dürfen Erstellen, AKtualisieren und Löschen.
        Das Reinigunspersonal hat die gleichen Permissions, abgesehen von Löscen, dies dürfen sie nicht."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        elif requester is not None and requester.role == Roles.PERSONAL.value:
            return ManipulationPermissions.CREATE_UPDATE, {}
        else:
            return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Beide Rollen dürfen die nötigen Werte einlesen lassen. Die Art wird automatisch auf Manuell gesetzt."""
        return await self.get_permissions_for_role(requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Beide Rollen dürfen die nötigen Werte einlesen lassen. Die Art wird automatisch auf Manuell gesetzt."""
        if role in [Roles.ADMIN.value, Roles.PERSONAL.value]:
            return {
                'id': Permissions.READ,
                'art': Permissions.READ,
                'datum': Permissions.READ,
                'bearbeitet': Permissions.READ_WRITE,
                'beschreibung': Permissions.READ_WRITE,
                'sensor': {
                    'dev_eui': Permissions.READ_WRITE,
                    'name': Permissions.READ,
                    'art': Permissions.READ
                },
                'beobachter': {
                    'id': Permissions.READ_WRITE,
                    'name': Permissions.READ,
                    'art': Permissions.READ,
                    'wertName': Permissions.READ,
                    'ausloeserWert': Permissions.READ,
                    'stand': Permissions.READ
                },
                'raum': {
                    'id': Permissions.READ_WRITE,
                    'name': Permissions.READ
                },
                'stockwerk': {
                    'id': Permissions.READ,
                    'name': Permissions.READ,
                    'niveau': Permissions.READ
                },
                'gebaeude': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                },
                'personal': {
                    'uuid': Permissions.READ,
                    'name': Permissions.READ
                }
            }

    async def validate(self, connection: SQLConnectionInterface, model: Model,
                       _type: ValidationTypes):
        if _type == ValidationTypes.CREATE:

            if model["art"].value == MeldungsArt.MANUELL:
                await model.validate_not_empty(['personal.uuid'])
            else:
                await model.validate_not_empty(['beobachter.id'])

            await model.validate_not_empty(['raum.id', 'beschreibung'])

        if not model["raum"]["id"].empty:
            if await self.raum_controller.get(connection, model["raum"]) is None:
                raise ValidationError(["raum.id"], "Raum existiert nicht.")

        if not model["sensor"]["dev_eui"].empty:
            # Prüft das der Sensor im ausgewählten Raum liegt.
            sensor = await self.sensor_controller.get(connection, model["sensor"])
            if sensor is None:
                raise ValidationError(["sensor.dev_eui"], "Sensor existiert nicht.")
            elif sensor["raum"]["id"].value != model["raum"]["id"].value:
                raise ValidationError(['sensor.dev_eui', 'raum.id'], "Sensor liegt nicht im Raum.")

        sanitize_fields(model, ['beschreibung'])


