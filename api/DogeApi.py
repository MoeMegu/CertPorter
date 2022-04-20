#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/19 10:50
Desc    : DogeCloud API的Python实现
"""
import hmac
import json
import sys
from hashlib import sha1
from urllib import parse

import requests
from requests.exceptions import SSLError

from api.BaseApi import API
from main import logger


class DogeApi(API):
    def __init__(self, access_key, secret_key, url="https://api.dogecloud.com"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    def request(self, method, path, data={}, json_mode=False):
        if json_mode:
            body = json.dumps(data)
            mime = 'application/json'
        else:
            body = parse.urlencode(data)  # Python 2 可以直接用 urllib.urlencode
            mime = 'application/x-www-form-urlencoded'
        sign_str = path + "\n" + body
        signed_data = hmac.new(self.secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
        sign = signed_data.digest().hex()
        authorization = 'TOKEN ' + self.access_key + ':' + sign
        try:
            with requests.request(method, self.url + path, data=body, headers={
                'Authorization': authorization,
                'Content-Type': mime
            }) as response:
                return response
        except SSLError as e:
            logger.debug(e)
            logger.error("无法建立SSL连接, 请检查是否启用了网络代理")
            sys.exit()

    def listDomain(self):
        return self.request("get", "/cdn/domain/list.json")
