# I have this code currently working with selenium-server-standalone-3.9.1.jar. It only seems to work with safari
# I tried running 'selenium-server-4.8.1.jar standalone --port 4444', and while this code connects it doesn't seem to do anything after and doesn't report errors

#export PATH="/Users/madunlap/Downloads/chromedriver_mac64:$PATH"
#java -jar ~/Downloads/selenium-server-standalone-3.9.1.jar
#setwd("~/Documents/GitHub/dataverse-automated-user-tests")
source('dv_tests.R')

try(sesh$closeWindow())

load_dataverse_admin_info_from_file()
begin_user_browser()
call_mainpath(r01alt_mainpath_builtin_auth)
call_mainpath(test_get_api_token)

call_mainpath(r03_mainpath_create_sub_dataverse)
call_mainpath(r09_mainpath_create_dataset)
#TODO: Ask Don tomorrow about ways to get delete permissions of dataverses directly off the root dataverse
clean_up_mainpath()
#test_delete_dataverse()
#TODO: If we can't find a simple way for our admin to get permissions on the root dataverse, then we'll need a better path
#      - Immediately we'll need a way to delete the dataset