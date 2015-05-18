# -*- coding: utf-8 -*-
"""
"""

import unittest

from easytest import EasyTest

import tempfile
import os

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
        T.run_tests(files='all')

    def test_test_checksum(self):
        T = self.T
        tdir = tempfile.mkdtemp() + os.sep
        tfile = tdir + 'a.txt'
        o=open(tfile,'w')
        o.write('test1')
        o.close()

        self.assertFalse(T._test_checksum([tfile]))
        self.assertTrue(T._test_checksum([self.refdir + 'a.txt']))


if __name__ == '__main__':
    unittest.main()
