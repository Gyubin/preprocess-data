import os
import argparse
import numpy as np
from multiprocessing import Process


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


def standardize_images(image_file_names, paths):
    mean_image = np.load(os.path.join(paths['meta_data_path'],
                                      paths['mean_image_name']))
    std_image = np.load(os.path.join(paths['meta_data_path'],
                                      paths['std_image_name']))
    
    for idx, ifn in enumerate(image_file_names):
        image = np.load(os.path.join(paths['source_image_path'], ifn))
        image = (image - mean_image) / std_image
        image = image.astype(np.float32)
        file_name = os.path.join(paths['dest_image_path'], ifn)
        np.save(file_name, image)
        if idx % 1000 == 0:
            print('{}\t{} done.'.format(idx, len(image_file_names)))


def standardize_images_multiprocess(paths, process_num=8):
    print('Start processing')
    if not os.path.exists(paths['dest_image_path']):
        os.mkdir(paths['dest_image_path'])
    
    image_file_names = sorted(os.listdir(paths['source_image_path']))
    alloc_num = len(image_file_names) // process_num
    
    my_procs = []
    for i in range(process_num):
        start_ind = i * alloc_num
        end_ind = (i+1) * alloc_num
        if i != (process_num-1):
            part_of_data = image_file_names[start_ind:end_ind]
        else:
            part_of_data = image_file_names[start_ind:]

        p = Process(target=standardize_images,
                    args=(part_of_data, paths))
        p.start()
        my_procs.append(p)

    for p in my_procs:
        p.join()

    print('Done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standardize images")
    parser.add_argument("source_image_path", metavar="S", type=str,
                        help="Source image path",
                        default="./data/images_224_resize/", nargs='?')
    parser.add_argument("dest_image_path", metavar="D", type=str,
                        help="Destination image path",
                        default="./data/images_224_standardized/", nargs='?')
    parser.add_argument("meta_data_path", metavar="M", type=str,
                        help="Meta data path",
                        default="./data/images_224_mean_std/", nargs='?')
    parser.add_argument("mean_image_name", metavar="M", type=str,
                        help="Mean image name",
                        default="mean_image.npy", nargs='?')
    parser.add_argument("std_image_name", metavar="T", type=str,
                        help="Standard deviation image name",
                        default="std_image.npy", nargs='?')
    parser.add_argument("process_num", metavar="P", type=int,
                        help="Number of process to use",
                        default=8, nargs='?')
    
    args = parser.parse_args()
    paths = {
        'source_image_path': args.source_image_path,
        'dest_image_path': args.dest_image_path,
        'meta_data_path': args.meta_data_path,
        'mean_image_name': args.mean_image_name,
        'std_image_name': args.std_image_name
    }
    process_num = args.process_num
    
    standardize_images_multiprocess(paths, process_num)
