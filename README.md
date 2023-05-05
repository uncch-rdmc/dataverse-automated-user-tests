# dataverse-automated-user-tests

#### Selenium-based user tests for Dataverse that generate reports using Python/Jinja2.
##

### General Info
Currently this project only supports use of the Chrome browser and has been tested both on macOS and Windows. This was developed using Visual Studio Code and files (`sample.env`/`.vscode/launch.json` are provided to run the code via those means). You can also run the code by setting the environment variables with `python/env.secret.sample.sh`.

This project has been written to be run two different ways. The main way is by running `python/html/html_gen.py`, which will generate an html report of the test results. During development, `test_development.ipynb` can be used to run the tests inside a Jupyter Notebook. This is very helpful as when tests fail you can easily keep working with the browser session and write out the correct test automation. It is also easy to call the `IngestWorkflowReportTestCase` inside `python/tests/test_ingest_workflow_report.py` to call the tests directly.

The test suite has been written to allow disabling parts of the tests. Specifically, testing of files can be disabled to remove those manual components. Currently to test accounts via built-in-auth, instead of SSO, the built-in-auth test needs to be swapped in via `IngestWorkflowReporTestCase.test_requirements()`. It is planned to make this doable without code changes in the near future. Note that disabling test components will make the html report inaccurate. We require manual interaction for file uploads because automating file interactions is painful in windows and practically impossible with macOS.

##

### Notes for use:
- Make sure to generate the api token for the user named in `DATAVERSE_TEST_USER_USERNAME`
- Resizing browser window can cause tests to break. Window should be 1200x827 or larger. This will be done automatically for html generation but is not currently for other testing (the default in chrome is large enough on most machines)
