# Software_Testing_asm3
Assignment 3 of Software Testing (Sem 221)

## Initial setup
- Install Python bindings for Selenium: `pip install selenium`
- Install webdriver manager: `pip install webdriver-manager`
- Config webdriver manager based on [this guide](https://github.com/SergeyPirogov/webdriver_manager#configuration). Configurations for webdriver manager should be written in `.webdriver_manager.env` (see `.webdriver_manager_example.env` for the template)

## Writing test cases
- Each folder in the `test_cases` folder represents a functional requirement.
- Each folder containing test cases must also contain an empty `__init__.py` file. Otherwise, unittest cannot discover and run the test cases inside that folder.
- Each test case is contained in a Python file of which name matches the pattern `TC_*_*.py`. The filename must be a valid Python identifier. For example, `TC-001-001` is not a valid Python identifier, so it can't be a filename.
- Example test cases: see `test_cases/private_file_upload` for examples.
- Notes:
  - It's best to install pre-commit hooks to re-format the files before pushing your work to origin. Commands:
    - `pip install pre-commit`
    - `pre-commit install`

## Running test cases
- Go to the top-level folder `Software_Testing_asm3`
- Run tests for specific functional requirements: `./run_tests.sh <folder name 1> <folder name 2> ...`
  - Example: `./run_tests.sh private_file_upload`
- Run all tests: `./run_tests.sh`
