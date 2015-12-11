#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import socket
import struct


class Storage(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.update(state)


def storage_object_hook(dct):
    return Storage(dct)


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def json_decode(data, *args, **kw):
    return json.loads(data, object_hook=storage_object_hook, *args, **kw)


def json_encode(data, *args, **kw):
    return json.dumps(data, *args, **kw)
