# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/19 12:20
Desc    : julydate/acmeDeliver API的Python客户端实现
"""

import hashlib
import random
from time import time

import requests


class AcmeDeliverClient:
    def __init__(self, host="https://localhost:9443", passwd="passwd", proxies=None):
        self.host = host
        self.passwd = passwd
        self.proxies = proxies

    def getCert(self, domain, file):
        timestamp = str(int(time())).encode()
        # 构建 checksum
        checksum = hashlib.md5()
        checksum.update(str(random.randint(0, 32767)).encode())
        checksum.update(timestamp)
        checksum = checksum.hexdigest()
        # 构建 token
        sign = hashlib.md5()
        sign.update(domain.encode())
        sign.update(file.encode())
        sign.update(self.passwd.encode())
        sign.update(timestamp)
        sign.update(checksum.encode())
        sign = sign.hexdigest()
        with requests.get(self.host, params={
            "domain": domain,
            "file": file,
            "t": timestamp,
            "sign": sign,
            "checksum": checksum
        },proxies=self.proxies) as res:
            return res.content
