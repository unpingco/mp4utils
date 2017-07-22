# Use ffmpeg to join an arbitrarily long list of compatible mp4 files
#
#  % python mp4_join.py -o foo.mp4 L1.mp4 L2.mp4 ...
#

from subprocess import PIPE, call
import tempfile, os, argparse

if __name__ == '__main__':
   parse = argparse
   parser = argparse.ArgumentParser()
   parser.add_argument(dest="infile",
                       help='input file(s)',
                       nargs='+',
                       )
   parser.add_argument("-o","--output-file", 
                       dest="outfile",
                       help='output file',
                       default='')
   args = parser.parse_args()
   fname= tempfile.mktemp(suffix='.txt',dir=os.getcwd())
   with open(fname,'w') as fd:
      for fn in args.infile:
         fd.write('file '+fn+'\n')
      fd.close()
   # ffmpeg -safe 0 -f concat -i list.txt -c copy outfile.mp4
   cmd=['ffmpeg','-safe','0','-f','concat','-i',fname,'-c','copy',args.outfile ]
   call(cmd,stdout=PIPE,stderr=None)
   os.unlink(fname)
