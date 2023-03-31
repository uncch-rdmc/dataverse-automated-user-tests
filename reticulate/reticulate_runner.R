#install.packages("rstudioapi")
#rstudioapi::writeRStudioPreference("console_max_lines", 5000L)

library(reticulate)

setwd("~/Documents/GitHub/dataverse-automated-user-tests/reticulate")
source('helper.R')

source_python('python/requirement_tests.py')
#py_tests <- PyClass('RequirementTests')

py_tests <- RequirementTests()
#We have to manually reload our modules referenced by requirement_tests.py if we want to be able to change them without restarting RStudio.
importlib <- import("importlib")
python <- import("python")
importlib$reload(python$dataset_test_helper)
importlib$reload(python$dataverse_test_helper)
# sys <- import('sys')
# print(sys$modules)

#py_tests$linear_test_runner('','')

get_dv_username_password()

py_tests$test_caller(py_tests$begin_user_browser)
py_tests$set_username_password(username, password)
py_tests$test_caller(py_tests$r01alt_mainpath_builtin_auth)
py_tests$test_caller(py_tests$r03_mainpath_create_sub_dataverse)

py_tests$test_caller(py_tests$r04_mainpath_edit_dataverse)
py_tests$test_caller(py_tests$r05_mainpath_create_metadata_template)
py_tests$test_caller(py_tests$r06_mainpath_edit_metadata_template)
py_tests$test_caller(py_tests$r09_mainpath_create_dataset)
py_tests$test_caller(py_tests$r10_mainpath_edit_dataset)

# call_mainpath(r04_mainpath_edit_dataverse)
# call_mainpath(r05_mainpath_create_metadata_template)
# call_mainpath(r06_mainpath_edit_metadata_template)
# call_mainpath(r09_mainpath_create_dataset)
# call_mainpath(r10_mainpath_edit_dataset)
#clean_up_mainpath()

py_tests$sesh$close() #probably unneeded, python code causes exit on its own?

# print(username)
# print(password)