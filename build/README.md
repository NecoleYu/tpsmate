##可执行文件##

* tpsmate //linux 可执行文件(archlinux 64bit)
* tpsmate.exe //windows 可执行文件(windows 7)
* mac 下可执行文件暂缺，参考python环境部分

##python执行环境##
Mac和大部分的*nix发行版默认安装python，在使用前确认安装版本最低要求为2.6，且安装python包管理工具pip。

1. 进入src目录;
- 执行```pip install -r requirements.txt``` 安装依赖模块;
- 如果你使用的版本为2.6，需要安装argparse，执行 ```pip install argparse```;
- 执行```python cli.py```等同运行可执行文件。

##参考文档##
* [pip官方安装指南](http://www.pip-installer.org/en/1.3.X/installing.html)
