# coding: utf-8

import yaml
# from .display import *


def load_config(file):
    with open(file) as fp:
        conf = yaml.safe_load(fp)
    return conf


class Config:

    def __init__(self, config):
        self._cf = config if isinstance(config, dict) else load_config(config)
        self._retrieve(self._cf)

    def _retrieve(self, cf):
        for key, val in cf.items():
            if isinstance(val, dict):
                val = Config(val)
            self.set(key, val)

    def set(self, key, value):
        self.__setattr__(key, value)

    def dump(self, file_name):
        with open(file_name ,"w") as fp:
            yaml.safe_dump(self._cf, fp)
        info("save config file as", file_name)
