This repo stores tools necessary for automated QA in the HORTON project to ensure consistent quality of code across all repositories. However, the tools here can easily be used for assuring code quality in other mixed C++/Python projects as well.

Dependencies
============
Please use your favourite neighbourhood package manager to install these dependencies:

- cppcheck
- pycodestyle
- pydocstyle
- pylint
- nosetests
- coverage (from Ned Batchelder)
- doxygen

As for F24, Fedora users can find everything in the repos except for pycodestyle and pydocstyle. Those two can be installed via pip (with the --user flag!)

Installation
============
1) Fork the repository into your own github account. This will allow you to make changes to the buildkite testing scripts and also to configuration files.

2) Add your newly forked repo as a submodule of your current project. For example, if your repository is located at `git@github.com:MyAcct/InspectorElephant.git`, then you would type, from your project root, `git submodule add git@github.com:MyAcct/InspectorElephant.git`. The QA tools would then appear in a subrepository at the directory `InspectorElephant`. You can then rename it using git mv or with the --name option. You now have a separate git repository within your original project, which you can use to track any custom testing scripts and configuration files you may choose to implement.

3) Write your own versions of the buildkite scripts and configuration files. Examples with documentation have been given. They end with the .sample extension. The `.cfg`, `cleanfiles.sh`, and `pre-commit` scripts are mandatory to reimplement, but you can safely skip some of the buildkite scripts if they don't fall within your project scope.

4) Run the install.sh script to copy a .gitignore file into your project home. It will also copy a pre-commit hook to save you pain with whitespaces and also the cleanfiles script to make sure you don't accidentally delete valuable files. More detail of the pre-commit hook can be found [here](https://theochem.github.io/horton/2.0.1/tech_dev_git.html#tools-pre-commit)

Config Files
============
The qa/trapdoor.cfg file has the following format. It is parsed as a JSON file and as such should conform to that syntax.

| Field              | Description                                                           | Example                                                                                        |
|--------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| "py_packages"      | Name(s) of python package                                             | ["horton"]                                                                                     |
| "py_directories"   | Directories to check for python code style (relative to project root) | ["horton", "tools/qa", "scripts", "doc"]                                                       |
| "py_test_files"    | Directories of nosetest files                                         | ["horton/test/test_*.py", "horton/*/test/test_*.py"]                                           |
| "py_exclude"       | Files to exclude from python source checks                            | ["cpplint.py"]                                                                                 |
| "py_invalid_names" | Names which should not be exported in \_\_all\_\_.                    | ["np", "numpy", "m", "math", "scipy", "sp", "matplotlib",,"pyplot", "plt", "pt", "h5py", "h5"] |
| "cpp_directories"  | Directories to check for c++ code style (relative to project root)    | ["horton"]                                                                                     |
| "cpp_exclude"      | .Files to exclude from c++ source checks                              | ["*_inc.cpp", "cext.cpp"]                                                                      |
| "doxygen_root"     | Directory with documentation (relative to project root)               | "doc"                                                                                          |
| "doxygen_conf"     | Name of doxygen config file (within doxygen_root)                     | "doxygen.conf"                                                                                 |
| "doxygen_warnings" | Doxygen warning file specified by WARN_LOGFILE in doxygen_conf        | "doxygen_warnings.log"                                                                         |

Explanation of Scripts
======================
The scripts in _qa_ are used by the continuous integration (Buildkite and, for the time being, also Travis-CI). Most scripts can also be used locally to hunt down problems in the CI.

The buildkite_* scripts are run on the buildkite cluster. The current examples are for testing HORTON. To reimplement them, you must change the relevant details in each script to build and run your unit tests. These scripts are essentially bash scripts with some extra environmental variables made available for obtaining information from github, and also some machinery for parallelizing builds. More information can be found [here](https://buildkite.com/docs/guides/writing-build-scripts), [here](https://buildkite.com/docs/guides/artifacts) , and [here](https://buildkite.com/docs/guides/environment-variables) .

The script qa/simulate_trapdoor_pr.py facilitates local execution of the trapdoor scripts. These scripts will not allow a degredation in code quality. i.e. If your past commit had 5 undocumented functions, your current commit cannot have 6 or higher undocumented functions.  

The trapdoor scripts are for testing different aspects of code quality. 

- qa/trapdoor_coverage.py: Percentage of code covered by unit tests
- qa/trapdoor_cppcheck.py: Static analysis of c++ bugs.
- qa/trapdoor_cpplint.py: c++ code style
- qa/trapdoor_doxygen.py: c++ documentation
- qa/trapdoor_import.py: safeguard against bad import style.
- qa/trapdoor_namespace.py: checks for namespace collisions within project.
- qa/trapdoor_pycodestyle.py: Python coding style (PEP8)
- qa/trapdoor_pydocstyle.py: Python doc style (PEP257)
- qa/trapdoor_pylint.py: Additional Python coding style.
