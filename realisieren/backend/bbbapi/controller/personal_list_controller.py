from tedious.mdl.list_controller import ListController
from bbbapi.models.personal import Personal


class PersonalListController(ListController):
    """Erstellt eine Auflistung aller Personal Mitglieder."""

    def __init__(self):
        super().__init__(Personal)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        if join_foreign_keys:
            return """SELECT personal.uuid AS "uuid", name, logins.username AS "benutzername", logins.role AS "rolle" FROM personal JOIN logins on personal.uuid = logins.uuid LIMIT {} OFFSET {}""".format(limit, offset)
        else:
            return """SELECT uuid, name, FROM personal JOIN logins on personal.uuid = logins.uuid LIMIT {} OFFSET {}""".format(limit, offset)




