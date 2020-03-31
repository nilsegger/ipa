from typing import Tuple, Dict, Any, List

from bbbapi.models.beobachter import Beobachter

from bbbapi.controller.sensor_controller import SensorController
from bbbapi.models.material import Material
from bbbapi.util import sanitize_fields
from bbbapi.common_types import Roles, BeobachterArt
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface


class BeobachterController(ModelController):

    def __init__(self):
        super().__init__('beobachter', 'id')
        self.sensor_controller = SensorController()

    async def _select_stmt(self, model: Model, join_foreign_keys=False):

        if not join_foreign_keys:
            return """SELECT dev_euiSensor as "sensor.dev_eui" , name, art, wertName as "wertName", ausloeserWert as "ausloeserWert", stand FROM beobachter WHERE id=$1"""
        else:
            return """
                    SELECT beobachter.name, beobachter.art, wertName as "wertName", ausloeserWert as "ausloeserWert", stand,
                     sensoren.dev_eui AS "sensor.dev_eui",
                     sensoren.name AS "sensor.name",
                     sensoren.art AS "sensor.art",
                     raeume.id AS "raum.id",
                     raeume.name AS "raum.name",
                     stockwerke.id AS "stockwerk.id",
                     stockwerke.name AS "stockwerk.name",
                     gebaeude.id AS "gebaeude.id",
                     gebaeude.name AS "gebaeude.name"
                     FROM beobachter
                     LEFT JOIN sensoren ON beobachter.dev_euisensor = sensoren.dev_eui
                     LEFT JOIN raeume on sensoren.idraum = raeume.id
                     LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
                     LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                     WHERE beobachter.id=$1 
                """

    async def _insert_stmt(self):
        return "INSERT INTO beobachter(dev_euisensor, name, wertname, art, ausloeserwert) VALUES ($1, $2, $3, $4, $5) RETURNING id"

    async def _insert_values(self, model: Model):
        return model["sensor"]["dev_eui"].value, model["name"].value, model[
            "wertName"].value, model["art"].value.value, model[
                   "ausloeserWert"].value

    async def _update_stmt(self):
        return "UPDATE beobachter SET dev_euiSensor=coalesce($2, dev_euiSensor), name=coalesce($3, name), wertName=coalesce($4, wertName), art=coalesce($5, art),  ausloeserwert=coalesce($6, ausloeserwert), stand=coalesce($7, stand) WHERE id=$1"

    async def _update_values(self, model: Model):
        return (model["id"].value, *await self._insert_values(model), model["stand"].value)

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt Beobachter und setzt ID."""
        await self.validate(connection, model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(
            await self._insert_stmt(), *await self._insert_values(model))
        return model

    @property
    def identifiers(self) -> List[str]:
        """Ein Beobachter wird druch seine ID identifiziert."""
        return ["id"]

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[
        ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen Beobachter bearbeiten."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Administratoren dürfen gewisse Werte einlesen lassen während das Reinigungspersonal nur lesen darf."""
        return await self.get_permissions_for_role(
            requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Administratoren dürfen gewisse Werte einlesen lassen während das Reinigungspersonal nur lesen darf."""
        if role == Roles.ADMIN.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ_WRITE,
                'art': Permissions.READ_WRITE,
                'wertName': Permissions.READ_WRITE,
                'ausloeserWert': Permissions.READ_WRITE,
                'stand': Permissions.READ_WRITE,
                'sensor': {
                    'dev_eui': Permissions.READ_WRITE,
                    'art': Permissions.READ,
                    'name': Permissions.READ
                },
                'raum': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
                ,
                'stockwerk': {
                    'id': Permissions.READ,
                    'name': Permissions.READ,
                    'niveau': Permissions.READ,
                },
                'gebaeude': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
            }
        elif role == Roles.PERSONAL.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ,
                'art': Permissions.READ,
                'wertName': Permissions.READ,
                'ausloeserWert': Permissions.READ,
                'stand': Permissions.READ,
                'sensor': {
                    'dev_eui': Permissions.READ,
                    'art': Permissions.READ,
                    'name': Permissions.READ
                },
                'raum': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
                ,
                'stockwerk': {
                    'id': Permissions.READ,
                    'name': Permissions.READ,
                    'niveau': Permissions.READ,
                },
                'gebaeude': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
            }
        return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model,
                       _type: ValidationTypes):

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['sensor.dev_eui', 'name', 'art'])

            if model["art"].value == BeobachterArt.RICHTWERT_DARUEBER or model[
                "art"].value == BeobachterArt.RICHTWERT_DARUNTER:
                await model.validate_not_empty(['wertName', 'ausloeserWert'])

        if not model["sensor"]["dev_eui"].empty:
            if await self.sensor_controller.get(connection,
                                                model["sensor"]) is None:
                raise ValidationError(['sensor.dev_eui'], "Sensor existiert nicht.")

        sanitize_fields(model, ['name', 'wertName'])

    async def add_material(self, connection: SQLConnectionInterface, beobachter: Beobachter, material: Material):
        """Fügt ein Material einem Beobachter hinzu."""
        stmt = "INSERT INTO materialzubeobachter(idmaterial, idbeobachter, anzahl) VALUES ($1, $2, $3) RETURNING id"
        return await connection.fetch_value(stmt, material["id"].value, beobachter["id"].value, material["anzahl"].value)

    async def remove_material(self, connection: SQLConnectionInterface, _id):
        """Löscht die Reihe mit _id."""
        stmt = "DELETE FROM materialzubeobachter WHERE id=$1"
        await connection.execute(stmt, _id)