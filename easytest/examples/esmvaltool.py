"""
sample script for ESMValTool testing
"""

import sys
sys.path.insert(0,'/home/m300028/shared/dev/svn/easytest/')   # TODO (not needed when installed correctly as python package)

import os
import shutil

from easytest import EasyTest

# ESMValTool installation path
esmval_dir = '/home/m300028/shared/dev/svn/ESMVAL/svn/trunk2'  # todo: would be best if during ESMValTool installation an environment variable would be set.

class ESMValToolTest(EasyTest):
    """
    main class for all ESMValTool tests
    """

    def __init__(self, **kwargs):
        """
        output_directory : str
            a default output directory is set as ESMVALROOT/work/plots
            but user can specify custom output directory
        """
        self.nml = kwargs.pop('nml', None)
        assert self.nml is not None, 'Namelist needs to be provided!'

        exe = 'python main.py'  # the command to call ESMValTool
        assert exe is not None, 'Executable needs to be given!'

        self.esmval_dir = kwargs.pop('esmval_dir', None)
        assert self.esmval_dir is not None, 'esmval_dir directory needs to be given'

        output_directory = kwargs.pop('output_directory', self.esmval_dir + os.sep + 'work' + os.sep + 'plots')  # default output directory

        self.refdir_root = self.esmval_dir + 'testdata' + os.sep

        super(ESMValToolTest,self).__init__(exe, args=[self.nml], output_directory=output_directory, **kwargs)

    def generate_reference_data(self):
        """
        generate reference data by executing the namelist once and then copy results
        to the output directory
        """
        self._execute(wdir=self.esmval_dir)

    def run_nml(self):
        self._execute(wdir=self.esmval_dir)

    def _copy_output(self):
        """ copy entire result output to reference data directory """
        shutil.copytree(self.output_directory, self.refdirectory)



class DummyTest(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/namelist_dummy_python.xml'
        refdir = '.' + os.sep + 'refdata' + os.sep + 'dummy' + os.sep
        super(DummyTest,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)

class PerfMetricCMIP5Test(ESMValToolTest):
    def __init__(self):

        # 1) define here the name of the namelist
        nml_name = 'namelist_perfmetrics_CMIP5_test.xml'

        # 2) specify here the full path of the namelist (relative to ESMValTool root)
        nml = 'nml/test_suites/dlr/' + nml_name

        # 3) define here the location of the reference directory
        #    note that it is expeced that the directory has the same name as the namelist
        refdir = esmval_dir + os.sep + os.path.splitext(nml_name)[0] + '/output/plots/'

        super(PerfMetricCMIP5Test,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)


PT = PerfMetricCMIP5Test()
PT.run_nml()
PT.run_tests(execute=False, graphics=None, checksum_files='all',files='all')


