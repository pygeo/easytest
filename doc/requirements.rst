ESMValTool testing
==================

Introduction
------------



Test requirements
-----------------

The following requirements need to be fulfilled to allow for automated testing.



Test data
~~~~~~~~~

Test data is mandatory for testing. An optimum test data set has the following characteristics:

* is a representative subset of data to be analyzed by the diagnostic
* small enough (space or time) to allow for **fast** test runs. Try to avoid big data volumes that slow down the entire testing procedure. Keep in mind that tests are executed many times during further development
* be a good reference. Testdata can be either real data or can be synthetic data where you know the correct solution. The latter would allow to compare results of a diagnostic against analytical reference solutions.





??? why separate testing namelist ??? Does not really make sense, as we want to test the implemented namelists / diagnostics!



A namelist needs to be provided that can be executed for testing purposes.



Todo
----

* implement automatic generation of reference dataset
* implement napkin framework for graphical comparison

