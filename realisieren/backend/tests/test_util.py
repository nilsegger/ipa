from tedious.mdl.fields import StrField
from tedious.mdl.model import Model
from bbbapi.util import sanitize_fields


class NestedMock(Model):

    def __init__(self, name: str):
        super().__init__(name, [
            StrField('name')
        ])


class Mock(Model):

    def __init__(self):
        super().__init__(None, [
            StrField('name'),
            NestedMock('nested')
        ])


def test_sanitize_fields():
    mock = Mock()
    mock['name'].value = '<script>alert("Böse");</script>'
    mock['nested']['name'].value = '<script>alert("Böse");</script>'
    sanitize_fields(mock, ['name', 'nested.name'])

    assert mock['name'].value == '&lt;script&gt;alert("Böse");&lt;/script&gt;'
    assert mock['nested'][
               'name'].value == '&lt;script&gt;alert("Böse");&lt;/script&gt;'
