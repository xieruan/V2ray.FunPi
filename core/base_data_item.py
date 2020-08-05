# encoding: utf-8
"""
File:       base_data_item
Author:     twotrees.us@gmail.com
Date:       2020年7月29日  31周星期三 21:45
Desc:
"""
import json

class BaseDataItem:
    def filename(self):
        return ''

    def update(self, data):
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def dump(self):
        return vars(self)

    def load(self):
        with open(self.filename()) as f:
            data = json.load(f)
            self.update(data)

    def save(self):
        data = self.dump()
        with open(self.filename(), 'w+') as f:
            json.dump(data, f, indent=4)