rem open and save this bat with encoding GB2312, and line breaker CRLF instead of LF

rem if compressing by upx is required, put upx binary under [upx] folder, then add this argument line to the commands:
rem --upx-dir .\upx\[directory path to the upx binary file]
rem beware of using line continuation mark ^
rem 如果需要使用upx压缩，将upx可执行文件放在upx文件夹下，然后把下面这句参数加到每句命令中：
rem --upx-dir --upx-dir .\upx\[upx文件的路径]
rem 注意正确使用续行符 ^

pyinstaller -F -c ^
            --specpath .\ ^
            -n 浦东公租房多人通勤分析 ^
            -i ..\ico\pixel_house.ico ^
            ..\transport_analyse.py