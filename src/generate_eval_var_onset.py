# -*- coding: utf-8 -*-
#########################################################################
# Initial software
# Copyright Nicolas Turpault, Romain Serizel, Justin Salamon, Ankit Parag Shah, 2019, v1.0
# This software is distributed under the terms of the License MIT
#########################################################################
import time
import argparse
import scaper
import os
import os.path as osp
import glob
import jams
import pandas as pd

from utils import create_folder, pprint, rm_high_polyphony, post_processing_annotations


def modify_fg_onset(added_value, jam_file):
    """ Add a value foreground onset of a JAMS generated by scaper (containing a single event)
    Args:
        added_value: float, value in seconds, value to be added to previous onset
        jam_file: str, the name of the JAMS file to change the background SNR

    Returns:
        jams object that has been modified
    """
    jam_obj = jams.load(jam_file)
    data = jam_obj["annotations"][0].data
    for cnt, obs in enumerate(data):
        if obs.value["role"] == "foreground":
            onset = obs.value["event_time"]
            # Change source time by adding the added value specified
            jam_obj["annotations"][0].data[cnt].value["event_time"] = onset + added_value
            # Todo, this is tricky, because it is an object, find a better way to do that with Scaper
            new_obs = jam_obj["annotations"][0].data[cnt]._replace(time=onset + added_value)
            del jam_obj["annotations"][0].data[cnt]
            jam_obj["annotations"][0].data.add(new_obs)

    return jam_obj


def generate_new_fg_onset_files(added_value, in_dir, out_dir):
    """ Generate the new JAMS and audio files adding a value to forground onsets
    Args:
        added_value: float, value in seconds, value to be added to previous onset
        in_dir: str, folder containing JAMS file with background SNR to be changed
        out_dir: str, folder where to save the new audio and JAMS

    Returns:

    """
    for jam_file in sorted(glob.glob(os.path.join(in_dir, "*.jams"))):
        jams_obj = modify_fg_onset(added_value, jam_file)
        out_jams = osp.join(out_dir, os.path.basename(jam_file))
        jams_obj.save(out_jams)

        audiofile = os.path.join(out_dir, osp.splitext(osp.basename(jam_file))[0] + ".wav")
        print(audiofile)
        scaper.generate_from_jams(out_jams, audiofile)


if __name__ == '__main__':
    t = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--outfolder', type=str, default=osp.join('..', 'eval', 'soundscapes_generated_var_onset'))
    parser.add_argument('--number', type=int, default=1000)
    parser.add_argument('--fgfolder', type=str, default=osp.join("..", "eval", "soundbank", "foreground_on_off"))
    parser.add_argument('--bgfolder', type=str, default=osp.join("..", "eval", "soundbank", "background"))
    args = parser.parse_args()
    pprint(vars(args))

    # General output folder, in args
    out_folder = args.outfolder
    create_folder(out_folder)

    # Default parameters
    n_soundscapes = args.number
    ref_db = -50
    duration = 10.0

    # ################
    # Varying onset of a single event
    # ###########
    # SCAPER SETTINGS
    fg_folder = args.fgfolder
    bg_folder = args.bgfolder

    source_time_dist = 'const'
    source_time = 0.0

    event_duration_dist = 'uniform'
    event_duration_min = 0.25
    event_duration_max = 10.0

    snr_dist = 'uniform'
    snr_min = 6
    snr_max = 30

    pitch_dist = 'uniform'
    pitch_min = -3.0
    pitch_max = 3.0

    time_stretch_dist = 'uniform'
    time_stretch_min = 1
    time_stretch_max = 1

    event_time_dist = 'truncnorm'
    event_time_mean = 0.5
    event_time_std = 0.25
    event_time_min = 0.25
    event_time_max = 0.750

    out_folder_500 = osp.join(out_folder, "500ms")
    create_folder(out_folder_500)
    # Generate 1000 soundscapes using a truncated normal distribution of start times
    for n in range(n_soundscapes):
        print('Generating soundscape: {:d}/{:d}'.format(n+1, n_soundscapes))
        # create a scaper
        sc = scaper.Scaper(duration, fg_folder, bg_folder)
        sc.protected_labels = []
        sc.ref_db = ref_db

        # add background
        sc.add_background(label=('choose', []),
                          source_file=('choose', []),
                          source_time=('const', 0))

        # add a single foreground event to the file
        sc.add_event(label=('choose', []),
                     source_file=('choose', []),
                     source_time=(source_time_dist, source_time),
                     event_time=(event_time_dist, event_time_mean, event_time_std, event_time_min, event_time_max),
                     event_duration=(event_duration_dist, event_duration_min, event_duration_max),
                     snr=(snr_dist, snr_min, snr_max),
                     pitch_shift=(pitch_dist, pitch_min, pitch_max),
                     time_stretch=(time_stretch_dist, time_stretch_min, time_stretch_max))

        # generate
        audiofile = osp.join(out_folder_500, f"{n}.wav")
        jamsfile = osp.join(out_folder_500, f"{n}.jams")
        txtfile = osp.join(out_folder_500, f"{n}.txt")

        sc.generate(audiofile, jamsfile,
                    allow_repeated_label=True,
                    allow_repeated_source=True,
                    reverb=0.1,
                    disable_sox_warnings=True,
                    no_audio=False,
                    txt_path=txtfile)

    rm_high_polyphony(out_folder_500, 3)
    out_csv = osp.join('..', 'eval', 'soundscapes_generated_var_onset',
                                                    "500ms.csv")
    post_processing_annotations(out_folder_500, output_folder=out_folder_500,
                                output_csv=out_csv)
    df = pd.read_csv(out_csv, sep="\t")
    # Be careful, if changing the values of the added onset value,
    # you maybe want to rerun the post_processing_annotations to be sure there is no inconsistency
    out_folder_5500 = osp.join(out_folder, "5500ms")
    create_folder(out_folder_5500)
    add_onset = 5.0
    df["onset"] += add_onset
    df["offset"] = df["offset"].apply(lambda x: min(x, add_onset))
    generate_new_fg_onset_files(add_onset, out_folder_500, out_folder_5500)
    df.to_csv(osp.join('..', 'eval', 'soundscapes_generated_var_onset', "5500ms.csv"),
              sep="\t", float_format="%.3f", index=False)

    out_folder_9500 = osp.join(out_folder, "9500ms")
    create_folder(out_folder_9500)
    add_onset = 9.0
    df = pd.read_csv(out_csv, sep="\t")
    df["onset"] += add_onset
    df["offset"] = df["offset"].apply(lambda x: min(x, add_onset))
    generate_new_fg_onset_files(add_onset, out_folder_500, out_folder_9500)
    df.to_csv(osp.join('..', 'eval', 'soundscapes_generated_var_onset', "9500ms.csv"),
              sep="\t", float_format="%.3f", index=False)
