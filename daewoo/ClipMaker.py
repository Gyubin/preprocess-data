import os
import argparse
import numpy as np
from datetime import datetime


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


class ClipMaker(object):
    """
    시간, Label 두 가지 기준으로 연속되는 이미지들을 가지고
    Non overlapped 16장을 Video clip으로 만들어 저장
    """

    def __init__(self, args):
        self.source_image_path = args.source_image_path
        self.dest_clip_path = args.dest_clip_path
        self.image_label_path = args.image_label_path
        self.clip_label_path = args.clip_label_path
        self.frame_num = args.frame_num
        self.frame_interval = args.frame_interval

    @staticmethod
    def get_timestamp(d):
        """
        파일명을 입력으로 받아서 시간 정보(초 단위)를 리턴하는 함수
        ex) '20190424133050_13.jpg'
        """
        underpoint = float(d.split('.')[0].split('_')[1])
        d_obj = datetime.strptime(d.split('_')[0], '%Y%m%d%H%M%S')
        return d_obj.timestamp() + underpoint/100

    def save_clips(self, image_file_names, line, clip_num):
        """
        """
        end_idx = 16 * (len(image_file_names) // 16)
        image_file_names = image_file_names[:end_idx]

        f = open(self.clip_label_path, 'a')
        clip = None
        for idx_ifn, ifn in enumerate(image_file_names):
            image = np.load(os.path.join(self.source_image_path, ifn))
            image = np.expand_dims(image, axis=0)
            if idx_ifn % 16 == 0:
                clip = image
                sub_ifn = [ifn.replace('npy', 'jpg')]
            else:
                clip = np.vstack((clip, image))
                sub_ifn.append(ifn.replace('npy', 'jpg'))
                if idx_ifn % 16 == 15:
                    clip_name = os.path.join(self.dest_clip_path,
                                             'clip_{}.npy'.format(clip_num))
                    np.save(clip_name, clip)
                    f.write(f"{clip_num},{line},{','.join(sub_ifn)}\n")
                    if clip_num % 100 == 0:
                        print('clip_{}.npy is saved.'.format(clip_num))
                    clip_num += 1
        f.close()
        return clip_num

    def make_clips(self):
        """
        """
        os.makedirs(self.dest_clip_path, exist_ok=True)

        with open(self.image_label_path, 'r') as f:
            match_data = f.readlines()[1:]
        with open(self.clip_label_path, 'w') as f:
            f.write('clip,swh,swt,dir8,dir16,dir36,dir,i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15\n')

        prev_timestamp = datetime(2018, 11, 6, 11, 10, 22).timestamp()
        prev_swh = -999
        prev_swt = -999
        prev_d8 = 'xxx'
        prev_d16 = 'xxx'
        prev_d36 = 'xxx'
        prev_dir = -999

        clip_num = 0
        subgroup = []
        for idx_md, md in enumerate(match_data):
            fn, cur_swh, cur_swt, cur_d8, cur_d16, cur_d36, cur_dir = md.strip().split(',')
            fn = fn.replace('jpg', 'npy')
            cur_swh = float(cur_swh)
            cur_swt = float(cur_swt)
            cur_d36 = int(float(cur_d36))
            cur_dir = float(cur_dir)
            cur_timestamp = ClipMaker.get_timestamp(fn)

            if cur_timestamp-prev_timestamp < self.frame_interval\
            and cur_swh == prev_swh:
                subgroup.append(fn)
            else:
                if len(subgroup) >= self.frame_num:
                    line = f'{prev_swh},{prev_swt},{prev_d8},{prev_d16},{prev_d36},{prev_dir}'
                    clip_num = self.save_clips(subgroup, line, clip_num)
                subgroup = [fn]

            prev_swh = cur_swh
            prev_swt = cur_swt
            prev_d8 = cur_d8
            prev_d16 = cur_d16
            prev_d36 = cur_d36
            prev_dir = cur_dir
            prev_timestamp = cur_timestamp
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make clips")
    parser.add_argument("--source_image_path", type=str, required=True,
                        help="Source image path")
    parser.add_argument("--dest_clip_path", type=str, required=True,
                        help="Destination clip path")
    parser.add_argument("--image_label_path", type=str, required=True,
                        help="Image label path")
    parser.add_argument("--clip_label_path", type=str, required=True,
                        help="Clip label path")
    parser.add_argument("--frame_num", type=int, help="Number of frames",
                        default=16)
    parser.add_argument("--frame_interval", type=float,
                        help="Interval of frame", default=2.0)

    args = parser.parse_args()
    print(f'====================\nPassed arguments\n====================')
    print(f'{args}\n')

    cm = ClipMaker(args)
    cm.make_clips()
