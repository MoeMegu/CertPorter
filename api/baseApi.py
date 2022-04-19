#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod


class API(ABC):

    @abstractmethod
    def request(self, method, path, data):
        ...
