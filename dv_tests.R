library(RSelenium)
library(testthat)
library(askpass)
source('dv_api.R')

mainpath_state <- TRUE
default_wait <- .5 #If a target system is running slow, bump this to increase the wait globally
dataverse_name <- "rselenium-test-dataverse"
dataset_name <- "rselenium-test-dataset"
dataset_id <- "" #set by code
login_user_api_token <- "" #set by code

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
  sesh$open()
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

clean_up_mainpath <- function() {
  tryCatch({
    destroy_dataset(dataset_id, dv_server_url, login_user_api_token) #dv_admin_api_token)
  }, error = function(e) { #print error
    print(e)
  })
  tryCatch({
    delete_dataverse(dataverse_name, dv_server_url, login_user_api_token) #dv_admin_api_token)
  }, error = function(e) { #print error
    print(e)
  })
  sesh$navigate(dv_server_url)
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

set_consistent_dataverse_metadata <- function(prefix='') {
  # We clear all the elements for when this code is called during edit and there are already contents
  sesh$findElement(value='//*[@id="dataverseForm:name"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:name"]')$sendKeysToElement(list(paste(prefix, dv_props["name"], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:affiliation"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:affiliation"]')$sendKeysToElement(list(paste(prefix, dv_props["affiliation"], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:identifier"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:identifier"]')$sendKeysToElement(list(paste(prefix, dv_props["identifier"], sep='')))
  dataverse_name <<- paste(prefix, dv_props["identifier"], sep='')
  sesh$findElement(value='//*[@id="dataverseForm:dataverseCategory"]')$sendKeysToElement(list(dv_props["category"]))
  sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$sendKeysToElement(list(paste(prefix, dv_props["email"], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:description"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:description"]')$sendKeysToElement(list(paste(prefix, dv_props["description"], sep='')))
  
  sesh$findElement(value='//*[@id="dataverseForm:save"]')$clickElement() #create dataverse
  
  Sys.sleep(default_wait)
}

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
  #sesh$findElement(using="xpath", value='//*[@id="loginForm:login"]')$clickElement()
  #sesh$screenshot(file = 'atest.png')
  
  Sys.sleep(default_wait) #Wait for page load. We should be able to use setImplicitWaitTimeout, but that doesn't seem to work currently due to rselenium being stale
  
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
  set_consistent_dataverse_metadata(prefix="create") #Metadata that is same for create/edit
 
  ### Test Save ###
  
  expect_identical(paste(dv_server_url,'/dataverse/',dataverse_name, '/', sep=''), toString(sesh$getCurrentUrl())) #confirm page
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  
  test_dataverse_metadata(prefix="create")
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  
  ### Dataverse Page - Publish ###
  
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/button')$clickElement() #click publish
  sesh$findElement(value='//*[@id="dataverseForm:j_idt431"]')$clickElement() #confirm publish
  
  Sys.sleep(default_wait)
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
}

r04_mainpath_edit_dataverse <- function() {
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button')$clickElement()
  sesh$findElement(value='//*[@id="dataverseForm:editInfo"]')$clickElement()
  
  Sys.sleep(default_wait)
  
  set_consistent_dataverse_metadata()
  test_dataverse_metadata()
}

r09_mainpath_create_dataset <- function() {
  sesh$findElement(value='//*[@id="addDataForm"]/div/button')$clickElement() #click add data
  sesh$findElement(value='//*[@id="addDataForm"]/div/ul/li[2]/a')$clickElement() #click new dataset
  
  Sys.sleep(default_wait)
  
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(dataset_name)) #set dataset title
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]')$sendKeysToElement(list("test description")) #set dataset description (text)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2"]')$clickElement() #click subject dropdown      #$sendKeysToElement(list("u")) 
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2_panel"]/div[2]/ul/li[14]/div')$clickElement() #click "other" inside dropdown
  
  sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #create dataset
  
  Sys.sleep(default_wait + 1)
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div[1]')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  
  ### Get dataset id from permissions page url for later uses ###
  dataset_id <<- sub(".*=", "", sesh$findElement(value='//*[@id="datasetForm:manageDatasetPermissions"]')$getElementAttribute("href")) 
  print(dataset_id)
}

###################################
### Sub-test (called by others) ###
###################################

test_dataverse_metadata <- function(prefix='') {
  #TODO: Do we really need this navigate?
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, '/', sep=''))
  
  ### Dataverse Page - Test Save Results ###
  
  expect_identical(toString(sesh$findElement(value='//*[@id="breadcrumbLnk0"]')$getElementText()), toString(dv_props["host_dataverse"]))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseHeader"]/div/div/a/h1')$getElementText()), paste(prefix, dv_props["name"], sep=''))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseHeader"]/div/div/span[1]')$getElementText()), paste('(', prefix, dv_props["affiliation"], ')', sep=''))
  expect_identical(toString(sesh$getCurrentUrl()), paste(dv_server_url,'/dataverse/', prefix, dv_props["identifier"], '/', sep=''))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseDesc"]')$getElementText()), paste(prefix, dv_props["description"], sep=''))
  
  ### Dataverse Edit Page - Test Save Results Additional ###
  # Category and contactEmail do not show up in the overview (public) page, so we test them here
  
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button')$clickElement()
  sesh$findElement(value='//*[@id="dataverseForm:editInfo"]')$clickElement()
  
  Sys.sleep(default_wait)
  
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:dataverseCategory"]/option[@selected]')$getElementText()), toString(dv_props["category"]))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$getElementAttribute("value")), paste(prefix, dv_props["email"], sep=''))
  
  sesh$findElement(value='//*[@id="dataverseForm:cancel"]')$clickElement()
  
}

#######################
### Data Structures ###
#######################

dv_props <- c(
  "host_dataverse"="Root",
  "name"=dataverse_name,
  "affiliation"="Odum",
  "identifier"=dataverse_name,
  "category"="Journal",
  "email"="test@example.com",
  "description"="this is a test description"
)