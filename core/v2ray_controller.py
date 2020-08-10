# encoding: utf-8
"""
File:       v2ray_controller
Author:     twotrees.us@gmail.com
Date:       2020年7月30日  31周星期四 10:53
Desc:
"""
import textwrap
import subprocess
import requests
from .node_item import NodeItem
from . import v2ray_config_generator

class V2rayController:
    def start(self) -> bool:
        cmd = "systemctl start v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return self.running()

    def stop(self) -> bool:
        cmd = "systemctl stop v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return not self.running()

    def restart(self) -> bool:
        cmd = "systemctl restart v2ray.service"
        subprocess.check_output(cmd, shell=True).decode('utf-8')
        return self.running()

    def running(self) -> bool:
        cmd = """ps -ef | grep "v2ray" | grep -v grep | awk '{print $2}'"""
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if output == "":
            return False
        else:
            return True

    def version(self) -> str:
        v2ray_path = '/usr/bin/v2ray/v2ray'
        cmd_get_current_ver = """echo `{0} -version 2>/dev/null` | head -n 1 | cut -d " " -f2""".format(v2ray_path)
        current_ver = 'v' + subprocess.check_output(cmd_get_current_ver, shell=True).decode('utf-8').replace('\n', '')

        return current_ver

    def check_new_version(self) -> str:
        r = requests.get('https://api.github.com/repos/v2fly/v2ray-core/releases/latest')
        r = r.json()
        version = r['tag_name']
        return version

    def update(self) -> bool:
        r = requests.get('https://api.github.com/repos/v2ray/v2ray-core/releases/latest')
        r = r.json()
        version = r['tag_name']

        update_log = subprocess.check_output("bash ./script/update_v2ray.sh {0}".format(version), shell=True).decode('utf-8')
        ret = update_log.find('installed')
        if ret:
            ret = self.restart()

        return ret

    def access_log(self) -> str:
        with open('/var/log/v2ray/access.log') as f:
            lines = f.read().split("\n")
            return self.wrap_last_lines(lines)

    def error_log(self) -> str:
        with open('/var/log/v2ray/error.log') as f:
            lines = f.read().split("\n")
            return self.wrap_last_lines(lines)

    def wrap_last_lines(self, lines: list) -> str:
        count = min(10, len(lines))
        lines = lines[-count:]
        string = ""

        wrapper = textwrap.TextWrapper(width=100)
        for line in lines:
            wrap_list = wrapper.wrap(line)
            for wrap in wrap_list:
                string += wrap + '<br>'
        return string

    def apply_node(self, node: NodeItem, all_nodes:list, mode: int) -> bool:
        config = v2ray_config_generator.gen_config(node, all_nodes, mode)
        return self.apply_config(config)

    def apply_config(self, config: str) -> bool:
        with open('/etc/v2ray/config.json', 'w+') as f:
            f.write(config)

        return self.restart()