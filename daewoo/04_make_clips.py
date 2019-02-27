import os
import argparse
import numpy as np
from datetime import datetime


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


def get_timestamp(d):
    underpoint = float(d.split('.')[0].split('_')[1])
    date = d.split('.')[0].split('_')[0]
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hour = int(date[8:10])
    minutes = int(date[10:12])
    sec = int(date[12:14])
    d_str = '{} {} {} {} {} {}'.format(year, month, day, hour, minutes, sec)
    d_obj = datetime.strptime(d_str, '%Y %m %d %H %M %S')
    return d_obj.timestamp() + underpoint/100


def make_clip(image_file_names, paths, line, clip_num, frame_num=16):
    end_idx = 16 * (len(image_file_names) // 16)
    image_file_names = image_file_names[:end_idx]
    
    f = open(paths['clip_label_path'], 'a')
    clip = None
    for idx_ifn, ifn in enumerate(image_file_names):
        image = np.load(os.path.join(paths['source_image_path'], ifn))
        image = np.expand_dims(image, axis=0)
        if idx_ifn % 16 == 0:
            clip = image
        else:
            clip = np.vstack((clip, image))
            if idx_ifn % 16 == 15:
                clip_name = os.path.join(paths['dest_clip_path'],
                                         'clip_{}.npy'.format(clip_num))
                np.save(clip_name, clip)
                f.write('{},{}'.format(clip_num, line))
                if clip_num % 100 == 0:
                    print('clip_{}.npy is saved.'.format(clip_num))
                clip_num += 1
    f.close()
    return clip_num


def make_clips(paths, frame_num):
    if not os.path.exists(paths['dest_clip_path']):
        os.mkdir(paths['dest_clip_path'])
        
    with open(paths['meta_data_path']) as f:
        match_data = f.readlines()[1:]
    with open(paths['clip_label_path'], 'w') as f:
        f.write('clip,swh,swt,dir8,dir16\n')
        
    prev_timestamp = datetime(2018, 11, 6, 11, 10, 22).timestamp()
    prev_swh = -999
    prev_swt = -999
    prev_d8 = 'xxx'
    prev_d16 = 'xxx'

    clip_num = 0
    subgroup = []
    for idx_md, md in enumerate(match_data):
        fn, cur_swh, cur_swt, cur_d8, cur_d16 = md.strip().split(',')
        fn = fn.replace('jpg', 'npy')
        cur_swh = float(cur_swh)
        cur_swt = float(cur_swt)
        cur_timestamp = get_timestamp(fn)

        if cur_timestamp - prev_timestamp < 1.1 and cur_swh == prev_swh:
            subgroup.append(fn)
        else:
            if len(subgroup) >= frame_num:
                line = '{},{},{},{}\n'.format(prev_swh, prev_swt, prev_d8, prev_d16)
                clip_num = make_clip(subgroup, paths, line, clip_num=clip_num, frame_num=frame_num)
            subgroup = [fn]

        prev_swh = cur_swh
        prev_swt = cur_swt
        prev_d8 = cur_d8
        prev_d16 = cur_d16
        prev_timestamp = cur_timestamp
    return
        

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Make clips")
    parser.add_argument("source_image_path", metavar="S", type=str,
                        help="Source image path",
                        default="./data/images_224_standardized/", nargs='?')
    parser.add_argument("dest_clip_path", metavar="D", type=str,
                        help="Destination clip path",
                        default="./data/clips/", nargs='?')
    parser.add_argument("meta_data_path", metavar="M", type=str,
                        help="Meta data path",
                        default="./data/image_label_matching.csv", nargs='?')
    parser.add_argument("clip_label_path", metavar="L", type=str,
                        help="Label path",
                        default="./data/clip_labels.csv", nargs='?')
    parser.add_argument("frame_num", metavar="F", type=int,
                        help="Sequence number of frames",
                        default=16, nargs='?')
    
    args = parser.parse_args()
    paths = {
        'source_image_path': args.source_image_path,
        'dest_clip_path': args.dest_clip_path,
        'meta_data_path': args.meta_data_path,
        'clip_label_path': args.clip_label_path
    }
    frame_num = args.frame_num
    
    make_clips(paths, frame_num)
