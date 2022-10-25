# -*- coding: UTF-8 -*-
import pytest


@pytest.fixture(scope="session", autouse=True)
def start_running():
    print("执行开始")
    yield
    print("执行完成")
