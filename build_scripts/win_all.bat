rem open and save this bat with encoding GB2312, and line breaker CRLF instead of LF

rem if compressing by upx is required, put upx binary under [upx] folder, then add this argument line to the commands:
rem --upx-dir .\upx\[directory path to the upx binary file]
rem beware of using line continuation mark ^

pyinstaller -F -c ^
            --specpath .\ ^
            -n �ֶ����ⷿ����ͨ�ڷ��� ^
            -i ..\ico\pixel_house.ico ^
            ..\transport_analyse.py

pyinstaller -F -c ^
            --specpath .\ ^
            -n �ֶ����ⷿС�����Ĺ��� ^
            -i ..\ico\building.ico ^
            ..\project_subscription.py