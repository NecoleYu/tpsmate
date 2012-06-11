#TPS Mate 使用指南
TPS Mate是TPS系统的命令行/桌面版本。其中命令行版本基于python，当前功能主要包括上传单张图片、批量上传图片以及样式文件中背景图片的批量上传以及输出。其目的主要为减少手工替换以及为可能出现的前端打包工具提供更为有效的支持。

##环境支持以及权限说明

命令行版本支持Linux、Mac、Windows平台，在使用TPS Mate前，请确认已经安装符合对应平台的python发行版本，python的版本要求为2.x(2.6 above)。另外你需要一个有TPS上传权限的账号。

##命令总览
    python tpsmate_cli.py login "username" "password"
    python tpsmate_cli.py login "password"
    python tpsmate_cli.py login

    python tpsmate_cli.py config username "username"
    python tpsmate_cli.py config password "password"
    python tpsmate_cli.py config encoding "utf-8,gbk"
    python tpsmate_cli.py config logdir "/path/to/save/csv/log/"

    python tpsmate_cli.py upload --file "/path/to/image.jpg"
    python tpsmate_cli.py upload --file "/path/to/image.jpg,/path/to/another/image.png"
    python tpsmate_cli.py upload --dir "/path/to/image/directory"
    python tpsmate_cli.py upload --dir "/path/to/image/directory" --logdir "/path/to/save/csv/log/"

    python tpsmate_cli.py sheet --file "/path/to/sheet.css"
    python tpsmate_cli.py sheet --file "/path/to/sheet.css" --logdir "/path/to/save/csv/log/"

    python tpsmate_cli.py logout

##登陆
登陆后，cookie会保存在你的用户目录下，以便进行上传等操作。通常情况下，建议你使用config命令对账户和密码进行配置。config命令的使用可以参考“配置”章节。

如果你已经通过config命令配置过账户和密码，只需要通过以下命令即可登陆：

    python tpsmate_cli.py login
    
如果未做完全配置，即只配置过账户或密码，则会提示你输入相应的值。由于登陆采用交互式登陆，因此在执行涉及上传动作的命令时请确认当前已处于登陆状态，将此集成至打包工具尤为需要注意。

##配置
配置用户名：

    python tpsmate_cli.py config username "username"

配置密码：

    python tpsmate_cli.py config password "password"

配置样式表文件编码解析顺序，默认为utf-8,gbk,big5：

    python tpsmate_cli.py config encoding "utf-8,gbk"
    
配置csv格式的日志文件存储目录，默认情况下为用户目录：

    python tpsmate_cli.py config logdir "/path/to/save/csv/log/"

##上传图片
上传单张图片：

    python tpsmate_cli.py upload --file "/path/to/image.jpg"

上传单张图片且不在终端输出上传信息：

    python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-interactive

上传多张图片：

    python tpsmate_cli.py upload --file "/path/to/image.jpg,/path/to/another/image.png"

上传某目录下的图片：

    python tpsmate_cli.py upload --dir "/path/to/image/directory"

上传图片且将log文件保存到指定目录，如果无此参数，则会保存至config配置的logdir或者默认的用户目录中。通常日志名格式为tpsmate_20120611.csv。

    python tpsmate_cli.py upload --dir "/path/to/image/directory" --logdir "/path/to/save/csv/log/"

##上传样式表中的的背景图片并做替换：

    python tpsmate_cli.py sheet --file "/path/to/sheet.css"

当前只有覆盖原文件一种方式，后续版本会做逐步改进。另外logdir参数与upload命令中的解释保持一致。

##关于
TPS Mate基于TPS的非官方接口，因此任何TPS官方的变动都可能导致TPS Mate短时间内不可用。当前版本未做过严格的测试，如果在使用中发现问题，可以创建ISSUE，我会尽快修复。同时你也可以通过下面的方式联系。

gmail/gtalk: sodabiscuit@gmail.com
AliWangWang:无语
AliMail:wuyu@taobao.com
