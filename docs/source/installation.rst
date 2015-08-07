Installation
============


Using pip
---------

TBD




The standard python way
-----------------------

TBD





From code repository
--------------------

Installation from the most recent code repository is also very easy in a few steps::

    # get the code
    cd /go/to/my/directory/
    git clone git@github.com:pygeo/easytest.git .

    # set the python path
    export PYTHONPATH=`pwd`:$PYTHONPATH
    echo PYTHONPATH



Test installation sucess
------------------------
Independent how you installed `easytest`, you should test that it was sucessfull by the following tests::

    python -c "import easytest"

If you don't get an error message, the module import was sucessfull.


