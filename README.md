# Software_Testing_asm3
Assignment 3 of Software Testing (Sem 221)
## Initial setup
- Install browsers:
  - Chrome: `sudo apt-get install google-chrome`
  - Firefox: `sudo apt-get install firefox`
  - Edge: Download .deb file [here](https://www.microsoftedgeinsider.com/vi-vn/download?platform=linux-deb) and run `sudo dpkg -i microsoft-edge-beta_*.deb`
- Install dependencies: `pip install -r requirements.txt`
- Config webdriver manager based on [this guide](https://github.com/SergeyPirogov/webdriver_manager#configuration). Configurations for webdriver manager should be written in `.webdriver_manager.env` (see `.webdriver_manager_example.env` for the template)
- Provide credentials for authentication (used to log in to BKeL) in `features/utils/config.py`: see `config_example.py` for the template

## Writing test cases
- Based on the workflow of [Cucumber](https://cucumber.io/)
- The steps are defined in Python files inside the `features/steps` folder. The file `common.py` contains definitions of steps that are used in many scenarios. The step description and associated function name should NOT be duplicated.
- The scenarios are defined in `.feature` file inside the  `features` folder
- The `utils` folder contains reusable code that is too lengthy to be put inside step definitions
- Environmental controls are defined in `features/environment.py`. Read more about it [here](https://behave.readthedocs.io/en/stable/tutorial.html#environmental-controls)

## Running test cases
- Go to the top-level folder `Software_Testing_asm3`
- Run tests for specific functional requirements: `./run_tests.sh func_req_1.feature func_req_2.feature ...`
  - Example: `./run_tests.sh private_file_upload.feature`
- Run all tests: `./run_tests.sh`
- In order to run a scenario/feature in multiple browsers, use the `@multibrowser` tag (see `features/private_file_upload.feature` file for example).
- You can change the list of browsers to run tests in by modifying `CONFIG["DRIVERS"]["BROWSERS"]` in `features/utils/config.py`. The field `CONFIG["DRIVERS"]["DEFAULT_BROWSER"]` specifies which browser to use by default when a scenario/feature is not run in multiple browsers.

## Notes
- It's best to install pre-commit hooks to re-format the files before pushing your work to origin. Commands:
  - `pip install pre-commit`
  - `pre-commit install`
