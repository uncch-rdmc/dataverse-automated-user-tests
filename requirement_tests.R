library(RSelenium)
library(testthat)
library(askpass)
library(urltools)

mainpath_state <- TRUE
default_wait <- 2 #If a target system is running slow, bump this to increase the wait globally
dataverse_name <- "rselenium-test-dataverse"
dataset_name <- "rselenium-test-dataset"
dataset_id <- "" #set by code
template_id <- "" #set by code
root_dv_id <- "1" #assumed
login_user_api_token <- "" #set by code

source('functions/api_dataverse.R')
source('functions/test_functions_dataset.R')
source('functions/test_functions_dataverse.R')

#########################
### Requirement Tests ###
#########################

r01alt_mainpath_builtin_auth <- function() {
  username <- askpass("Username for builtin account")
  password <- askpass("Password for builtin account")
  #username <- ''
  #password <- ''
  
  sesh$navigate(paste(dv_server_url,'/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml', sep=''))
  #
  sesh$findElement(value='//*[@id="loginForm:credentialsContainer:0:credValue"]')$sendKeysToElement(list(username))
  sesh$findElement(value='//*[@id="loginForm:credentialsContainer:1:sCredValue"]')$sendKeysToElement(list(password, key="enter"))
  #NOTE: For some reason this button click works with directly setting username/password, but NOT when using askpass.
  #      currently the code is just triggering an enter key after entering the password, but we may have the issue again
  #      ...
  #      I'm pretty sure this is an old issue due to using safari
  
  #sesh$findElement(using="xpath", value='//*[@id="loginForm:login"]')$clickElement()
  #sesh$screenshot(file = 'atest.png')
  
  sesh$findElement(value='//*[@id="dataverseDesc"]') #Find element to wait for load
  expect_identical(paste(dv_server_url,'/dataverse.xhtml', sep=''), toString(sesh$getCurrentUrl()))
}

r03_mainpath_create_sub_dataverse <- function() {
  sesh$navigate(dv_server_url)
  ### Main Landing Page ###
  sesh$findElement(value='//*[@id="addDataForm"]/div/button')$clickElement() #click add data
  sesh$findElement(value='//*[@id="addDataForm"]/div/ul/li[1]/a')$clickElement() #click new dataverse
  
  ### Create Dataverse Page ###
  sesh$findElement(value='//*[@id="dataverseForm:selectHostDataverse_input"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:selectHostDataverse_input"]')$sendKeysToElement(list(paste(dv_props["host_dataverse"], sep='')))
  Sys.sleep(2) # wait for host list to load
  sesh$findElement(value='//*[@id="dataverseForm:selectHostDataverse_input"]')$sendKeysToElement(list(key = "enter"))
  Sys.sleep(.5) # wait after click for ui to be usable
  set_dataverse_metadata(add_string="create") #Metadata that is same for create/edit
 
  ### Test Save ###
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  expect_identical(paste(dv_server_url,'/dataverse/',dataverse_name, '/', sep=''), toString(sesh$getCurrentUrl())) #confirm page
  
  test_dataverse_metadata(add_string="create")
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  
  ### Dataverse Page - Publish ###
  
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/button')$clickElement() #click publish
  sesh$findElement(value='//*[@id="dataverseForm:j_idt431"]')$clickElement() #confirm publish
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
}

r04_mainpath_edit_dataverse <- function() {
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  Sys.sleep(default_wait)
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button')$clickElement()
  sesh$findElement(value='//*[@id="dataverseForm:editInfo"]')$clickElement()
  
  set_dataverse_metadata()
  test_dataverse_metadata()
  
  Sys.sleep(1) #wait before switching pages in r05
}

