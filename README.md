# mp4utils

Python 2.7 powered ffmpeg utilities. You need to have ffmpeg installed
separately.

Example: extract from start to 00:11:44 
----------------------------------------

    % python mp4_cut.py -e 11:44  -i inputfile.mp4 -o outputfile.mp4 

Note that you don't have to use the leading zeros for the hours. The general
call is the following:

    % python mp4_cut.py -s [hh]:mm:ss -e [hh]:mm:ss -i inputfile.mp4  -o outputfile.mp4

Using your own `inputfile` and `outputfile`.

Example: extract from 00:15:00 to 00:17:34 
-------------------------------------------

    % python mp4_cut.py -s 15:00 -e 17:34  -i inputfile.mp4 -o outputfile.mp4 

You can also take the complement of the selected slice by using the
`--invert` flag

    % python mp4_cut.py --inverse -s 15:00 -e 17:34  -i inputfile.mp4 -o outputfile.mp4 

The two complementary parts are joined to make the output file.
