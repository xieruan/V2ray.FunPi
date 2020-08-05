# encoding: utf-8
"""
File:       proxy_mode
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 15:56
Desc:
"""
from enum import Enum

class ProxyMode(Enum):
    Direct = 0
    ProxyAuto = 1
    ProxyGlobal = 2