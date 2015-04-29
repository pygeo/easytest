Testing in ESMValTool
=====================

This documentation briefly describes how testing of ESMValTool works.


Why testing?
------------

TBD

Motivation ...
~~~~~~~~~~~~~~

Testing does not need to be complicated. This is what you basically need to do::

1. Define some class for your test::

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

2. run it::

    PT = PerfMetricCMIP5Test()
    PT.run_nml()
    PT.run_tests(execute=False, graphics=None, checksum_files='all',files='all')

That's it! Interested, then keep reading ...


How does the testing work in principle?
---------------------------------------

The general concept of the testing framework is that it compares results of a diagnostic with reference data generated once with the same inputs for the same diagnostic. The following checks can be performed:

1. check if all output files are available (Filecheck)
2. check that content of output files is the same (MD5 checksum check)
3. check that graphic files look the same (graphic check)  - TBD in development

What is needed?

* a namelist for your diagnostic tailored for your tests
* test data
* a script that implements your test


Generation of reference data
----------------------------

Each developer of a diagnostic needs to provide a small test dataset together with each diagnostic. This should contain all required input data to run the test diagnostic as well as expected results.

Thus in case that the code for a diagnostic is adapted/changed, the corresponding reference data for that diagnostic needs to be regenerated. Steps are as follows:

A test dataset shall be small enough to allow for frequent testing.

0. get ESMValTool testdata like described here (TBD)
1. Generate a test namelist
2. generate a directory with the name of the test namelist as subdirectory of the testdata folder
3. within that directory generate subdirectories "input" and "output"
4. put into "input" all required input data for the namelist, unless it is not covered by the already existing testdata
5. modify your testscript to follow the new pathes
6. run your test namelist once
7. check results
8. if results are fine, then copy the results that shall be tested into the "output" directory

That's it!

Compress the directory with the name of your diagnostic in the testdata directory and ship it with your code.



More details
------------

Testdata
~~~~~~~~

The testdata is expected to be organized as follows::

    ESMVALROOT/testdata/<name of test namelist>/
                                               /generic
                                               /input
                                                    /subdirectory structure with input data
                                               /output
                                                    /directory structure with expexted results

where

* **generic** provides generic observational and model data for testing required by several diagnostics
* **input** contains diagnostic specific input data
* **output** contains expected output of diagnostic

This can then e.g. look like illustrated in the file *example_structure.txt*



File testing
~~~~~~~~~~~~

The file tests simply check if files with appropriate filenames are produced by a diagnostic. It takes all files from the reference directory and looks if the output of the test namelist produce the same filenames. No content is checked!

File checksum
~~~~~~~~~~~~~

To check if the content of two files are similar, the `MD5 checksum <http://en.wikipedia.org/wiki/MD5>`_ is used.

*Note, that this is not ensuring that the files are identical, but are very similar*


Graphic files
~~~~~~~~~~~~~

TBD







