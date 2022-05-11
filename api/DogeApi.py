# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/19 10:50
Desc    : DogeCloud API的Python实现
"""
import hmac
import json
from hashlib import sha1
from numbers import Number
from urllib import parse

import requests

from api.BaseApi import API


class DogeApi(API):
    def __init__(self, access_key, secret_key, url="https://api.dogecloud.com", proxies=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url
        self.proxies = proxies

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
        with requests.request(method, self.url + path, proxies=self.proxies, data=body, headers={
            'Authorization': authorization,
            'Content-Type': mime
        }) as response:
            return response

    def listDomain(self):
        return self.request("GET", "/cdn/domain/list.json")

    def getUserInfo(self):
        return self.request('GET', '/console/userinfo.json')

    def uploadCert(self, data: dict):
        return self.request("POST", "/cdn/cert/upload.json", data)

    def updateCert(self, domain_id, new_cert_id):
        data: dict[str, int] = {
            'id': domain_id,
            'cert_id': new_cert_id
        }
        return self.request("POST", "/cdn/domain/config.json", data, True)

    def deleteCert(self, cert_id):
        return self.request('POST', '/cdn/cert/delete.json')
