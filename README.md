# Testing

Use this repository to run tests on MRtrix3 commands and ensure that the output is consistent with expectation. If you intend to help with development of MRtrix3, you will need to set this up to ensure your changes do not introduce regressions. 

## Setup

- clone this repo:
    
        git clone https://github.com/MRtrix3/testing.git

- create a symbolic link to the build script in your main MRtrix3 git clone. For example, if you cloned the testing repo within your main MRtrix3 folder:
    
        ln -s ../build

- run the `./run_tests.sh` script:

        ./run_tests.sh
        
  This will build the main MRtrix3 install, then build the testing executables, then run the tests. All activities are logged to the `testing.log` file - take a look in there for details of any failures.
  
