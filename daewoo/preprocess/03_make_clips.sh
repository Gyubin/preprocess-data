DATASET_ROOT="/home/gyubin/Documents/korea_dsba/daewoo/dataset"
FRAME_NUM=4
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
for CAMERA_NUM in 1 2 3 4 5
do
    python ClipMaker.py --data_name="lngc"\
                        --source_image_path="/hdd1/daewoo/lngc/resized/cam${CAMERA_NUM}"\
                        --dest_clip_path="$DATASET_ROOT/lngc/clips_${FRAME_NUM}/cam${CAMERA_NUM}"\
                        --image_label_path="$DATASET_ROOT/lngc/labels/image_label_cam${CAMERA_NUM}.csv"\
                        --clip_label_path="$DATASET_ROOT/lngc/labels/clip${FRAME_NUM}_label_cam${CAMERA_NUM}.csv"\
                        --frame_num=${FRAME_NUM}\
                        --frame_interval=${FRAME_INTERVAL}
done

# VLCC
for CAM in "PORT-BD-B9" "PORT-NaviD-B7" "STBD-BD-B10" "STBD-NaviD-B4"
do
    python ClipMaker.py --data_name="vlcc"\
                        --source_image_path="/hdd1/daewoo/vlcc/resized/${CAM}"\
                        --dest_clip_path="$DATASET_ROOT/vlcc/clips_${FRAME_NUM}/${CAM}"\
                        --image_label_path="$DATASET_ROOT/vlcc/labels/image_label_vlcc_${CAM}.csv"\
                        --clip_label_path="$DATASET_ROOT/vlcc/labels/clip${FRAME_NUM}_label_vlcc_${CAM}.csv"\
                        --frame_num=${FRAME_NUM}\
                        --frame_interval=${FRAME_INTERVAL}
done
