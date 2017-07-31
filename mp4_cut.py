from datetime import datetime, timedelta
from subprocess import PIPE, call, Popen
import tempfile, os, argparse, sys, re

def get_file_duration(infilename):
   '''
   :param infilename: input mp4 filename
   :type infilename: str
   :returns: (h,m,s) tuple 
   '''
   cmd=['ffmpeg','-i',infilename]
   p=Popen(cmd,stdout=PIPE,stderr=PIPE)
   output=p.stderr.read()
   match=re.search('Duration: (.*?)\.',output)
   match.groups()
   h,m,s= parse_ts(match.groups()[0])
   return datetime(2017,1,1,h,m,s)

def parse_ts(instring):
   x=instring.split(':')
   if len(x)==2:
      x.insert(0,'0')
   h,m,s = map(int,x)
   return (h,m,s)

def format_ts(instring):
   h,m,s=parse_ts(instring)
   return '%02d:%02d:%02d'%(h,m,s)

def run_cmd_dt(start,end,infname,outfname):
   assert isinstance(start,datetime)
   assert isinstance(end,datetime)
   start_time='%02d:%02d:%02d'%(start.hour,start.minute,start.second)
   end_time='%02d:%02d:%02d'%(end.hour,end.minute,end.second)
   run_cmd(start_time,end_time,infname,outfname)

def run_cmd(start='00:00:00',end='23:00:00',infname='foo.mp4',outfname='outfoo.mp4'):
   duration = get_duration(start,end)
   cmd=['ffmpeg','-ss',format_ts(start),'-t',duration,'-i',
                 infname,'-acodec','copy','-vcodec','copy',
                 outfname]
   call(cmd,stdout=PIPE,stderr=None)

def get_duration(start,end):
   hs,ms,ss=parse_ts(start)
   he,me,se=parse_ts(end)
   start_time=datetime(2017,1,1,hs,ms,ss)
   end_time=datetime(2017,1,1,he,me,se)
   duration=str(end_time - start_time)
   if len(duration)==7: duration = '0'+duration
   return duration

if __name__ == '__main__':
   parse = argparse
   parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
   description='''Cut a section out of MP4 file and return it using ffmpeg
without re-encoding. 

Example: extract from start to 00:11:44 

   % python mp4_cut.py -e 11:44  -i L.mp4 -o foo.mp4 

Example: extract from 00:15:00 to 00:17:34 

   % python mp4_cut.py -s 15:00 -e 17:34  -i L.mp4 -o foo.mp4 
 
You can also take the complement of the selected slice by using the
--invert flag

   % python mp4_cut.py --inverse -s 15:00 -e 17:34  -i L.mp4 -o foo.mp4 

The two complementary parts are joined to make the output file.''')
   parser.add_argument("-i","--input-file", 
                           dest="infile",
                           help='input file',
                           default='',
                           )
   parser.add_argument("-o","--output-file", 
                           dest="outfile",
                           help='output file',
                           default='',
                           )
   parser.add_argument("-s","--start-time", 
                           dest="start_time",
                           help='hh:mm:ss',
                           default='00:00:00',
                           )
   parser.add_argument("-e","--end-time", 
                           dest="end_time",
                           help='hh:mm:ss',
                           default='',
                           )
   parser.add_argument("-c","--chunk_duration", 
                           help='Divide into <n> chunks of this duration hh:mm:ss. Overrides other flags!',
                           default='',
                           )
   parser.add_argument("--invert", 
                        dest='invert',
                        default=False,
                        action='store_true',
                        help="return complement of indicated section")

   args = parser.parse_args()
   if args.chunk_duration:
      # this over-rides other options
      hc,mc,sc=parse_ts(args.chunk_duration)
      start_time=datetime(2017,1,1,0,0,0)
      end_time=datetime(2017,1,1,hc,mc,sc)
      file_length = get_file_duration(args.infile)
      dt = timedelta(hours=hc,minutes=mc,seconds=sc)
      outfilename_head = args.outfile.replace('.mp4','')
      n=0
      while end_time < file_length:
         run_cmd_dt(start_time,end_time,args.infile,'%s_%03d.mp4'%(outfilename_head,n))
         start_time = end_time
         end_time = start_time + dt
         n += 1
      sys.exit()

   duration = get_duration(args.start_time,args.end_time)
   if args.invert: 
      if args.start_time=='00:00:00': # tail section
         duration = '23:00:00'
         cmd=['ffmpeg','-ss',format_ts(args.end_time),'-t',duration,'-i',
                       args.infile,'-acodec','copy','-vcodec','copy',
                       args.outfile]
         call(cmd,stdout=PIPE,stderr=None)
      else: # middle section
         start_time='00:00:00'
         filename1=tempfile.mktemp('.mp4',dir=os.getcwd())
         filename2=tempfile.mktemp('.mp4',dir=os.getcwd())
         run_cmd(start_time,args.start_time,args.infile,filename1)
         run_cmd(args.end_time,'23:00:00',args.infile,filename2)
         fname= tempfile.mktemp(suffix='.txt',dir=os.getcwd())
         with open(fname,'w') as fd:
            fd.write('file '+os.path.split(filename1)[1]+'\n')
            fd.write('file '+os.path.split(filename2)[1]+'\n')
            fd.close()
         # ffmpeg -safe 0 -f concat -i list.txt -c copy outfile.mp4
         cmd=['ffmpeg','-safe','0','-f','concat','-i',fname,'-c','copy',args.outfile ]
         call(cmd,stdout=PIPE,stderr=None)
         for i in (filename1,filename2,fname):
            os.unlink(i)
   else:
      run_cmd(args.start_time,args.end_time,args.infile,args.outfile)

