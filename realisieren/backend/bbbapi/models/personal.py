from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Personal(Model):
    """Wiederspiegelt eine Person aus dem Reinigungspersonal oder der
    Administratorgruppe.
    """

    def __init__(self, name: str = None, uuid=None):
        super().__init__(name, [
            UUIDField('uuid', value=uuid),
            StrField('name', min_len=3, max_len=99),
        ])