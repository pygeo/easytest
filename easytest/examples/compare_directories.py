import sys

sys.path.insert(0,'/home/m300028/shared/dev/svn/easytest/')

from easytest import EasyTest

sdir = '/home/m300028/shared/data/SEP/data_sources/CERES/DATA'
tdir = '/home/m300028/shared/data/SEP/data_sources/CERES/DATA'

T = EasyTest(None, refdirectory=sdir, output_directory=tdir)
T.run(files='all', graphics=None, checksum_files='all')

