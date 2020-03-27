from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Gebaeude(Model):

    def __init__(self, name: str = None):
        super().__init__(name, [
            IntField('id'),
            StrField('name', min_len=3, max_len=99)
        ])
