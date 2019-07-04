# Weather
python ImageResizer.py --data_name="weather"\
                       --source_image_path="/hdd1/daewoo/weather/raw_images"\
                       --dest_image_path="/hdd1/daewoo/weather/resized"\
                       --crop_coords="350,250,1600,900"

# Hyundai
python ImageResizer.py --data_name="hyundai"\
                       --source_image_path="/hdd1/daewoo/hyundai/raw_images"\
                       --dest_image_path="/hdd1/daewoo/hyundai/resized"\
                       --crop_coords="650,450,1600,750"\
                       --hyundai_label="/home/gyubin/Documents/korea_dsba/daewoo/dataset/hyundai/labels/image_matching_waveparam_2min.csv"

# LNGC
LNGC_SRC="/hdd1/daewoo/lngc/raw_images"
LNGC_DEST="/hdd1/daewoo/lngc/resized"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="$LNGC_SRC/cam1"\
                       --dest_image_path="$LNGC_DEST/cam1"\
                       --crop_coords="0,400,1000,600"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="$LNGC_SRC/cam2"\
                       --dest_image_path="$LNGC_DEST/cam2"\
                       --crop_coords="0,200,1200,400"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="$LNGC_SRC/cam3"\
                       --dest_image_path="$LNGC_DEST/cam3"\
                       --crop_coords="0,300,1600,550"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="$LNGC_SRC/cam4"\
                       --dest_image_path="$LNGC_DEST/cam4"\
                       --crop_coords="0,400,500,600"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="$LNGC_SRC/cam5"\
                       --dest_image_path="$LNGC_DEST/cam5"\
                       --crop_coords="0,300,1000,500"
