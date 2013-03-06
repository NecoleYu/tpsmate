##可执行文件##

* tpsmate //linux 可执行文件(archlinux 64bit)
* tpsmate.exe //windows 可执行文件(windows 7)
* mac 下可执行文件暂缺

##命令行##
Mac和大部分的*nix发行版默认安装python，在使用前确认安装版本最低要求为2.6。

1. 进入src目录;
- 执行```pip install -r requirements.txt``` 安装依赖模块;
- 如果你使用的版本为2.6，需要安装argparse，执行 ```pip install argparse```;
- 执行```python cli.py```等同运行可执行文件。
