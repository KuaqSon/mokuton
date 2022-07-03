import re
import unicodedata


def normalized_title(text):
    try:
        text = text.strip().lower()
        text = re.sub(u"đ", "d", text)
        text = unicode(text, "utf-8")  # noqa
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")

    return str(text)
