"""
sample script for ESMValTool testing
"""

import sys
sys.path.insert(0,'/home/m300028/shared/dev/svn/easytest/')   # TODO

import os
import shutil

from easytest import EasyTest

# ESMValTool installation path
esmval_dir = '/home/m300028/shared/dev/svn/ESMVAL/svn/trunk2'  # todo

class ESMValToolTest(EasyTest):
    """
    main class for all ESMValTool tests
    """

    def __init__(self, **kwargs):
        self.nml = kwargs.pop('nml', None)
        assert self.nml is not None, 'Namelist needs to be provided!'

        #exe = kwargs.pop('exe', None)
        exe = 'python main.py'
        assert exe is not None, 'Executable needs to be given!'

        self.esmval_dir = kwargs.pop('esmval_dir', None)
        assert self.esmval_dir is not None, 'esmval_dir directory needs to be given'

        #output_directory = get_output_dir_from_namelist()

        output_directory = kwargs.pop('output_directory', './work/plots')  # default output directory

        super(ESMValToolTest,self).__init__(exe, args=[self.nml], output_directory=output_directory, **kwargs)

    def generate_reference_data(self):
        """
        generate reference data by executing the namelist once and then copy results
        to the output directory
        """
        self._execute(wdir=self.esmval_dir)

        # copy results from output directory to reference directory
        #self._copy_output()

    def run_nml(self):
        self._execute(wdir=self.esmval_dir)

    def _copy_output(self):
        """ copy entire result output to reference data directory """
        shutil.copytree(self.output_directory, self.refdirectory)


class SeaIceTest(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/seaice.xml'
        refdir = '.' + os.sep + 'refdata' + os.sep + 'seaice' + os.sep
        super(SeaIceTest,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)

class DummyTest(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/namelist_dummy_python.xml'
        refdir = '.' + os.sep + 'refdata' + os.sep + 'dummy' + os.sep
        super(DummyTest,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)

class PerfMetricCMIP5Test(ESMValToolTest):
    def __init__(self):
        # specify namelist name and reference data directory
        nml = 'nml/test_suites/dlr/namelist_perfmetrics_CMIP5_test.xml'
        #refdir = '.' + os.sep + 'refdata' + os.sep + 'dummy' + os.sep  # todo
        refdir = '/home/m300028/shared/dev/svn/ESMVAL/svn/trunk2/testdata/perfmetrics_CMIP5/output/plots/'  # todo

        super(PerfMetricCMIP5Test,self).__init__(nml=nml, refdirectory=refdir, esmval_dir=esmval_dir)


#todo recursive file check !!!
#with sundirectories !




# small datasets!
# all test namelists should haves same output directory ???? Otherwise as part of child class!





##### test

#~ ST = DummyTest()
#~ ST.generate_reference_data()
#~
#~ ST = SeaIceTest()
#~ ST.run_test()

PT = PerfMetricCMIP5Test()
#PT.run_nml()
PT.run_tests(execute=False, graphics=None, checksum_files=None,files='all')



#PT.run(files=None, graphics=None, checksum_files=None)



