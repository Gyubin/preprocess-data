# Weather
python ImageResizer.py --data_name="weather"\
                       --source_image_path="/path/to/the/raw_images"\
                       --dest_image_path="/path/to/the/destination"\
                       --crop_coords="350,250,1600,900"

# Hyundai
python ImageResizer.py --data_name="hyundai"\
                       --source_image_path="/path/to/the/raw_images"\
                       --dest_image_path="/path/to/the/destination"\
                       --crop_coords="650,450,1600,750"\
                       --hyundai_label="/path/to/the/hyundai/label"

# LNGC
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="/path/to/the/raw/cam1"\
                       --dest_image_path="/path/to/the/dest/cam1"\
                       --crop_coords="0,400,1000,600"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="/path/to/the/raw/cam2"\
                       --dest_image_path="/path/to/the/dest/cam2"\
                       --crop_coords="0,200,1200,400"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="/path/to/the/raw/cam3"\
                       --dest_image_path="/path/to/the/dest/cam3"\
                       --crop_coords="0,300,1600,550"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="/path/to/the/raw/cam4"\
                       --dest_image_path="/path/to/the/dest/cam4"\
                       --crop_coords="0,400,500,600"
python ImageResizer.py --data_name="lngc"\
                       --source_image_path="/path/to/the/raw/cam5"\
                       --dest_image_path="/path/to/the/dest/cam5"\
                       --crop_coords="0,300,1000,500"
