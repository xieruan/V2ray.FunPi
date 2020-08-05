# encoding: utf-8
"""
File:       node_manager
Author:     twotrees.us@gmail.com
Date:       2020年7月29日  31周星期三 21:57
Desc:
"""

from typing import List
import json
import requests
import base64
import os
from tcp_latency import measure_latency
from concurrent import futures
from .keys import Keyword as K
from .node_item import NodeItem

class NodeManager:
    def __init__(self):
        self.nodes: List[NodeItem]= []
        self.file = 'config/nodes.json'

    def load(self):
        if os.path.isfile(self.file):
            with open(self.file) as f:
                list = json.load(f)
                for data in list:
                    node = NodeItem()
                    node.update(data)
                    self.nodes.append(node)

    def list(self):
        list = []
        for node in self.nodes:
            data = node.dump()
            list.append(data)

        return list

    def save(self):
        list = []
        for node in self.nodes:
            data = node.dump()
            list.append(data)

        with open(self.file, 'w+') as f:
            json.dump(list, f, indent=4)

    def update(self, url):
        new_nodes = []
        r = requests.get(url)
        list = r.text
        list = base64.b64decode(list).decode('utf8')
        for line in list.splitlines():

            if line.startswith(K.vmess_scheme):
                line = line[len(K.vmess_scheme):]
                line = base64.b64decode(line).decode('utf8')
                data = json.loads(line)
                node = NodeItem()
                node.update(data)
                new_nodes.append(node)

        self.nodes = new_nodes
        self.save()

    def delete_node(self, index):
        self.nodes.pop(index)
        self.save()

    def ping_test_all(self) -> dict :
        results = { node.add : -1 for node in self.nodes }

        def ping(host, port):
            delay = measure_latency(host, port, 1)[0]
            return delay

        with futures.ThreadPoolExecutor(max_workers=len(self.nodes)) as executor:
            futures_to_hosts = {}
            for node in self.nodes:
                future = executor.submit(ping, node.add, node.port)
                futures_to_hosts[future] = node.add
            futures.wait(futures_to_hosts.keys())

            for future in futures_to_hosts.keys():
                delay = future.result()
                if delay != None:
                    results[futures_to_hosts[future]] = int(delay)

        return results