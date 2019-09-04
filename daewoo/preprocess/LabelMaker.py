import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime


class LabelMaker(object):
    """
    레이더를 통해 수집된 시간 단위 raw label을 활용해
    같은 시간 정보인 이미지들 각각에 파고, 파주기, 파향 레이블을 설정한다.
    """
    def __init__(self, opt):
        self.data_name = opt.data_name
        self.source_dir = opt.source_dir
        self.image_label_path = opt.image_label_path
        self.rough_label_path = opt.rough_label_path
        self.label_range = opt.label_range

        if self.data_name == 'weather':
            self.rough_label = pd.read_csv(self.rough_label_path)
            self.rough_label = self.rough_label.loc[:, ['DATE', 'SWH', 'SWT', 'DIR']]
            self.rough_label.columns = ['date', 'swh', 'swt', 'dir']
        elif self.data_name == 'hyundai':
            self.rough_label = pd.read_csv(self.rough_label_path)
            self.rough_label = self.rough_label.loc[:, ['Date&Time', ' T.Hs', ' T.Tp', ' T.Dp']]
            self.rough_label.columns = ['date', 'swh', 'swt', 'dir']
        elif self.data_name == 'lngc':
            label_list = []
            for fn in sorted(os.listdir(self.rough_label_path)):
                tmp = pd.read_csv(os.path.join(self.rough_label_path, fn))
                tmp = tmp.loc[:, ['TimeS', 'W.Hs', 'W.T01', 'W.Dir']]
                tmp.columns = ['date', 'swh', 'swt', 'dir']
                label_list.append(tmp)
            self.rough_label = pd.concat(label_list, ignore_index=True)

    @staticmethod
    def check_time(image_d, label_d, label_range):
        """
        레이더 raw label의 시간 간격이 띄엄 띄엄 있기 때문에
        이미지의 시간 정보가 사전에 설정한 범위 내에 있는지 체크하는 함수
        """
        td = image_d - label_d
        diff = td.total_seconds()
        if -label_range <= diff <= label_range:
            return 0
        elif diff < -label_range:
            return -1
        elif diff > label_range:
            return 1

    def get_datetime(self, d_str, dtype):
        """
        문자열에서 날짜 정보를 추출하는 함수
        """
        assert dtype in ['label', 'file']
        if dtype == 'label':
            if self.data_name == 'weather':
                d_obj = datetime.strptime(d_str, '%Y_%m_%d_%H_%M')
            elif self.data_name == 'hyundai':
                d_obj = datetime.strptime(d_str, '%Y-%m-%d %H:%M:%S')
            elif self.data_name == 'lngc':
                d_obj = datetime.strptime(d_str, '%Y-%m%d-%H%M%S')
        else:
            d_obj = datetime.strptime(d_str[:-7], '%Y%m%d%H%M%S')
        return d_obj

    def image_iterator(self):
        """
        이미지를 정렬해서 순서대로 하나씩 iterate하는 함수
        """
        image_file_names = sorted(os.listdir(self.source_dir))
        for ifn in image_file_names:
            yield ifn

    def label_iterator(self):
        """
        raw label의 각 row를 순서대로 하나씩 iterate하는 함수
        """
        for i in range(len(self.rough_label)):
            yield self.rough_label.loc[i, :]

    def make_label(self):
        """
        이미지 레이블을 만드는 함수
        이미지와, raw label을 하나 하나씩 넘겨가면서
        시간대가 매칭되는 경우 이미지 레이블 파일에 하나씩 기록한다.
        """
        print(f'Making label: {self.image_label_path}')
        f = open(self.image_label_path, 'w')
        f.write('filename,swh,swt,dir\n')
        ifn_iter = self.image_iterator()
        label_iter = self.label_iterator()

        ifn_flag = True
        label_flag = True
        while True:
            try:
                if ifn_flag: ifn = next(ifn_iter)
                if label_flag: lb = next(label_iter)
            except:
                break

            image_d = self.get_datetime(ifn, 'file')
            label_d = self.get_datetime(lb['date'], 'label')
            if LabelMaker.check_time(image_d, label_d, self.label_range) == 0:
                f.write(f'{ifn},{lb["swh"]},{lb["swt"]},{lb["dir"]}\n')
                ifn_flag = True
                label_flag = False
            elif LabelMaker.check_time(image_d, label_d, self.label_range) == -1:
                ifn_flag = True
                label_flag = False
            elif LabelMaker.check_time(image_d, label_d, self.label_range) == 1:
                ifn_flag = False
                label_flag = True
        f.close()
        print('Done')
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Label maker arguments")
    parser.add_argument('--data_name', type=str, help="Data name")
    parser.add_argument('--source_dir', type=str, help='Source image path')
    parser.add_argument('--image_label_path', type=str, help='Output label path')
    parser.add_argument('--rough_label_path', type=str, help='Original rough label')
    parser.add_argument('--label_range', type=float, help='Label time range')
    opt = parser.parse_args()

    label_maker = LabelMaker(opt)
    label_maker.make_label()

