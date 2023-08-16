# 鱼子酱部署指南(windows系统):

本项目需要使用[mirai](https://github.com/mamoe/mirai)和[mirai-api-http](https://github.com/project-mirai/mirai-api-http),如果你不知道mirai是什么,请停止部署

1. 成功运行mirai并且安装好mirai-api-http插件

2. 修改mirai所在文件夹的\config\net.mamoe.mirai-api-http\setting.yml为以下内容并保存(verifyKey和port可自行修改)

    ```
    adapters:
    - ws
    debug: false
    enableVerify: true
    verifyKey: QQWWEERRTTYY
    singleMode: false
    cacheSize: 4096
    adapterSettings:
    ws:
        host: localhost
        port: 8081
        reservedSyncId: -1
    ```
3. 安装python环境(请安装python3.8.3或之后的版本)

4. 安装[YiriMirai](https://github.com/YiriMiraiProject/YiriMirai)库

        从 PyPI 安装：pip install yiri-mirai
5. 使用文本编辑器打开yiri文件夹的main.py,修改bot_qq和admin,保存文件

6. 在yiri文件夹打开命令窗口,键入python main.py然后enter.如果不出意外,会出现很多No module named 'xxx',这是因为python缺少这些库,请自行百度解决.(才不是我懒得写requirements.txt)

