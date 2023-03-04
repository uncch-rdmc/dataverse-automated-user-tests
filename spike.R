# I have this code currently working with selenium-server-standalone-3.9.1.jar. It only seems to work with safari
# I tried running 'selenium-server-4.8.1.jar standalone --port 4444', and while this code connects it doesn't seem to do anything after and doesn't report errors


#setwd("~/Documents/GitHub/dataverse-automated-user-tests")
source('dv_tests.R')

# remDr$navigate("https://dataverse.unc.edu/")

# advancedSearchButton <- remDr$findElement(using="xpath", value='//*[@id="j_idt443:advsearchlink"]')
# advancedSearchButton$clickElement()

# remDr$closeWindow()

# testvar <- r01alt_builtin_auth()

#expect_identical(1, 1)
