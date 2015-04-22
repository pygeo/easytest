"""
sample script for ESMValTool testing
"""

import sys
sys.path.insert(0,'/home/m300028/shared/dev/svn/easytest/')

import os
import shutil

from easytest import EasyTest


class ESMValToolTest(EasyTest):

    def __init__(self, **kwargs):
        self.nml = kwargs.pop('nml', None)
        assert self.nml is not None, 'Namelist needs to be provided!'

        #exe = kwargs.pop('exe', None)
        exe = 'python main.py'
        assert exe is not None, 'Executable needs to be given!'

        self.esmval_dir = kwargs.pop('esmval_dir', None)
        assert self.esmval_dir is not None, 'esmval_dir directory needs to be given'

        #output_directory = get_output_dir_from_namelist()

        output_directory = '.'   # TODO

        super(ESMValToolTest,self).__init__(exe, args=[self.nml], output_directory=output_directory, **kwargs)

    def generate_reference_data(self):
        """
        generate reference data by executing the namelist once and then copy results
        to the output directory
        """
        self._execute(wdir=self.esmval_dir)

        # copy results from output directory to reference directory
        #self._copy_output()

    def _copy_output(self):
        """ copy entire result output to reference data directory """
        shutil.copytree(self.output_directory, self.refdirectory)


class SeaIceTest(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/seaice.xml'
        refdir = '.' + os.sep + 'refdata' + os.sep + 'seaice' + os.sep
        esmval_dir = '/home/m300028/shared/dev/svn/ESMVAL/svn/trunk2'
        super(SeaIceTest,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)

class DummyTest(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/namelist_dummy_python.xml'
        refdir = '.' + os.sep + 'refdata' + os.sep + 'dummy' + os.sep
        esmval_dir = '/home/m300028/shared/dev/svn/ESMVAL/svn/trunk2'
        super(DummyTest,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)


##### test

ST = DummyTest()
ST.generate_reference_data()
