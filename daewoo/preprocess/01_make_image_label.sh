# Weather
python LabelMaker.py --data_name="weather"\
                     --source_dir="/hdd1/daewoo/weather/raw_images"\
                     --image_label_path="./labels/image_label_weather.csv"\
                     --rough_label_path="./labels/rough/weather_rough_label.csv"\
                     --label_range=150.0

# Hyundai
python LabelMaker.py --data_name="hyundai"\
                     --source_dir="/hdd1/daewoo/hyundai/raw_images"\
                     --image_label_path="./labels/image_label_hyundai.csv"\
                     --rough_label_path="./labels/rough/hyundai_rough_label.csv"\
                     --label_range=120.0

# LNGC
for CAMERA_NUM in 1 2 3 4 5
do
    python LabelMaker.py --data_name='lngc'\
                         --source_dir="/hdd1/daewoo/lngc/raw_images/cam${CAMERA_NUM}"\
                         --image_label_path="./labels/image_label_lngc_cam${CAMERA_NUM}.csv"\
                         --rough_label_path="./labels/rough/lngc_rough_labels"\
                         --label_range=25.0
done

# VLCC
for CAM in "PORT-BD-B9" "PORT-NaviD-B7" "STBD-BD-B10" "STBD-NaviD-B4"
do
    python LabelMaker.py --data_name='vlcc'\
                         --source_dir="/hdd1/daewoo/vlcc/raw_images/${CAM}"\
                         --image_label_path="/home/gyubin/Documents/korea_dsba/daewoo/dataset/vlcc/labels/image_label_vlcc_${CAM}.csv"\
                         --rough_label_path="/home/gyubin/Documents/korea_dsba/daewoo/dataset/vlcc/labels/WaveParam_2019_VLCC_custom.csv"\
                         --label_range=30.0
done
