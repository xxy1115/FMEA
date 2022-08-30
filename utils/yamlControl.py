# -*- coding: UTF-8 -*-
import yaml


def parse_yaml(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data
