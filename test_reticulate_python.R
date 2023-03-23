# Test calling Python
#install.packages("reticulate")
library(reticulate)
#setwd("~/Documents/GitHub/dataverse-automated-user-tests")

source_python('test.py')
add(5, 10)
test_caller()
test_selenium()

# test <- LoggingInTestCase()
# test.setUp()

#import_main()
# source_python('test2.py')
# py_run_file('test2.py')