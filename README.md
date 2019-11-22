# Desed_synthetic
Synthetic data of Desed dataset (used in DCASE 2019 task 4), and creation of new mixtures.

## Description
This repository gives the information and the code to download the data, reproduce the synthetic dataset used in 
DCASE 2019 task 4 and examples of how you can create your own data 
(using [Scaper](https://github.com/justinsalamon/scaper) [[1]](#1)).

You can find information about this dataset in this paper: [link](https://hal.inria.fr/hal-02160855).
The evaluation part was submitted to ICASSP and will be updated later.

The dataset is available here: **[zenodo link](https://zenodo.org/record/3550599)**

* Background files are extracted from SINS [[2]](#2), MUSAN [[3]](#3) or Youtube and have been selected because they 
contain a very low amount of our sound event classes.
* Foreground files are extracted from Freesound [[4]](#4)[[5]](#5) and manually verified to check the quality 
and segmented to remove silences.


#### Desed_synthetic for DCASE 2019 task 4:
10 second audio clips generated with [Scaper](https://github.com/justinsalamon/scaper).

**Training**:
There are 2060 background files from SINS and 1009 foreground from Freesound.

We generated 2045 10s files with a FBSNR between 6dB to 30dB.

**Eval**
There are 12(Freesound) + 5(Youtube) background files and 314 foreground files. 
Generating different subsets to test robustness against some parameters.

Taking a background sound and multiple foreground sounds and associating them in different conditions:
* Varying the foreground-background signal to noise ratio (FBSNR).
* Varying the onsets: Generating foreground sounds only at the beginning, middle or end of the 10 seconds.
* Using long 'foreground' event classes as background, and short events as foreground. 
* Degrading the final 10s mixtures.


### Technical description
In this repository, you can find:
* `src/` folder with the code to generate sounds used in DCASE challenge or new ones.
* `test` fodler (partial testing) 

After downloading the data (see below) you should have this tree:
```
dataset root
└───training                            
│   └───soundbank                       (Isolated sounds to generate mixtures)
│   │   └───background                    
│   │   │   └───sins     
│   │   │ 
│   │   └───foreground
│   │   	└───Event_classname     (14 folders for event classes + those without onsets or offsets)
│   │
│   └───soundscapes                     (Files used in DCASE challenge)
│   │   └───X.jams                      (X being the id number of the file)
│   └───synthetic.csv                   (Metadata file of the training soundscapes)
│    
└───eval                                
│   └───soundbank                       (Isolated sounds to generate mixtures)
│   │   └───background                  (Background from musan and youtube should only contain background sounds (no event))
│   │   │	└───freesound           (From MUSAN)
│   │   │	└───youtube
│   │   └───foreground                  
│   │   │	└───Event_classname     (18 folders)
│   │   └───background_long             (Variation of foreground, long events are used as background sounds)
│   │   │	└───Event_classname     (5 folders)
│   │   └───foreground_short            (Variation of foreground, only short events)
│   │   │	└───Event_classname     (5 folders)
│   │   └───foreground_on_off           (Variation of foreground, take only files with an onset and offset)
│   │   │	└───Event_classname     (10 folders)
│   │   │                 
│   │   └───soundscapes
│   │   	└───subset_name         (10 folders names of the different scenarios using scaper)
│   │   	└───distorted           (6 folders names of the distorted subsets)
│   │   	└───subset_name.csv     (Metadata file of the different subsets)
│   │
│   └───soundscapes			(Files used in DCASE challenge)
│         X.jams                        (X being the id number of the file)  
│
└───src                                 (This repo, described in 'Generating sounds' below)
    └───...
```
*All folder without examples of files contain audio (.wav) files*

## Download
Link to the zenodo repo: **[zenodo link](https://zenodo.org/record/3550599)**

To download the **training**, there are 2 steps:
* Run ```python get_background_training.py``` in the `src/` folder. (Background files from SINS [[2]](#2))
* Download `training.tar.gz` of the zenodo repo. Corresponding to the 
"foreground soundbank" and the JAMS soundscapes used in the DCASE challenge.

To download the **evaluation**:
* Download `eval.tar.gz` of the zenodo repo. (used data from MUSAN[[3]](#3), youtube and freesound)
Corresponding to the "soundbank" and the "JAMS soundscapes" used in the DCASE challenge.

## Generating sounds
##### Desed_synthetic for DCASE 2019 task 4 challenge 
Data has to be downloaded (see above).

* The distorted versions are already in a wav format, because we use XXX tool (in Matlab) 
to generate them which we still didn't transpose to python.
* Run ````python generate_wav.py```` in the `src/` folder for the other scenarios.

##### Generate new sounds 
To generate new sounds, in the same way as the Desed_synthetic dataset, you can use these files:
 * `generate_training.py`, uses `event_occurences_train.json` for co-occurrence of events.
 * `generate_eval_FBSNR.py` generates similar subsets with different foreground-background sound to noise ratio (fbsnr): 30dB, 24dB, 15dB, 0dB.
 Uses `event_occurences_eval.json` for occurence and co-occurrence of events.  
 * `generate_eval_var_onset.py` generates subsets with a single event per file, the difference between subsets is
  the onset position:
    1. Onset between 0.25s and 0.75s. 
    2. Onset between 5.25s and 5.75s. 
    3. Onset between 9.25s and 9.75s.
 * `generate_eval_long_short.py` generates subsets with a long event in the background and short events in the foreground, 
 the difference beteen subsets is the FBSNR: 30dB, 15dB, 0dB. 
 * `generate_eval_distortion.py` generates distortion subsets, not yet in python, 
 see `generate_eval_distortion.m` for matlab code (will be updated later).

When a script is generating multiple subfolder but only one csv file, it means it is the same csv for the different cases.
Example: when modifying the FBSNR, we do not change the labels (onset, offsets). 

## Licenses
The python code is publicly available under the MIT license, see the LICENSE file. 
The matlab code is taken from the Audio degradation toolbox [[6]](#6), see the LICENSE file.

The different datasets contain a license file at their root for the attribution of each file.

The different platform used are: Freesound [[4]](#4)[[5]](#5), Youtube, MUSAN [[3]](#3) and SINS [[2]](#2).  

## Citing
If you use this repository, please cite this paper:
N. Turpault, R. Serizel, A. Parag Shah, J. Salamon. 
Sound event detection indomestic environments with weakly labeled data and soundscape synthesis. 
Workshop on Detectionand Classification of Acoustic Scenes and Events, Oct 2019, New York City, USA.

## References
<a id="1">[1]</a> J. Salamon, D. MacConnell, M. Cartwright, P. Li, and J. P. Bello. Scaper: A library for soundscape synthesis and augmentation
In IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), New Paltz, NY, USA, Oct. 2017.

<a id="2">[2]</a> Gert Dekkers, Steven Lauwereins, Bart Thoen, Mulu Weldegebreal Adhana, Henk Brouckxon, Toon van Waterschoot, Bart Vanrumste, Marian Verhelst, and Peter Karsmakers.
The SINS database for detection of daily activities in a home environment using an acoustic sensor network.
In Proceedings of the Detection and Classification of Acoustic Scenes and Events 2017 Workshop (DCASE2017), 32–36. November 2017.

<a id="3">[3]</a> David Snyder and Guoguo Chen and Daniel Povey.
MUSAN: A Music, Speech, and Noise Corpus.
arXiv, 1510.08484, 2015.

<a id="4">[4]</a> F. Font, G. Roma & X. Serra. Freesound technical demo. In Proceedings of the 21st ACM international conference on Multimedia. ACM, 2013.
 <a id="5">[5]</a> E. Fonseca, J. Pons, X. Favory, F. Font, D. Bogdanov, A. Ferraro, S. Oramas, A. Porter & X. Serra. Freesound Datasets: A Platform for the Creation of Open Audio Datasets.
In Proceedings of the 18th International Society for Music Information Retrieval Conference, Suzhou, China, 2017.

 <a id="5">[6]</a> M. Mauch and S. Ewert, “The Audio Degradation Toolbox and its Application to Robustness Evaluation”. 
In Proceedings of the 14th International Society for Music Information Retrieval Conference (ISMIR 2013), Curitiba, Brazil, 2013.