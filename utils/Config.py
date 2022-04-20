#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : Moe
Time    : 2022/4/20 11:12
Desc    : 解析配置文件用工具类
"""
import sys

import yaml
from yaml.parser import ParserError

from api.DogeApi import DogeApi
from main import logger


class Config:
    loaded = False

    def __init__(self, cfg_file="config.yml"):
        self.cfg_file = cfg_file
        cfg = {}
        # 读取配置文件
        try:
            with open(self.cfg_file, 'r', encoding='utf-8') as cfg_file:
                cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
                loaded = True
        except FileNotFoundError as e:
            logger.debug(e)
            logger.error("配置文件不存在")
        except ParserError as e:
            logger.debug(e)
            logger.error("配置文件格式错误")
        # 校验并处理数据
        try:
            assert cfg['cert-list'] is None or cfg['cert-list'][0]['name'] == "" ,"未配置证书列表"
        except KeyError as e:
            logger.debug(e)
            logger.error('证书列表中未读取到"name"键, 请检查格式')
            sys.exit()
        else:
                self.certs=['cert-list']

        with DogeApi(cfg['dogecloud']['access_id'],cfg['dogecloud']['secret_key']).listDomain() as res:
            if res.status_code != 200:
                raise ConnectionError("API未正确响应, 请检查连接与参数")
            elif res['err_code'] == "ERROR_AUTHORIZATION_FAILED":
                raise ValueError("API验证失败, 请检查AccessKey与SecretKey")
            elif res['code']!=200:
                logger.debug(res)
                logger.error("API未正确响应,状态码:%d,错误代码:'%s'错误信息:'%s'"%(res.json()['code'],res.json()['err_code'],res.json()['msg']))
                raise Exception()
            self.remote_domain_list = {}
            # iter(res.json()['data']['domains'])
        # TODO 迭代域名


