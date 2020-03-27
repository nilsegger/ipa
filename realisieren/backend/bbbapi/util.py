from tedious.mdl.fields import StrField
from tedious.util import KeyPathsIter
import bleach


def sanitize_fields(model, fields):
    """Bereinigt alle String Felder in fields von möglicherweise bösartige Tags.

    Args:
        fields: Liste von Feldern zum Bereinigen.
        model: Model welches Bereinigt wird.

    Returns:
        model
    """

    if isinstance(fields, list):
        fields = KeyPathsIter(fields)

    for key, _iter in fields:

        if _iter is None:
            field = model[key]
            assert isinstance(field,
                              StrField), "Nur String Felder können von Tags bereinigt werden."
            if not field.empty:
                field.value = bleach.clean(field.value)
        else:
            sanitize_fields(model[key], _iter)

    return model
