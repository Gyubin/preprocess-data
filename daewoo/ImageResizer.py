import os
import argparse
import numpy as np
import pandas as pd
from PIL import Image
from multiprocessing import Process


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


class ImageResizer(object):
    """
    카메라로 찍은 원본 사진을 읽어들여서 필요한 부분을 Crop하고
    224x224 사이즈로 리사이즈하여 저장
    """

    def __init__(self, args):
        self.data_name = args.data_name
        self.source_image_path = args.source_image_path
        self.dest_image_path = args.dest_image_path
        self.crop_coords = args.crop_coords
        self.target_size = args.target_size
        self.process_num = args.process_num
        self.enable_grayscale = args.enable_grayscale
        self.hyundai_label = args.hyundai_label

        if self.data_name == 'weather':
            self.image_file_names = sorted(os.listdir(self.source_image_path))
        elif self.data_name == 'hyundai':
            df = pd.read_csv(self.hyundai_label)
            cond1 = df['T.Hs'] == 0  # swh
            cond2 = df['T.Tp'] == 0  # swt
            cond3 = df['T.Dp'] == 0  # dir
            df = df.loc[~(cond1&cond2&cond3), :]
            self.image_file_names = list(df['filename'].values)
        elif self.data_name == 'lngc':
            pass


    @staticmethod
    def get_grayscale(img):
        """
        흑백 이미지로 바꾸는 함수
        """
        return np.dot(img, [0.299, 0.587, 0.114])


    def _resize_func(self, image_file_names):
        """
        실질적으로 이미지 변형 기능을 담당하는 함수로
        프로세스 개수만큼(Logical core) 데이터가 쪼개져서 할당되어
        Load -> Crop -> Resize -> Save 기능 순차적으로 수행
        """
        for idx, ifn in enumerate(image_file_names):
            image = Image.open(os.path.join(self.source_image_path,
                                            image_file_names[idx]))
            image = image.crop(self.crop_coords)
            image = image.resize((self.target_size, self.target_size))
            image = np.array(image)
            if self.enable_grayscale:
                image = image.astype(np.float32)
                image = ImageResizer.get_grayscale(image)
            file_name = os.path.join(self.dest_image_path,
                                     '{}.npy'.format(ifn.split('.')[0]))
            np.save(file_name, image)
            if idx % 1000 == 0:
                print('{}\t{} done.'.format(idx, len(image_file_names)))


    def resize_images(self):
        """
        사용할 수 있는 모든 Logical core를 활용하여
        이미지 transform 진행
        """
        print('Start processing')
        os.makedirs(self.dest_image_path, exist_ok=True)
        alloc_num = len(self.image_file_names) // self.process_num
        my_procs = []
        for i in range(self.process_num):
            start_ind = i * alloc_num
            end_ind = (i+1) * alloc_num
            if i != (self.process_num-1):
                part_of_data = self.image_file_names[start_ind:end_ind]
            else:
                part_of_data = self.image_file_names[start_ind:]

            p = Process(target=self._resize_func, args=(part_of_data,))
            p.start()
            my_procs.append(p)

        for p in my_procs:
            p.join()

        print('Done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images to N by N")
    parser.add_argument("--data_name", type=str, required=True,
                        help="weather or hyundai or lngc")
    parser.add_argument("--source_image_path", type=str, required=True,
                        help="Source image path")
    parser.add_argument("--dest_image_path", type=str, required=True,
                        help="Destination image path")
    parser.add_argument("--crop_coords", type=str, required=True,
                        help="(X_start,Y_start,X_end,Y_end)")
    parser.add_argument("--target_size", type=int,
                        help="Target size, (N, N, 3)", default=224)
    parser.add_argument("--process_num", type=int,
                        help="Number of process to use", default=16)
    parser.add_argument("--enable_grayscale", type=bool, default=False)
    parser.add_argument("--hyundai_label", type=str, help="hyundai label")

    args = parser.parse_args()
    args.crop_coords = tuple(map(int, args.crop_coords.split(',')))
    print(f'====================\nPassed arguments\n====================')
    print(f'{args}\n')

    ir = ImageResizer(args)
    ir.resize_images()
