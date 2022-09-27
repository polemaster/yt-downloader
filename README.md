# yt-downloader: Download videos from YouTube using pytube
## Description
The project is aimed at downloading videos from YouTube directly, i.e. without any third-parties like online web tools, having only the URL of the video.
The program is written in Python and utilizes pytube python library. After running the program, it prompts you to enter the desired details
of the video such as resolution or captions. Having answered all the questions, the video is downloaded to ~\Downloads or ~/Downloads folder,
depending on your OS. It also has a possibility of merging the downloaded video and audio files using ffmpeg so that you can watch the video immediately after downloading.
## Requirements
* Python 3.10.0 or newer
* *(optional)* ***ffmpeg*** *(must be also included in your path)*
## Installation
```pip install pytube``` \
*(optional) ![ffmpeg.org](https://ffmpeg.org/)*
## Usage
You don't need really need ffmpeg installed. In that case, answer ***no*** to the question about merging files. The program will then download
video and audio files separately without merging them. \
After installing pytube, you can download main.py file from this projects and run it with the python interpreter: \
```py main.py```          &emsp;&emsp;&emsp;(Windows) \
```python main.py```      &emsp;(Linux) \
Next follow the instructions given by the program.
## Sources
![pytube.io](https://pytube.io/)       &emsp;&emsp;&emsp;(pytube documentation)
## Additional notes
* The reason that this project downloads video and audio separately is that YouTube supports a streaming technique called Dynamic Adaptive Streaming over HTTP (DASH). Due to this fact, pytube can download videos together with audio (called progressive) only up to 720p resolution. So I decided to take advantage of
DASH and implemented adaptive (DASH) streams (in pytube) which support higher resolutions.
* You can use ffmpeg independently of the program. You can also use other softawre than ffmpeg to combine video and audio files.
