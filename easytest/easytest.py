
import os
import glob
import hashlib
import pdb
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
        self.sucess = True

        assert self.refdirectory is not None, 'Reference directory needs to be given!'
        if self.refdirectory[-1] != os.sep:
            self.refdirectory += os.sep

        assert self.output_directory is not None, 'Output directory needs to be given!'
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        if self.output_directory[-1] != os.sep:
            self.output_directory += os.sep

    def run_tests(self, files=None, graphics=None, checksum_files=None, execute=True):
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

        if execute:
            if self.exe is not None:
                self._execute()
        if files is not None:
            files2test = self._get_reference_file_list(files)
            assert len(files2test) > 0, 'No testfiles were found in the reference directory! ' + self.refdirectory
            file_test = self._test_files(files2test)
        if graphics is not None:
            assert False, 'Graphic testing currently not implemented yet!'
            #self._test_graphics(self._get_graphic_list(graphics))
        if checksum_files is not None:
            files2testchk = self._get_reference_file_list(checksum_files)
            assert len(files2testchk) > 0, 'No testfiles were found in the reference directory for checksum! ' + self.refdirectory
            chk_test = self._test_checksum(files2testchk)
        if files is not None:
            if file_test:
                print 'File     ... SUCESSFULL'
            else:
                print 'File     ... FAILED'
                self.sucess = False

        if checksum_files is not None:
            if chk_test:
                print 'Checksum ... SUCESSFULL'
            else:
                print 'Checksum ... FAILED'
                self.sucess = False

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
                assert False, 'Argument FILES has not been correctly specified!'
        return files

    def _get_files_from_refdir(self):
        """ get list of files from reference directory """
        #return glob.glob(self.refdirectory + '*')
        # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        import fnmatch
        matches = []
        for root, dirnames, filenames in os.walk(self.refdirectory):
          for filename in fnmatch.filter(filenames, '*'):
            matches.append(os.path.join(root, filename))
        return matches

    def _get_graphic_list(self, files):
        assert False

    def _xxxget_cmd_list(self):
        """
        get command list
        """
        r = []
        r.append(self.exe)

        for a in self.args:
            r.append(a)
        return r

    def _get_cmd_list(self):
        """
        get command list
        """
        r = ''
        r += self.exe
        for a in self.args:
            r += ' ' + a
        return r

    def _execute(self, wdir='.'):
        """
        run the actual program

        generates a command line string for execution in a shell.
        and then executes the command

        Parameters
        ----------
        wdir : str
            working directory
        """
        if wdir != '.':
            curdir = os.path.realpath(os.curdir)
            os.chdir(wdir)

        # execute command line
        cmd = self._get_cmd_list()
        print 'Command line: ', cmd
        #subprocess.call(cmd, shell=True)  # todo use subprocess
        os.system(cmd)

        if wdir !='.':
            os.chdir(curdir)

    def _test_files(self, reffiles):
        """
        test availability of files

        Parameters
        ----------
        reffiles : list
            list of reference files to agains
        """
        res = True
        for f in reffiles:
            # get list of expected plot files
            sf = f.replace(self.refdirectory,self.output_directory) #+ os.path.basename(f)
            if os.path.exists(sf):
                pass
            else:
                res = False
                print 'Failure: ', sf
        return res

    def _test_graphics(self, reffiles):
        assert False

    def _test_checksum(self, reffiles):
        """
        perform a checksum test for all reffiles given
        against the files in the current plot dir

        Parameters
        ----------
        reffiles : list
            list of files to be processed
        """

        res = True
        for f in reffiles:
            cref = self.hashfile(open(f, 'rb'), hashlib.sha256())

            sf = f.replace(self.refdirectory, self.output_directory)
            sfref = self.hashfile(open(sf, 'rb'), hashlib.sha256())

            print sf, f, self.refdirectory, self.output_directory

            if cref != sfref:
                print ''
                print 'Different sha256 key: ', os.path.basename(f), cref.encode('hex'), sfref.encode('hex')
                print sf
                print f
                res = False

        return res

    def hashfile(self, afile, hasher, blocksize=65536):
        """
        perform memory effiecient sha256 checksum on
        provided filename.
        See https://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file#3431835

        Parameters
        ----------
        afile : string
        hasher: hash function
        blocksize: file read chunk size
        """
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher.digest()
