

Todo for ESMValTool application
-------------------------------

For the application to the ESMValTool, the following further modifications would be helpfull.

* test namlist input directories: the namelists specify where input data for is located. Unfortunately, the path names are hardcoded in the namelist itself and therefore need to be always adapted by the user of the code. It would be better if ESMValTool would have some environment variable $DATA_ROOT and then only relative path names would be used instead.