r05_mainpath_create_metadata_template <- function() {
  sesh$navigate(dv_server_url)
  Sys.sleep(default_wait)

  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div[2]/div[2]/div/button')$clickElement() #click dataverse edit button
  sesh$findElement(value='//*[@id="dataverseForm:manageTemplates"]')$clickElement() #click manage templates
  Sys.sleep(default_wait)
  sesh$findElement(value='//*[@id="manageTemplatesForm"]/div[1]/div/a')$clickElement() #click create dataset template
  Sys.sleep(default_wait)
  sesh$findElement(value='//*[@id="templateForm:templateName"]')$sendKeysToElement(list("test template create")) #Create template title
  set_dataset_metadata_edit(add_string='create', xpath_dict=ds_template_xpaths)

  sesh$findElement(value='//*[@id="templateForm:j_idt892"]')$clickElement() #click "Save + Add Terms"

  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div[1]')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  template_id <<- toString(param_get(toString(sesh$getCurrentUrl()), c("id")))
  # sesh$navigate(dv_server_url)
  # Sys.sleep(default_wait)
  # sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div[2]/div[2]/div/button')$clickElement() #click dataverse edit button
  # sesh$findElement(value='//*[@id="dataverseForm:manageTemplates"]')$clickElement() #click manage templates
  # Sys.sleep(9999999999)
  #TODO: I'm not sure what ownerId refers to. We may need to go through the UI (like we probably will have to for delete anyways...)
  sesh$navigate(paste(dv_server_url, '/template.xhtml?id=', template_id, '&ownerId=1&editMode=METADATA', sep=''))
  test_dataset_metadata(add_string='create', xpath_dict=ds_template_xpaths)
}

r09_mainpath_create_dataset <- function() {
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  
  sesh$findElement(value='//*[@id="addDataForm"]/div/button')$clickElement() #click add data
  sesh$findElement(value='//*[@id="addDataForm"]/div/ul/li[2]/a')$clickElement() #click new dataset
  
  set_dataset_metadata_create(add_string='create')
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div[1]')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  
  ### Get dataset id from permissions page url for later uses ###
  dataset_id <<- sub(".*=", "", sesh$findElement(value='//*[@id="datasetForm:manageDatasetPermissions"]')$getElementAttribute("href")) 
  # print(dataset_id)
  
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div[1]/div/a')$clickElement() #click publish

  sesh$findElement(value='//*[@id="datasetForm:j_idt2547"]')$clickElement() #click publish confirm

  sesh$findElement(value='label-default', using='class name') #Find element to wait for load. May trigger prematurely with files added.
  expect_identical(toString(sesh$findElement(value='//*[@id="title-label-block"]/span')$getElementText()), "Version 1.0") #Test dataset published
  
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click edit dataset
  
  test_dataset_metadata(add_string='create', is_update=FALSE, xpath_dict=ds_edit_xpaths)
  
  sesh$findElement(value='//*[@id="datasetForm:cancel"]')$clickElement() #click out after testing data
  
  Sys.sleep(default_wait)
}

r10_mainpath_edit_dataset <- function() {
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click new dataset

  set_dataset_metadata_edit(add_string='edit', xpath_dict=ds_edit_xpaths)
  sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #click to create dataset

  sesh$findElement(value='//*[@id="actionButtonBlock"]/div[1]/div/a')$clickElement() #click publish

  sesh$findElement(value='//*[@id="datasetForm:j_idt2547"]')$clickElement() #click publish confirm
  
  sesh$findElement(value='label-default', using='class name') #Find element to wait for load. May trigger prematurely with files added.
  expect_identical(toString(sesh$findElement(value='//*[@id="title-label-block"]/span')$getElementText()), "Version 1.1") #Test dataset published
  
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click new dataset
  
  test_dataset_metadata(add_string='edit', is_update=TRUE, xpath_dict=ds_edit_xpaths) 

  sesh$findElement(value='//*[@id="datasetForm:cancelTop"]')$clickElement() #click cancel out of edit after testing
}


#############################################
### Requirement Test Additional Functions ###
#############################################

# TODO:
# - Begin implementing R03-R25
# - How do I handle cleanup?
#   - Probably best to tie it into the call_mainpath error code? Try to do deletes if possible.
#   - I need to delete datasets AND a dataverse

