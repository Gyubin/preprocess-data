import os
import argparse
import numpy as np
from PIL import Image
from multiprocessing import Process


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


def get_grayscale(img):
    return np.dot(img, [0.299, 0.587, 0.114])


def resize_images(image_file_names, paths, coord, target_size):
    for idx, ifn in enumerate(image_file_names):
        image = Image.open(os.path.join(paths['source_image_path'],
                                        image_file_names[idx]))
        image = image.crop((coord['crop_width'], coord['crop_height'],
                            coord['total_width'], coord['total_height']))
        image = image.resize((target_size, target_size))
        image = np.array(image)
        image = image.astype(np.float32)
        image = get_grayscale(image)
        image /= 255
        file_name = os.path.join(paths['dest_image_path'],
                                 '{}.npy'.format(ifn.split('.')[0]))
        np.save(file_name, image)
        if idx % 1000 == 0:
            print('{}\t{} done.'.format(idx, len(image_file_names)))


def resize_images_multiprocess(paths, coord, target_size, process_num=8):
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

        p = Process(target=resize_images,
                    args=(part_of_data, paths, coord, target_size))
        p.start()
        my_procs.append(p)

    for p in my_procs:
        p.join()

    print('Done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images to N by N")
    parser.add_argument("source_image_path", metavar="S", type=str,
                        help="Source image path",
                        default="./data/images", nargs='?')
    parser.add_argument("dest_image_path", metavar="D", type=str,
                        help="Destination image path",
                        default="./data/images_112_resize_gray/", nargs='?')
    parser.add_argument("crop_width", metavar="w", type=int,
                        help="Crop width",
                        default=350, nargs='?')
    parser.add_argument("crop_height", metavar="h", type=int,
                        help="Crop height",
                        default=250, nargs='?')
    parser.add_argument("total_width", metavar="W", type=int,
                        help="Total width",
                        default=1600, nargs='?')
    parser.add_argument("total_height", metavar="H", type=int,
                        help="Total height",
                        default=900, nargs='?')
    parser.add_argument("target_size", metavar="N", type=int,
                        help="Target size, (N, N, 3)",
                        default=112, nargs='?')
    parser.add_argument("process_num", metavar="P", type=int,
                        help="Number of process to use",
                        default=8, nargs='?')
    
    args = parser.parse_args()
    paths = {
        'source_image_path': args.source_image_path,
        'dest_image_path': args.dest_image_path
    }
    coord = {
        'crop_width': args.crop_width,
        'crop_height': args.crop_height,
        'total_width': args.total_width,
        'total_height': args.total_height
    }
    target_size = args.target_size
    process_num = args.process_num
    
    resize_images_multiprocess(paths, coord, target_size, process_num)
