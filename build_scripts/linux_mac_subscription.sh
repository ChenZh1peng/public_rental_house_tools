# if compressing by upx is required, put upx binary under [upx] folder, then add this argument line to the commands:
# --upx-dir ./upx/[directory path to the upx binary file]
# beware of using line continuation mark \
# 如果需要使用upx压缩，将upx可执行文件放在upx文件夹下，然后把下面这句参数加到每句命令中：
# --upx-dir ./upx/[upx文件的路径]
# 注意正确使用续行符 \
    
pyinstaller -F -c \
    --specpath ./ \
    -n 浦东公租房小区订阅工具 \
    -i ../ico/building.ico \
    ../project_subscription.py
    