load_dataverse_admin_info_from_file <- function() {
  #Currently this is programmed to read from a secret_table file located at a fixed directory
  #TODO: This needs to be made dynamic once I understand how to do this better in rstudio
  dframe <- read.table(file='/Users/madunlap/Documents/GitHub/secret_table.txt',header=FALSE,
                       sep='=',col.names=c('key','value'))
  dtable <- data.table(dframe,key='key')
  
  #TODO: remove api token if we end up not needing it (we pull the user's instead)
  dv_server_url <<- dtable["DATAVERSE_SERVER_URL"]$value
  dv_admin_api_token <<- dtable["DATAVERSE_API_TOKEN"]$value
}

begin_user_browser <- function() {
  sesh <<- remoteDriver(
    remoteServerAddr = "localhost",
    port = 4444L,
    browserName = "chrome"
  )
  #sesh$errorDetails()
  sesh$open(silent=TRUE)
  #NOTE: This sets the timeout used to search for elements. This does not apply to other things like checking the current URL.
  #      In some places in this code we check for an element before checking the URL to leverage this dynamic check instead of setting explicit waits
  sesh$setTimeout("implicit", milliseconds=20000) #Set very high to handle dataverse publish steps
  # implicit_timeouts(sesh, 15000)
  #sesh$getStatus()
}

# Wrapper for all mainpath test functions. Allows us to not rewrite the same code over-and-over for all tests
call_mainpath <- function(FUN) {
  if(!mainpath_state) { return(mainpath_state) } #Fails if previous mainpath tests have failed
  
  mainpath_state <<- tryCatch({
    FUN()
    return(TRUE)
  }, expectation_failure=function(e) { #catch testthat failures
    print(e)
    return(FALSE)
  },error = function(e) { #catch general errors
    print(e)
    print(sesh$errorDetails()$localizedMessage)
    return(FALSE)
  })
  
  return(mainpath_state)
}

clean_up_mainpath <- function(do_ds=TRUE, do_dv=TRUE, do_tmp=TRUE) {
  if(do_ds) {
    tryCatch({
      destroy_dataset(dataset_id, dv_server_url, login_user_api_token) #dv_admin_api_token)
    }, error = function(e) { #print error
      print("Dataset Destroy Error")
      print(e)
    })
  }
  if(do_dv) {
    tryCatch({
      delete_dataverse(dataverse_name, dv_server_url, login_user_api_token) #dv_admin_api_token)
      sesh$navigate(dv_server_url)
    }, error = function(e) { #print error
      print("Dataverse Delete Error")
      print(e)
    })
  }
  if(do_tmp) {
    delete_template_via_ui(id=template_id, dv_id=root_dv_id) #based on the assu
    # tryCatch({
    #   delete_dataset_template(template_id, dv_server_url, login_user_api_token) #dv_admin_api_token)
    #   sesh$navigate(dv_server_url)
    # }, error = function(e) { #print error
    #   print("Dataverse Delete Error")
    #   print(e)
    # })
  }
}

#We get the api token for the logged in user
get_api_token <- function() {
  sesh$navigate(paste(dv_server_url,'/dataverseuser.xhtml?selectTab=apiTokenTab', sep=''))
  #Note: This test assumes you have already clicked "Create Token" with this account.
  login_user_api_token <<- toString(sesh$findElement(value='//*[@id="apiToken"]/pre/code')$getElementText())
}

##This is not currently needed for our requirements. It was built to get around permissions issues for our admin off the root dataverse 
# test_delete_dataverse <- function() {
#   sesh$navigate(paste(dv_server_url,'/dataverse/',dataverse_name, sep=''))
#   
#   Sys.sleep(default_wait)
#   
#   sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/div/button')$clickElement() #click edit
#   sesh$findElement(value='//*[@id="dataverseForm:deleteDataset"]')$clickElement() #click delete
#   sesh$findElement(value='//*[@id="dataverseForm:j_idt435"]')$clickElement() #click confirm
#   
#   Sys.sleep(default_wait)
#   
#   expect_identical(paste(dv_server_url,'/dataverse/root/', sep=''), toString(sesh$getCurrentUrl())) #confirm page
#   expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
#   
# }