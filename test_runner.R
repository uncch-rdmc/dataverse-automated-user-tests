# I have this code currently working with selenium-server-standalone-3.9.1.jar. It only seems to work with safari
# I tried running 'selenium-server-4.8.1.jar standalone --port 4444', and while this code connects it doesn't seem to do anything after and doesn't report errors

#export PATH="/Users/madunlap/Downloads/chromedriver_mac64:$PATH"
#java -jar ~/Downloads/selenium-server-standalone-3.9.1.jar
#setwd("~/Documents/GitHub/dataverse-automated-user-tests")
source('requirement_tests.R')

try(sesh$closeWindow())

load_dataverse_admin_info_from_file()
begin_user_browser()
call_mainpath(r01alt_mainpath_builtin_auth)
call_mainpath(get_api_token)
# call_mainpath(r05_mainpath_create_metadata_template)
# clean_up_mainpath(do_ds=FALSE, do_dv=FALSE) #TODO: I think admin endpoints are blocked by default outside localhost... so I may need to delete this via the UI... but that's also fairly sketchy :(

call_mainpath(r03_mainpath_create_sub_dataverse)
#TODO: I'm seeing a ui error when calling r04 initially, even though the code passes. Investigate
call_mainpath(r04_mainpath_edit_dataverse)
call_mainpath(r05_mainpath_create_metadata_template)
call_mainpath(r09_mainpath_create_dataset)
call_mainpath(r10_mainpath_edit_dataset)
clean_up_mainpath() #TODO: Destroying dataset seemed to fail sometimes. Maybe we aren't waiting enough?

#source('dv_tests.R') #TODO: remove
#call_mainpath(r09_mainpath_create_dataset)
#clean_up_mainpath(do_dv=FALSE) #TODO: remove


