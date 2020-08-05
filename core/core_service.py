# encoding: utf-8
"""
File:       core_service
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 10:55
Desc:
"""
from datetime import datetime
import time

from .app_config import AppConfig
from .node_item import NodeItem
from .v2ray_controller import V2rayController
from .node_manager import NodeManager
from .keys import Keyword as K

class CoreService:
    app_config = AppConfig()
    node_config = NodeItem()
    v2ray = V2rayController()
    node_manager = NodeManager()

    @classmethod
    def load(cls):
        cls.app_config.load()
        cls.node_config.load()
        cls.node_manager.load()

    @classmethod
    def status(cls) -> dict:
        running = cls.v2ray.running()
        version = cls.v2ray.version()
        last_subscribe = datetime.fromtimestamp(cls.app_config.last_subscribe).strftime('%Y-%m-%d %H:%M:%S')

        result = {
            K.running: running,
            K.version: version,
            K.proxy_mode: cls.app_config.proxy_mode,
            K.subscribe: cls.app_config.subscribe,
            K.last_subscribe: last_subscribe,
        }

        node = cls.node_config.dump()
        result.update(node)
        return result

    @classmethod
    def subscribe_new(cls, url: str):
        cls.node_manager.update(url)
        cls.app_config.subscribe = url
        cls.app_config.last_subscribe = int(time.time())
        cls.app_config.save()

    @classmethod
    def subscribe_update(cls):
        cls.node_manager.update(cls.app_config.subscribe)
        cls.app_config.last_subscribe = int(time.time())
        cls.app_config.save()

    @classmethod
    def apply_node(cls, index: int) -> bool:
        result = False
        node = cls.node_manager.nodes[index]
        if cls.v2ray.apply_node(node, cls.node_manager.nodes, cls.app_config.proxy_mode):
            cls.node_config = node
            cls.node_config.save()
            result = True

        return result

    @classmethod
    def switch_mode(cls, proxy_mode: int) -> bool:
        result = False
        if (cls.v2ray.apply_node(cls.node_config, cls.node_manager.nodes, proxy_mode)):
            cls.app_config.proxy_mode = proxy_mode
            cls.app_config.save()
            result = True

        return result

    @classmethod
    def node_link(cls, index: int) ->bool:
        return cls.node_manager.nodes[index].link

