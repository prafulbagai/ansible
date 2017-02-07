"""Module for caching."""
import ast
import json

from django.conf import settings

from modules import REDIS_CLIENT


class Cache(object):
    """Cache class for caching."""

    @classmethod
    def hmset(cls, key_type, mapping):
        try:
            REDIS_CLIENT.hmset(key_type, mapping)
            return True
        except:
            return False

    @classmethod
    def set_key(cls, key, value, key_type, append=False, hmset=False):
        if not append:
            try:
                REDIS_CLIENT.hset(key_type, key, value)
                return True
            except:
                return False

        exists, details = cls.get_key(settings.GROUP_REDIS_KEY, key)
        if not exists:
            return False

        details['group_codes'].append(value)
        try:
            REDIS_CLIENT.hmset(key_type, key, details)
            return True
        except:
            return False

    @classmethod
    def get_key(cls, key_type, key=None):
        try:
            if not key:  # if no key is present, then return all data.
                response = REDIS_CLIENT.hgetall(key_type)
            else:  # else return value of the specific data.
                response = REDIS_CLIENT.hget(key_type, key)
        except:
            return (False, None)

        if not response:
            return (False, None)

        try:
            response = json.loads(response)
        except:
            try:
                response = ast.literal_eval(response)
            except:
                try:
                    response = eval(response)
                except:
                    pass

        return (True, response)
