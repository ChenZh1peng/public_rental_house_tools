# 公租房信息工具箱

## 目前已接入的公租房列表

- 上海
  - 浦东区筹公租房

## 目前具有功能

1. 多人(多目的地）通勤时间计算/上限筛选（暂时只支持查询公交/地铁时间）
2. 关注特定房源，每日报告或推送消息到微信提醒

## 使用指南

### 可执行文件直接使用

在Release板块下载对应系统版本的压缩包，解压后有两个exe文件和一个config.toml配置文件。将exe文件和config.toml放在同一文件夹下（建议新建一个文件夹放置，因为运行时会生成结果和数据文件夹在同级目录）

1. 通勤时间计算

    &ensp;&ensp;&ensp;&ensp;主要用于按多目的地通勤时间快速筛选合适的房源。

    &ensp;&ensp;&ensp;&ensp;先按下文中高德key申请方式说明申请一个key，填入cofnig.toml文件中[amap]部分的key值内容中，然后将[transport]部分的其他设置按文件内对应的说明要求设置好。

    &ensp;&ensp;&ensp;&ensp;直接双击运行即可，如想按其他方式运行，可以更改设置后重新运行。

    &ensp;&ensp;&ensp;&ensp;结果将保存于result文件夹下，data文件夹内为缓存数据。

2. 小区房源订阅

    &ensp;&ensp;&ensp;&ensp;如需自动推送提醒消息到微信，请先按下文中WxPusher注册方式说明完成注册，并获取对应的token和uid，填入config.toml中[wx_pusher]部分。

    &ensp;&ensp;&ensp;&ensp;在[subscription]部分按文件内说明设置运行模式

    &ensp;&ensp;&ensp;&ensp;在[subscription.pudong]部分按说明填写关注的房源列表。房源名称可使用通勤时间计算功能导出的excel表第一列的小区名字，也可更精简为某条路名，某小区名关键词等。

    &ensp;&ensp;&ensp;&ensp;双击运行exe文件，会将今日可选的房源中你关注所有小区相关的房源结果，按你设置的模式保存到本地excel表或推送微信。

    &ensp;&ensp;&ensp;&ensp;推送到微信功能建议结合操作系统的定时自动运行或开机自动运行程序功能使用，实现每日自动提醒。

### 源码执行

1. 安装Python环境，Python环境版本： >= 3.11， 下载地址：<https://www.python.org/downloads/>， 安装教程：<https://liaoxuefeng.com/books/python/install/>

2. 下载源码后，安装外部依赖。以windows为例，打开cmd命令提示符后，进入源码目录中：

    例：源码目录为 C:\Users\peyton\Desktop\public_rental_house_tools

        cd C:\Users\peyton\Desktop\public_rental_house_tools
        pip install -r requirements.txt

        等待安装成功即可

3. 参照上文可执行文件运行方式，设置好config.toml后，在cmd中运行以下命令运行程序：

        进入文件夹（路径改成自己的）：
        cd C:\Users\peyton\Desktop\public_rental_house_tools
        通勤计算工具：
        python transport_analyse.py
        订阅工具：
        python project_subscription.py

## 第三方平台注册说明

## 高德地图

1. 先注册高德开发者账号，完成个人开发者认证，获取Web服务key（一串32位的数字字母）

   - 高德开放平台：<https://lbs.amap.com/>
   - 认证地址：<https://console.amap.com/dev/user/permission>
   - 应用创建地址：<https://console.amap.com/dev/key/app>

       填写任意名称和类型，完成应用创建后，添加一个key，类型选择Web服务

  ![](/pics/amap.png)

  **高德API有每日次数限制，如果当日使用次数过多，程序报错，将无法继续使用，请第二天再使用**

2. 将生成的多位数字字母key复制，替换配置文件config.toml中 [amap] 板块key后引号内的内容

## WxPusher

这是一个消息推送公众号，用于将消息推送到特定人的微信上

1. 参照链接<https://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8>，注册一个应用，在后台<https://wxpusher.zjiecode.com/admin/>中获取token。

2. 让需要收到消息的人扫码关注公众号后，在程序后台可以查询到所有关注了的用户的uid。

  ![](/pics/wxpusher.png)


3. 将token和uid按要求填入config.toml文件中[wx_pusher]部分

## 源码打包成可执行文件

    cd build_scripts
    
    macos或linux系统，运行linux_mac开头的几个脚本文件即可，几个文件分别对应打包所有工具或打包某一个工具:
    ./linux_mac_all.sh
    同理，windows系统，运行win开头的几个脚本
    .\win_all.bat

    打包好的可执行文件在build_scripts/dist文件夹下

**如需使用upx对可执行文件压缩体积，可按build_scripts/upx/README.md文件的说明下载upx文件并修改对应脚本参数**

## 祝早日住上心仪的房子！