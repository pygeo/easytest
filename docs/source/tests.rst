Implemented tests
=================

The following tests are currently implemented:

* *File testing*: The file tests simply check if files with appropriate filenames are produced by a diagnostic. It takes all files from the reference directory and looks if the output of the test namelist produce the same filenames. No content is checked!
* *MD5 checksum*: To check if the content of two files are similar, the `MD5 checksum <http://en.wikipedia.org/wiki/MD5>`_ is used. *Note, that this is not ensuring that the files are identical, but are very similar*. Problems with MD5 checksums can occur when comparing e.g. postscript files. These typically always differ in their header and therefore produce different checksums. The user can therefore exclude specific filetypes from the comparison.

The following tests are planned:

* *graphic file content*: It is planned to implement a test that compares the similarity between graphic files.
