library(reticulate)

#setwd("~/Documents/GitHub/dataverse-automated-user-tests/reticulate")
source('helper.R')

source_python('python/requirement_tests.py')
#py_tests <- PyClass('RequirementTests')

py_tests <- RequirementTests()

#py_tests$linear_test_runner('','')

get_dv_username_password()

py_tests$test_caller(py_tests$begin_user_browser)
py_tests$set_username_password(username, password)
py_tests$test_caller(py_tests$r01alt_mainpath_builtin_auth)

py_tests$sesh$close() #probably unneeded, python code causes exit on its own?

# print(username)
# print(password)