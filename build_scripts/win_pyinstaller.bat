rem open and save this bat with encoding GB2312, and line breaker CRLF instead of LF

pyinstaller -F -c ^
            --specpath .\ ^
            -n 浦东公租房多人通勤分析 ^
            -i ..\ico\pixel_house.ico ^
            ..\transport_analyse.py