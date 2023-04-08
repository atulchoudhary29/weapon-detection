
# Weapon Detection

  

This repository provides a weapon detection solution using the YOLOv3 object detection model. The program detects weapons in real-time using a webcam, pre-recorded video, and alerts the user when a weapon is detected.

  

## Table of Contents

  

1. [Installation](#install)

2. [Usage](#usage)

3. [Examples](#examples)

<a  name="install"></a>

  

## 1. Installation

1. Clone the repository:

  

```

git clone git clone https://github.com/your_username/weapon-detection.git

```

2. Install the required packages:

  

```

pip install -r requirements.txt

```

  

3. Download the YOLOv3 weights and cfg files:

- [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)

- [yolov3.cfg](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)

	Save these files in the project directory.

<a  name="usage"></a>

## 2. Usage

The program can be run using either a webcam or a pre-recorded video file as input. Use the following command-line arguments to specify the desired mode:

  

```

usage: main.py [-h] [--webcam WEBCAM] [--play_video PLAY_VIDEO]
                           [--video_path VIDEO_PATH]
                           [--verbose VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  --webcam WEBCAM       True/False
  --play_video PLAY_VIDEO
                        True/False
  --video_path VIDEO_PATH
                        Path of video file
  --verbose VERBOSE     To print statements


```

  

-  `--webcam`: Set to True to use a webcam as input (default: False).

-  `--video_path`: Path to the video file to be processed (default: "video.mp4").

  

### Webcam Mode

  

To run the weapon detection program using your webcam, use the following command:

```

python main.py --webcam True

```

  

### Video Mode

  

To run the weapon detection program using a video file, use the following command:

  

```

python main.py --play_video True --video_path <path_to_video_file>

```

  

Replace `<path_to_video_file>` with the path to your video file.


<a  name="examples"></a>

## 3. Examples

  

Detect weapons in a video file named "security_footage.mp4":

  

```

python main.py --play_video True --video_path security_footage.mp4

```
