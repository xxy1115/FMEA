# -*- coding: UTF-8 -*-
import hashlib


def get_md5(psw):
    """
    :param psd: 原始密码
    :return: 加密后
    """
    md5 = hashlib.md5()  # 实例化一个md5对象
    md5.update(psw.encode("utf-8"))  # 调用加密方法直接加密
    return md5.hexdigest()
