pyinstaller -F -c \
    --specpath ./ \
    -n 浦东公租房多人通勤分析 \
    -i ../ico/pixel_house.ico \
    ../transport_analyse.py
