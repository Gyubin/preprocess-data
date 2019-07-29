import os
import yaml
import PIL
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
from utils import stack_images, make_label_custom,
                  make_label_normal, get_timestamp


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


class ClipLoader(object):
    """
    Iterate all possible clips
    """

    def __init__(self, data_name, frame_length):
        with open('./cliploader_opt.yaml', 'r') as f:
            opt = yaml.load(f, yaml.FullLoader)
        self.data_name = data_name
        self.frame_length = frame_length
        self.seed = -1
        self.raw_image_path = opt[data_name]['raw_image_path']
        self.image_label_path = opt[data_name]['image_label_path']
        self.crop_coords = opt[data_name]['crop_coords']
        self.start_timestamp = opt[data_name]['start_timestamp']
        self.use_grayscale = opt['grayscale']['use']
        self.grayscale_coef = np.array(opt['grayscale']['coef'],
                                       dtype=np.float32)
        self.target_shape = (opt['target_size']['width'],
                             opt['target_size']['height'])
        self.frame_interval = opt['target_size']['frame_interval']
        self.split_ratio = {
                'train': opt['split_ratio']['train'],
                'val': opt['split_ratio']['val'],
                'test': opt['split_ratio']['test'],
        }
        if opt['dir_label_method']['type'] == 'custom':
            self.make_dir_label = make_label_custom
            self.dir_label_param = opt['dir_label_method']['custom_window']
        elif opt['dir_label_method']['type'] == 'normal':
            self.make_dir_label = make_label_normal
            self.dir_label_param = opt['dir_label_method']['normal_std']

        self.unloaded_clips = []
        self.clip_label = { 'swh': [], 'swt': [], 'dir': [] }
        self._get_image_file_names_and_label()
        self._get_sub_image_file_names_of_clips()

    def get_grayscale(self, img):
        """
        Transform rgb to gray scale
        """
        return np.dot(img, self.grayscale_coef)

    def _get_image_file_names_and_label(self):
        """
        Get file names of images.
        """
        if self.data_name in ['weather', 'lngc']:
            self.image_file_names = sorted(os.listdir(self.raw_image_path))
            self.image_label = pd.read_csv(self.image_label_path)
        elif self.data_name == 'hyundai':
            image_label = pd.read_csv(self.image_label_path)
            cond1 = image_label['swh'] == 0
            cond2 = image_label['swt'] == 0
            cond3 = image_label['dir'] == 0
            image_label = image_label.loc[~(cond1&cond2&cond3), :]
            self.image_label = image_label.reset_index(drop=True)
            self.image_file_names = list(self.image_label['filename'].values)
        return

    def _add_sub_clips(self, subgroup, swh, swt, swd):
        end_idx = self.frame_length * (len(subgroup) // self.frame_length)
        subgroup = subgroup[:end_idx]
        for i in range(len(subgroup)):
            if i % self.frame_length == 0:
                self.unloaded_clips.append(subgroup[i:i+self.frame_length])
                self.clip_label['swh'].append(swh)
                self.clip_label['swt'].append(swt)
                self.clip_label['dir'].append(swd)
        return

    def _get_sub_image_file_names_of_clips(self):
        print("Making clip file names... ", end='')
        prev_swh = -999
        prev_swt = -999
        prev_dir = -999
        prev_timestamp = datetime(*self.start_timestamp).timestamp()
        subgroup = []
        for i in range(len(self.image_label)):
            fn, cur_swh, cur_swt, cur_dir = self.image_label.iloc[i, :]
            if not os.path.exists(os.path.join(self.raw_image_path, fn)):
                continue
            cur_timestamp = get_timestamp(fn)
            if (cur_timestamp-prev_timestamp < self.frame_interval
                    and cur_swh == prev_swh):
                subgroup.append(fn)
            else:
                if len(subgroup) >= self.frame_length:
                    self._add_sub_clips(subgroup, prev_swh, prev_swt, prev_dir)
                subgroup = [fn]
            prev_swh, prev_swt, prev_dir = cur_swh, cur_swt, cur_dir
            prev_timestamp = cur_timestamp
        self.unloaded_clips = np.array(self.unloaded_clips)
        self.clip_label['swh'] = np.array(self.clip_label['swh'])
        self.clip_label['swt'] = np.array(self.clip_label['swt'])
        self.clip_label['dir'] = np.array(self.clip_label['dir'])
        print('Done.')
        return

    def _crop_and_resize(self, image):
        """
        Crop the images to the given crop coordinates.
        """
        assert type(image) == PIL.JpegImagePlugin.JpegImageFile
        image = image.crop(self.crop_coords)
        image = image.resize((self.target_shape))
        return image

    def _set_seed(self, seed=1):
        if self.seed == seed:
            return
        self.seed = seed
        np.random.seed(self.seed)
        train_end = int(len(self.unloaded_clips) * self.split_ratio['train'])
        val_end = int(len(self.unloaded_clips) * (self.split_ratio['train']
                                         + self.split_ratio['val']))
        total_indices = np.arange(len(self.unloaded_clips))
        np.random.shuffle(total_indices)
        self.indices = {
            'train': total_indices[:train_end],
            'val': total_indices[train_end:val_end],
            'test': total_indices[val_end:]
        }
        return

    def make_clip(self, image_file_names):
        images = []
        for ifn in image_file_names:
            image = Image.open(os.path.join(self.raw_image_path, ifn))
            image = self._crop_and_resize(image)
            image = np.array(image)
            if self.use_grayscale:
                image = self.get_grayscale(image)
            images.append(image)
        clip = stack_images(images)
        return clip

    def get_iterator(self, split_type='train', target_name='swh',
                     batch_size=16, seed=1):
        self._set_seed(seed=seed)
        splited_uc = self.unloaded_clips[self.indices[split_type]]
        splited_target = self.clip_label[target_name][self.indices[split_type]]
        batch_X, batch_y = [], []
        for i, (su, st) in enumerate(zip(splited_uc, splited_target)):
            clip = self.make_clip(su)
            batch_X.append(clip)
            batch_y.append(st)
            if i % batch_size == batch_size-1:
                if target_name == 'dir':
                    batch_y = self.make_dir_label(batch_y, self.dir_label_param)
                else:
                    batch_y = np.array(batch_y)
                yield (stack_images(batch_X), batch_y)
                batch_X, batch_y = [], []


if __name__ == "__main__":
    cl = ClipLoader(data_name='hyundai', frame_length=16)
