[comment]: <> (A README file that describes the script inside this folder.)

This README file describes the usage of the scripts inside this folder. In order of usage, the scripts are:

## Scripts

### `flatten_whiteboard_data.py`
This script generates a separate dataset including one sample folder for each captured whiteboard picture. Each sample folder contains the correspoding .txt file, the .ly file and the .png file.

### `generate_dataset_full.sh`
Executes all data generating scripts (generate_data.py, generate_hw_data.py, generate_augmented_data.py) in order to generate a full dataset. The dataset is saved in the `data`, `data_augmented`, `data_hw` and `data_hw_augmented` folders.

### `generate_data.py`
Generates a dataset of images of the random note sheets withing given a note-specific duration restriction (e.g. use a 1/16th note as a minimum duration). The dataset is saved in the `data` folder.

### `generate_augmented_data.py`
Given a folder of images, generates an augmented dataset of images. The dataset is saved in the `data_augmented` folder.


### `generate_hw_data.py`
Given a folder of images, generates a dataset of images with handwritten notes. The dataset is saved in the `data_hw` folder.

### `real_world_data_collection.py`
This script is used when collection real world data, e.g. from a webcam that is pointed at a whiteboard. It is used to collect images of the whiteboard and the corresponding Lilypond file. The images are saved in the `data_real` folder.

### `train.py`
Trains a model on the a set of given `train_data_paths`.

### `detect.py`
This script is used for live detection of notes. A trained model can be used to initialize. The current model is stored at HuggingFace and its path/name is set by the `MODEL_PATH` parameter inside `config/vision_node.yaml` The detected notes are shown in a window.