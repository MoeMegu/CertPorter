#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/19 10:50
Desc    : DogeCloud API的Python实现
"""
import json
import hmac
import requests
from urllib import parse
from api.baseApi import API
from hashlib import sha1


class DogeApi(API):
    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key

    def request(self, method, path, data=None):
        if type(data) is dict:
            body = json.dumps(data)
            mime = 'application/json'
        elif type(data) is str:
            body = parse.quote(data)  # Python 2 可以直接用 urllib.urlencode
            mime = 'application/x-www-form-urlencoded'
        else:
            mime = body = ""

        sign_str = path + "\n" + body
        signed_data = hmac.new(self.secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
        sign = signed_data.digest().hex()
        authorization = 'TOKEN ' + self.access_key + ':' + sign
        response = requests.request(method, self.url + path, data=body, headers={
            'Authorization': authorization,
            'Content-Type': mime
        })
        return response
