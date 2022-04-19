#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/19 10:44
Desc    : CDN提供商API实现的抽象基类
"""
from abc import ABC
from abc import abstractmethod


class API(ABC):

    @abstractmethod
    def request(self, method, path, data):
        ...
