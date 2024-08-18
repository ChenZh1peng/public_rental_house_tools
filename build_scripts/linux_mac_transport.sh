# if compressing by upx is required, put upx binary under [upx] folder, then add this argument line to the commands:
# --upx-dir ./upx/[directory path to the upx binary file]
# beware of using line continuation mark \

pyinstaller -F -c \
    --specpath ./ \
    -n 浦东公租房多人通勤分析 \
    -i ../ico/pixel_house.ico \
    ../transport_analyse.py
    
    