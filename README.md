# mp4utils

Python 2.7 powered ffmpeg utilities. You need to have ffmpeg installed
separately.

Example: extract from start to 00:11:44 
----------------------------------------

    % python mp4_cut.py -e 11:44  -i L.mp4 -o foo.mp4 

Example: extract from 00:15:00 to 00:17:34 
-------------------------------------------

    % python mp4_cut.py -s 15:00 -e 17:34  -i L.mp4 -o foo.mp4 
