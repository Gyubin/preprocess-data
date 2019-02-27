import os
import argparse
import numpy as np


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


def get_mean_std_image(paths):
    if not os.path.exists(paths['dest_image_path']):
        os.mkdir(paths['dest_image_path'])
        
    mean_x = np.zeros((224, 224, 3))
    mean_xs = np.zeros((224, 224, 3))
    image_file_names = os.listdir(paths['source_image_path'])
    for idx, ifn in enumerate(image_file_names):
        temp = np.load(os.path.join(paths['source_image_path'], ifn))
        temp = temp.astype(float)
        mean_x += temp
        mean_xs += np.square(temp)
        if idx % 1000 == 0:
            print('{}\tof\t{} done.'.format(idx, len(image_file_names)))
    mean_x /= len(image_file_names)
    mean_xs /= len(image_file_names)
    std_x = mean_xs - np.square(mean_x)
    
    mean_x_name = os.path.join(paths['dest_image_path'], paths['mean_image_name'])
    std_x_name = os.path.join(paths['dest_image_path'], paths['std_image_name'])
    np.save(mean_x_name, mean_x)
    np.save(std_x_name, std_x)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get mean image.")
    parser.add_argument("source_image_path", metavar="S", type=str,
                        help="Source image path",
                        default="./data/images_224_resize/", nargs='?')
    parser.add_argument("dest_image_path", metavar="D", type=str,
                        help="Destination image path",
                        default="./data/images_224_mean_std/", nargs='?')
    parser.add_argument("mean_image_name", metavar="M", type=str,
                        help="Mean image name",
                        default="mean_image.npy", nargs='?')
    parser.add_argument("std_image_name", metavar="T", type=str,
                        help="Standard deviation image name",
                        default="std_image.npy", nargs='?')
    
    args = parser.parse_args()
    paths = {
        'source_image_path': args.source_image_path,
        'dest_image_path': args.dest_image_path,
        'mean_image_name': args.mean_image_name,
        'std_image_name': args.std_image_name
    }
    
    get_mean_std_image(paths)
