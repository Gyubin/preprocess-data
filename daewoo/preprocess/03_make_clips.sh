DATASET_ROOT="/home/gyubin/Documents/korea_dsba/daewoo/dataset"
FRAME_NUM=16
FRAME_INTERVAL=2.0


# Weather
python ClipMaker.py --data_name="weather"\
                    --source_image_path="/hdd1/daewoo/weather/resized"\
                    --dest_clip_path="$DATASET_ROOT/weather/clips_${FRAME_NUM}"\
                    --image_label_path="$DATASET_ROOT/weather/labels/image_label_matching.csv"\
                    --clip_label_path="$DATASET_ROOT/weather/labels/clip${FRAME_NUM}_label.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}

# Hyundai
python ClipMaker.py --data_name="hyundai"\
                    --source_image_path="/hdd1/daewoo/hyundai/resized"\
                    --dest_clip_path="$DATASET_ROOT/hyundai/clips_${FRAME_NUM}"\
                    --image_label_path="$DATASET_ROOT/hyundai/labels/image_matching_waveparam_2min.csv"\
                    --clip_label_path="$DATASET_ROOT/hyundai/labels/clip${FRAME_NUM}_label.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}

# LNGC
python ClipMaker.py --data_name="lngc"\
                    --source_image_path="/hdd1/daewoo/lngc/resized/cam1"\
                    --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam1"\
                    --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam1.csv"\
                    --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam1.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}
python ClipMaker.py --data_name="lngc"\
                    --source_image_path="/hdd1/daewoo/lngc/resized/cam2"\
                    --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam2"\
                    --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam2.csv"\
                    --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam2.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}
python ClipMaker.py --data_name="lngc"\
                    --source_image_path="/hdd1/daewoo/lngc/resized/cam3"\
                    --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam3"\
                    --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam3.csv"\
                    --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam3.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}
python ClipMaker.py --data_name="lngc"\
                    --source_image_path="/hdd1/daewoo/lngc/resized/cam4"\
                    --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam4"\
                    --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam4.csv"\
                    --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam4.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}
python ClipMaker.py --data_name="lngc"\
                    --source_image_path="/hdd1/daewoo/lngc/resized/cam5"\
                    --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam5"\
                    --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam5.csv"\
                    --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam5.csv"\
                    --frame_num=${FRAME_NUM}\
                    --frame_interval=${FRAME_INTERVAL}
