#安装指定版本号的包
pip install 包名==版本号
#使用国内镜像源安装
pip install 包名 -i https://mirrors.aliyun.com/pypi/simple --trust-host mirrors.aliyun.com
#import导入模块，不建议一次导入多个
import module1
import module2
from module import fun1,fun2
from module import *
#dir()
print(dir())#当前模块下可用的变量、方法，包括导入进来的
print(dir(sys))
#生成报告
#运行文件保存结果到result目录下
pytest_cases>pytest test_01.py --alluredir ./result -vs
allure serve ./result
#生成报告-指定生成到report文件夹
allure generate ./result -o report