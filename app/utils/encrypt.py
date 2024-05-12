from django.conf import settings
import hashlib


def md5(data):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf8'))
    obj.update(data.encode('utf8'))
    return obj.hexdigest()
