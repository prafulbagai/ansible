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
    def set_key(cls, key, value, key_type, dict_key=False):
        """
        Set key in a Redis.

        Can set following key-value pairs:-
            1) {key_type: {key: value}}, ie simple dict.
            2) {key_type: {key: {name: name, phone: phone}}}, ie nested dict
        - key_type = either codes/groups (settings variables)
        - key = group_name
        - value = The updated value.
        - dict_key = If value is nested dict, and a particular key(dict_key)
                     of nested dict needs to be updated
        """
        if not dict_key:  # if not nested dict, then set value directly.
            try:
                REDIS_CLIENT.hset(key_type, key, value)
                return True
            except:
                return False

        exists, details = cls.get_key(settings.GROUP_REDIS_KEY, key)
        if not exists:
            return False

        if dict_key not in details:
            return False

        # if value is of 'list' type, then append.
        if isinstance(details[dict_key], list):
            details[dict_key].append(value)
        else:  # else assign value directly.
            details[dict_key] = value

        try:
            REDIS_CLIENT.hmset(key_type, details)
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

    @classmethod
    def del_key(cls, key_type, key=None):
        try:
            if not key:  # if no key is present, then delete the complete dict.
                REDIS_CLIENT.delete(key_type)
            else:  # else delete the specific key.
                exists, data = cls.get_key(key_type, key)
            return True
        except:
            return False
