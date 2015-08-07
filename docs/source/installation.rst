Installation
============

There are different methods to install `easytest`. The first two are for users who just want to use the package, while the last one is for developers. All follow standard practice.

Using pip
---------

The `easytestpackage is provided on [pip](https://pypi.python.org/pypi/easytest). Install is as easy as::

    pip install easytest

The standard python way
-----------------------

You can also download the source code package from the [project website](https://pypi.python.org/pypi/easytest) or from [pip](https://pypi.python.org/pypi/easytest). Unpack the file you obt

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


