# -*- coding: utf-8 -*-
"""
"""

import unittest

from easytest import EasyTest

import tempfile
import os
from file import File
import numpy as np


class TestData(unittest.TestCase):

    def setUp(self):
        self.refdir = tempfile.mkdtemp() + os.sep
        os.makedirs(self.refdir + 'A' + os.sep)
        os.makedirs(self.refdir + 'B' + os.sep)
        self.files = ['a.txt', 'b.dat', 'c.xls', 'd.doc',  'A' + os.sep + 'Aout1.dat', 'A' + os.sep + 'Aout2.dat',  'B' + os.sep + 'Bout.dat']
        for f in self.files:
            #print f
            #print self.refdir + f
            o = open(self.refdir + f, 'w')
            o.write('test')
            o.close()

        output_directory = tempfile.mkdtemp() + os.sep
        os.system('cp -r ' + self.refdir + '* ' +  output_directory)
        s = 'echo "Hello world"'
        l = ['a', 'xx', 'b']
        self.T = EasyTest(s, l, refdirectory=self.refdir, output_directory = output_directory)

    def test_init(self):
        T = self.T
        s = 'echo "Hello world"'
        self.assertEqual(T.exe, s)
        l = ['a', 'xx', 'b']
        for i in xrange(len(l)):
            self.assertEqual(l[i],T.args[i])
        self.assertEqual(T.refdirectory, self.refdir)

    def test_get_reference_file_list(self):
        T = self.T

        files = T._get_reference_file_list('all')
        print self.files
        for f in files:
            self.assertTrue(f.replace(self.refdir,'') in self.files)
            self.assertTrue(self.refdir in f)
        self.assertEqual(len(files), len(self.files))

        ref = ['xx.png', 'yy.txt']
        files = T._get_reference_file_list(ref)
        for f in files:
            self.assertTrue(os.path.basename(f) in ref)
            self.assertTrue(self.refdir in f)
        self.assertEqual(len(files), len(ref))

    def test_test_files(self):
        T = self.T
        self.assertTrue(T._test_files(T._get_reference_file_list('all')))
        self.assertFalse(T._test_files(['nope.z']))

    def test_execute(self):
        T = self.T
        T.run_tests(files='all', checksum_files='all', check_size='all')

    def test_test_checksum(self):
        T = self.T
        tdir = tempfile.mkdtemp() + os.sep
        T.refdirectory = tdir
        #write some file with different content
        tfile = tdir + 'a.txt'
        o=open(tfile,'w')
        o.write('test1')
        o.close()

        self.assertFalse(T._test_checksum([tfile]))
        self.assertTrue(T._test_checksum([self.refdir + 'a.txt']))

    def test_test_filesize(self):
        T = self.T
        tdir = tempfile.mkdtemp() + os.sep
        T.refdirectory = tdir
        #write some file with different content
        tfile = tdir + 'a.txt'
        o=open(tfile,'w')
        o.write('test1')
        o.close()

        self.assertFalse(T._test_filesize([tfile]))
        self.assertTrue(T._test_filesize([self.refdir + 'a.txt']))

    def test_netcdf_compare(self):
        #self.T = EasyTest(s, l, refdirectory=self.refdir, output_directory = output_directory)

        nx = 10
        ny = 20
        variables = ['var1','var2','var3']
        f1 = tempfile.mktemp(suffix='.nc')
        f2 = tempfile.mktemp(suffix='.nc')
        f3 = tempfile.mktemp(suffix='.nc')
        f4 = tempfile.mktemp(suffix='.nc')

        F1 = File(f1, 'x', 'y', mode='w')
        F1.create_dimension('x', nx)
        F1.create_dimension('y', ny)

        F2 = File(f2, 'x', 'y', mode='w')
        F2.create_dimension('x', nx)
        F2.create_dimension('y', ny)

        F3 = File(f3, 'x', 'y', mode='w')
        F3.create_dimension('x', nx)
        F3.create_dimension('y', ny)

        F4 = File(f4, 'x', 'y', mode='w')
        F4.create_dimension('x', nx)
        F4.create_dimension('y', ny)

        cnt = 1
        for k in variables:
            x = np.random.random((ny,nx))
            x = np.ma.array(x, mask=x !=x)
            F1.append_variable(k, x)
            F2.append_variable(k, x)  # ... two same files
            y = np.random.random((ny,nx))
            y = np.ma.array(y, mask=y !=y)
            F3.append_variable(k, y)  # ... and one different
            if cnt == 1:
                F4.append_variable(k, x)  # one file with different number of variables
            cnt += 1

        F1.close()
        F2.close()
        F3.close()
        F4.close()

        T = self.T
        self.assertTrue(T._compare_netcdf(f1, f2, compare_variables=True, compare_values=False))
        self.assertTrue(T._compare_netcdf(f1, f2, compare_variables=False, compare_values=True))
        self.assertTrue(T._compare_netcdf(f1, f2, compare_variables=True, compare_values=True))

        self.assertTrue(T._compare_netcdf(f1, f3, compare_variables=True, compare_values=False))
        self.assertFalse(T._compare_netcdf(f1, f3, compare_variables=False, compare_values=True))
        self.assertFalse(T._compare_netcdf(f1, f3, compare_variables=True, compare_values=True))

        self.assertFalse(T._compare_netcdf(f1, f4, compare_variables=True, compare_values=False))


if __name__ == '__main__':
    unittest.main()
