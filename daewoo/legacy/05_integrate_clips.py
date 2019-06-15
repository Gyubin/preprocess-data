import os
import argparse
import numpy as np


__author__ = "Gyubin Son"
__version__ = "1.0"
__maintainer__ = "Gyubin Son"
__email__ = "gyubin_son@korea.ac.kr"
__status__ = "Develop"


def integrate_clips(paths):
    clip_file_names = os.listdir(paths['source_clip_path'])
    clip_file_names = sorted(clip_file_names,
                             key=lambda x: int(x.split('.')[0].split('_')[1]))
    
    result = []
    for i, cfn in enumerate(clip_file_names):
        if i % 2 == 0:
            even = np.load(os.path.join(paths['source_clip_path'],
                                        clip_file_names[i]))
            even = np.expand_dims(even, axis=0)
            if i == len(clip_file_names)-1:
                result.append(even)
                break
            odd = np.load(os.path.join(paths['source_clip_path'],
                                       clip_file_names[i+1]))
            odd = np.expand_dims(odd, axis=0)
            result.append(np.vstack((even, odd)))
            
    while len(result) > 1:
        new_result = []
        for i, el in enumerate(result):
            if i % 2 == 0:
                if i == len(result)-1:
                    new_result.append(result[i])
                else:
                    new_result.append(np.vstack((result[i], result[i+1])))

        del result
        result = new_result
        del new_result
    
    np.save(paths['dest_clip_path'], result[0])
    print('Done')
    return
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make clips")
    parser.add_argument("source_clip_path", metavar="S", type=str,
                        help="Source clip path",
                        default="./data/clips/", nargs='?')
    parser.add_argument("dest_clip_path", metavar="D", type=str,
                        help="Destination clip path",
                        default="./data/total_clips.npy", nargs='?')
    
    args = parser.parse_args()
    paths = {
        'source_clip_path': args.source_clip_path,
        'dest_clip_path': args.dest_clip_path
    }
    
    integrate_clips(paths)
