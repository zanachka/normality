import os
from banal import decode_path
from normality.stringify import stringify
from normality.cleaning import collapse_spaces, category_replace
from normality.constants import UNICODE_CATEGORIES, WS
from normality.transliteration import ascii_text


def _safe_name(file_name, sep):
    """Convert the file name to ASCII and normalize the string."""
    file_name = stringify(file_name)
    if file_name is None:
        return

    file_name = ascii_text(file_name)
    file_name = category_replace(file_name, UNICODE_CATEGORIES)
    file_name = collapse_spaces(file_name)
    if file_name is None or not len(file_name):
        return

    file_name = file_name.replace(WS, sep)
    return file_name[:200]


def safe_filename(file_name, sep='_', default=None, extension=None):
    """Create a secure filename for plain file system storage."""
    if file_name is None:
        return decode_path(default)

    file_name = decode_path(file_name)
    file_name = os.path.basename(file_name)
    file_name, _extension = os.path.splitext(file_name)
    file_name = _safe_name(file_name, sep=sep) or decode_path(default)
    extension = _safe_name(extension or _extension, sep=sep)
    if extension and len(file_name):
        file_name = '.'.join((file_name, extension))
    if file_name is None:
        return default
    return file_name