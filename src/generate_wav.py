# -*- coding: utf-8 -*-
#########################################################################
# Initial software
# Copyright Nicolas Turpault, Romain Serizel, Justin Salamon, Ankit Parag Shah, 2019, v1.0
# This software is distributed under the terms of the License MIT
#########################################################################
import time
import argparse
import numpy as np
import os
import os.path as osp
import json
import glob
import soundfile as sf
import re
import jams
import csv

from scaper import generate_from_jams
from utils import create_folder, pprint


def generate_files(list_jams, outfolder, fg_path=None, bg_path=None, overwrite_jams=False):
    n = 0
    for jam_file in list_jams:
        audiofile = osp.join(outfolder, f"{osp.splitext(osp.basename(jam_file))[0]}.wav")
        if overwrite_jams:
            jams_outfile = jam_file
        else:
            jams_outfile = None
        generate_from_jams(jam_file, audiofile, fg_path=fg_path, bg_path=bg_path, jams_outfile=jams_outfile)

        n += 1
        if n % 500 == 0:
            print(f"generating {n} / {len(list_jams)} files")
    print("Done")


if __name__ == '__main__':
    t = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite-jams', action="store_true", default=False)
    args = parser.parse_args()
    pprint(vars(args))
    
    # Training
    train_folder = osp.join('..', 'training', 'soundscapes')
    list_jams = glob.glob(osp.join(train_folder, "*.jams"))
    fg_path_train = osp.join("..", "training", "soundbank", "foreground")
    bg_path_train = osp.join("..", "training", "soundbank", "background")
    generate_files(list_jams, train_folder, fg_path=fg_path_train, bg_path=bg_path_train, 
                   overwrite_jams=args.overwrite_jams)
    
    # Eval
    # In the evaluation part, there multiple subsets which allows to check robustness of systems
    eval_folder = osp.join('..', 'eval', 'soundscapes')
    list_folders = [osp.join(eval_folder, dI) for dI in os.listdir(eval_folder) if osp.isdir(osp.join(eval_folder, dI))]
    fg_path_eval = osp.join("..", "eval", "soundbank", "foreground")
    bg_path_eval = osp.join("..", "eval", "soundbank", "background")
    
    for folder in list_folders:
        print(folder)
        list_jams = glob.glob(osp.join(folder, "*.jams"))
        generate_files(list_jams, folder, fg_path=fg_path_eval, bg_path=bg_path_eval, 
                       overwrite_jams=args.overwrite_jams)
