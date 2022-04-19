#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding:utf-8
"""
Author  : Moe
Time    : ${DATE} ${TIME}
Desc    : julydate/acmeDeliver API的Python客户端实现
"""

import hashlib
import random
from time import time

import requests


class AcmeDeliverClient:
    def __init__(self, host="https://0.0.0.0:9443", domain="", file="", passwd="passwd"):
        self.host = host
        self.domain = domain
        self.file = file
        self.timestamp = str(int(time())).encode()
        # 构建 checksum
        checksum = hashlib.md5()
        checksum.update(str(random.randint(0, 32767)).encode())
        checksum.update(self.timestamp)
        self.checksum = checksum.hexdigest()
        # 构建 token
        sign = hashlib.md5()
        sign.update(domain.encode())
        sign.update(file.encode())
        sign.update(passwd.encode())
        sign.update(self.timestamp)
        sign.update(self.checksum.encode())
        self.sign = sign.hexdigest()

    def getCert(self):
        return requests.get(self.host, params={
            "domain": self.domain,
            "file": self.file,
            "t": self.timestamp,
            "sign": self.sign,
            "checksum": self.checksum
        })
