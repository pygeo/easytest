
import os
import glob
import hashlib
import subprocess


class EasyTest(object):
    def __init__(self, exe, args=None, refdirectory=None, output_directory=None):
        """
        Parameters
        ---------
        cmd : str
            command that will be executed at shell
        args : list
            list with command line arguments
        """
        self.exe = exe
        self.args = args
        self.refdirectory = refdirectory
        self.output_directory = output_directory

        assert self.refdirectory is not None, 'Reference directory needs to be given!'
        assert os.path.exists(self.refdirectory)
        if self.refdirectory[-1] != os.sep:
            self.refdirectory += os.sep

        assert self.output_directory is not None, 'Output directory needs to be given!'
        assert os.path.exists(self.output_directory)
        if self.output_directory[-1] != os.sep:
            self.output_directory += os.sep

    def run(self, files=None, graphics=None, checksum_files=None):
        """
        Execute program and run tests

        Parameters
        ----------
        files : list/str
            list of filenames to be checked.
            If 'all' is given instead, then the program automatically
            tries to check for all files which are found in the
            reference data directory
        """

        if self.exe is not None:
            self._execute()
        if files is not None:
            file_test = self._test_files(self._get_reference_file_list(files))
        if graphics is not None:
            assert False
            #self._test_graphics(self._get_graphic_list(graphics))
        if checksum_files is not None:
            chk_test = self._test_checksum(self._get_reference_file_list(checksum_files))

        if files is not None:
            if file_test:
                print 'File     ... SUCESSFULL'
            else:
                print 'File     ... FAILED'

        if checksum_files is not None:
            if chk_test:
                print 'Checksum ... SUCESSFULL'
            else:
                print 'Checksum ... FAILED'

    def _get_reference_file_list(self, files):
        if type(files) is list:
            r = []
            for f in files:
                r.append(self.refdirectory + os.path.basename(f))
            return r
        else:
            if files == 'all':
                files = self._get_files_from_refdir()
            else:
                assert False
        return files

    def _get_files_from_refdir(self):
        """ get list of files from reference directory """
        return glob.glob(self.refdirectory + '*')

    def _get_graphic_list(self, files):
        assert False

    def _get_cmd_list(self):
        """ get command list """
        r = []
        r.append(self.exe)

        for a in self.args:
            print a
            r.append(a)

        return r

    def _execute(self, change_dir=True):
        """
        run the actual program

        generates a command line string for execution in a shell.
        and then executes the command

        Parameters
        ----------
        change_dir : bool
            change to directory of executable before executing the shell
        """
        if change_dir:
            curdir = os.path.realpath(os.curdir)
            if len(os.path.dirname(self.exe))>0:
                os.chdir(os.path.dirname(self.exe))

        # execute command line
        subprocess.call(self._get_cmd_list(), shell=True)

        if change_dir:
            os.chdir(curdir)

    def _test_files(self, reffiles):
        """
        test availability of files

        Parameters
        ----------
        files : list
            list of files to test
        """
        res = True
        for f in reffiles:
            if os.path.exists(self.output_directory + os.path.basename(f)):
                pass
            else:
                res = False
                print 'Failure: ', f
        return res

    def _test_graphics(self, files):
        assert False

    def _test_checksum(self, files):
        """
        perform a checksum test for all files given
        it reads a list of filenames to be tested and
        searches for the corresponding files in the reference
        data directory

        Parameters
        ----------
        files : list
            list of files to be processed
        """

        # get list of reference files
        reffiles = self._get_files_from_refdir()

        res = True
        for f in reffiles:
            cref = hashlib.md5(f).hexdigest()  # hash key of reference file
            for k in files:
                if os.path.basename(f) == os.path.basename(k):
                    kref = hashlib.md5(k).hexdigest()

                    if cref != kref:
                        print ''
                        print k
                        print f

                        print 'Different md5 key: ', os.path.basename(f), cref, kref
                        res = False
        return res


