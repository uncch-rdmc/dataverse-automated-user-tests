library(RSelenium)
library(testthat)
library(askpass)
source('dv_api.R')

mainpath_state <- TRUE
default_wait <- .75 #If a target system is running slow, bump this to increase the wait globally
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

clean_up_mainpath <- function(do_ds=TRUE, do_dv=TRUE) {
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
  set_dataverse_metadata(add_string="create") #Metadata that is same for create/edit
 
  ### Test Save ###
  
  expect_identical(paste(dv_server_url,'/dataverse/',dataverse_name, '/', sep=''), toString(sesh$getCurrentUrl())) #confirm page
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  
  test_dataverse_metadata(add_string="create")
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
  
  set_dataverse_metadata()
  test_dataverse_metadata()
}

r09_mainpath_create_dataset <- function() {
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, sep=''))
  sesh$findElement(value='//*[@id="addDataForm"]/div/button')$clickElement() #click add data
  sesh$findElement(value='//*[@id="addDataForm"]/div/ul/li[2]/a')$clickElement() #click new dataset
  
  Sys.sleep(default_wait)
  
  set_dataset_metadata_create(add_string='create')
  
  Sys.sleep(default_wait + 1)
  
  expect_identical(paste(sesh$findElement(value='//*[@id="messagePanel"]/div/div[1]')$getElementAttribute("class")), "alert alert-success") #confirm success alert
  
  ### Get dataset id from permissions page url for later uses ###
  dataset_id <<- sub(".*=", "", sesh$findElement(value='//*[@id="datasetForm:manageDatasetPermissions"]')$getElementAttribute("href")) 
  # print(dataset_id)
  
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click new dataset
  
  Sys.sleep(default_wait)
  
  test_dataset_metadata(add_string='create', is_update=FALSE)
  
  sesh$findElement(value='//*[@id="datasetForm:cancelTop"]')$clickElement() #click add data
  
  Sys.sleep(default_wait)
}

r10_mainpath_edit_dataset <- function() {
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click new dataset
  

  Sys.sleep(default_wait)
  #print("BEFORE EDIT")
  set_dataset_metadata_edit(add_string='edit')
  #print("AFTER EDIT")
  Sys.sleep(default_wait + 1)
  
  sesh$findElement(value='//*[@id="editDataSet"]')$clickElement() #click add data
  sesh$findElement(value='//*[@id="datasetForm:editMetadata"]')$clickElement() #click new dataset
  
  Sys.sleep(default_wait)
  
  #TODO: make is_update true after we implement setting those fields
  #print("BEFORE TEST")
  test_dataset_metadata(add_string='edit', is_update=TRUE) 
  #print("AFTER TEST")
  sesh$findElement(value='//*[@id="datasetForm:cancelTop"]')$clickElement() #click add data
}

###########################################
### Dataverse Test Additional Functions ###
###########################################

dv_props <- c(
  'host_dataverse'='Root',
  'name'=dataverse_name,
  'affiliation'='Odum',
  'identifier'=dataverse_name,
  'category'='Journal',
  'email'='test@example.com',
  'description'='this is a test description'
)

set_dataverse_metadata <- function(add_string='') {
  # We clear all the elements for when this code is called during edit and there are already contents
  sesh$findElement(value='//*[@id="dataverseForm:name"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:name"]')$sendKeysToElement(list(paste(add_string, dv_props['name'], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:affiliation"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:affiliation"]')$sendKeysToElement(list(paste(add_string, dv_props['affiliation'], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:identifier"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:identifier"]')$sendKeysToElement(list(paste(add_string, dv_props['identifier'], sep='')))
  dataverse_name <<- paste(add_string, dv_props['identifier'], sep='')
  sesh$findElement(value='//*[@id="dataverseForm:dataverseCategory"]')$sendKeysToElement(list(dv_props['category']))
  sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$sendKeysToElement(list(paste(add_string, dv_props['email'], sep='')))
  sesh$findElement(value='//*[@id="dataverseForm:description"]')$clearElement()
  sesh$findElement(value='//*[@id="dataverseForm:description"]')$sendKeysToElement(list(paste(add_string, dv_props['description'], sep='')))
  
  sesh$findElement(value='//*[@id="dataverseForm:save"]')$clickElement() #create dataverse
  
  Sys.sleep(default_wait)
}

test_dataverse_metadata <- function(add_string='') {
  #TODO: Do we really need this navigate?
  #      ... Also, we could have maybe just tested this content from the edit page after saving. But maybe this is better?
  sesh$navigate(paste(dv_server_url, '/dataverse/', dataverse_name, '/', sep=''))
  
  ### Dataverse Page - Test Save Results ###
  
  expect_identical(toString(sesh$findElement(value='//*[@id="breadcrumbLnk0"]')$getElementText()), toString(dv_props['host_dataverse']))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseHeader"]/div/div/a/h1')$getElementText()), paste(add_string, dv_props['name'], sep=''))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseHeader"]/div/div/span[1]')$getElementText()), paste('(', add_string, dv_props['affiliation'], ')', sep=''))
  expect_identical(toString(sesh$getCurrentUrl()), paste(dv_server_url,'/dataverse/', add_string, dv_props['identifier'], '/', sep=''))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseDesc"]')$getElementText()), paste(add_string, dv_props['description'], sep=''))
  
  ### Dataverse Edit Page - Test Save Results Additional ###
  # Category and contactEmail do not show up in the overview (public) page, so we test them here
  
  sesh$findElement(value='//*[@id="actionButtonBlock"]/div/div/div[2]/div[2]/button')$clickElement()
  sesh$findElement(value='//*[@id="dataverseForm:editInfo"]')$clickElement()
  
  Sys.sleep(default_wait)
  
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:dataverseCategory"]/option[@selected]')$getElementText()), toString(dv_props['category']))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$getElementAttribute("value")), paste(add_string, dv_props['email'], sep=''))
  
  sesh$findElement(value='//*[@id="dataverseForm:cancel"]')$clickElement()
  
}

#########################################
### Dataset Test Additional Functions ###
#########################################

ds_props <- c(
  #'host_dataverse'='',
  'title'=dataset_name,
  'author_name'='author',
  'author_affiliation'='affiliation',
  #'author_id_type'='ORCID',
  'author_id'='author_affil_id',
  'contact_name'='contact',
  'contact_affiliation'='contact_affil',
  'contact_email'='test@example.com',
  'description'='this is a test description',
  'date'='2022-11-11',
  'subject'='Physics',
  'keyword_term'='keyword',
  'keyword_cv_name'='vocab_name',
  'keyword_cv_url'='https://odum.unc.edu/',
  'related_pub_citation'='this is a test citation',
  #'related_pub_id_type'='lissn',
  'related_pub_id'='pub_id',
  'related_pub_url'='https://odum.unc.edu/',
  'notes'='this is a test note',
  'depositor'='a depositor',
  'deposit_date'='2020-01-01',
  
  'subtitle'='subtitle',
  'alternative_title'='alternative_title',
  'alternative_url'='https://odum.unc.edu/',
  'other_id_agency'='other_id_agency',
  'other_id_id'='other_id_id',
  'topic_class_term'='topic_class_term',
  'topic_class_cv_name'='topic_class_cv_name',
  'topic_class_cv_url'='https://odum.unc.edu/',
  'language'='language',
  'producer_name'='producer_name',
  'producer_affiliation'='produder_affiliation',
  'producer_abbrev_name'='produder_abbrev_name',
  'producer_url'='https://odum.unc.edu/',
  'producer_logo_url'='https://odum.unc.edu/',
  'producer_date'='2020-01-01',
  'producer_location'='produder_location',
  'contributor_type'='contributor_type',
  'contributor_name'='contributor_name',
  'funding_info_agency'='funding_info_agency',
  'funding_info_id'='funding_info_id',
  'distributor_name'='distributor_name',
  'distributor_affiliation'='distributor_affiliation',
  'distributor_abbrev_name'='distributor_abbrev_name',
  'distributor_url'='https://odum.unc.edu/',
  'distributor_logo_url'='https://odum.unc.edu/',
  'distribution_date'='2020-01-01',
  'time_period_start'='2020-01-01',
  'time_period_end'='2020-01-02',
  'date_of_collection_start'='2020-01-01',
  'date_of_collection_end'='2020-01-02',
  'data_type'='data_type',
  'series_name'='series_name',
  'series_info'='series_info',
  'software_name'='software_name',
  'software_version'='software_version',
  'related_material'='related_material',
  'related_dataset'='related_dataset',
  'other_reference'='other_reference',
  'data_source'='data_source',
  'origin_hist_sources'='origin_hist_sources',
  'character_of_sources'='character_of_sources',
  'doc_to_sources'='doc_to_sources'
)

# Used both for editing and seeing results of create/edit
ds_edit_xpaths <- c(
  #'host_dataverse'='',
  'title'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:0:fieldvaluelist:0:inputText"]',
  'author_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:0:inputText"]',
  'author_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:1:inputText"]',
  #'author_id_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_label"]',
  'author_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:3:inputText"]',
  'contact_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:0:inputText"]',
  'contact_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:1:inputText"]',
  'contact_email'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:6:j_idt1679:0:j_idt1681:2:inputText"]',
  'description'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:0:description"]',
  'date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:7:j_idt1679:0:j_idt1681:1:inputText"]',
  'subject'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[1]', #This probably won't work due to the weirdness of the dropdown. Definitely not for create
  'keyword_term'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:0:inputText"]',
  'keyword_cv_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:1:inputText"]',
  'keyword_cv_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:9:j_idt1679:0:j_idt1681:2:inputText"]',
  'related_pub_citation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:0:description"]',
  #'related_pub_id_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_label"]', #Also might not work
  'related_pub_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:2:inputText"]',
  'related_pub_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:3:inputText"]',
  'notes'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:12:fieldvaluelist:0:description"]',
  'depositor'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:21:fieldvaluelist:0:inputText"]',
  'deposit_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:22:fieldvaluelist:0:inputText"]',
  
  'subtitle'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:1:fieldvaluelist:0:inputText"]',
  'alternative_title'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:2:fieldvaluelist:0:inputText"]',
  'alternative_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:3:fieldvaluelist:0:inputText"]',
  'other_id_agency'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:0:inputText"]',
  'other_id_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:4:j_idt1679:0:j_idt1681:1:inputText"]',
  'topic_class_term'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:0:inputText"]',
  'topic_class_cv_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:1:inputText"]',
  'topic_class_cv_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:10:j_idt1679:0:j_idt1681:2:inputText"]',
  'language'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/ul/li/span[2]', #This probably doesn't work, like subject
  'producer_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:0:inputText"]',
  'producer_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:1:inputText"]',
  'producer_abbrev_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:2:inputText"]',
  'producer_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:3:inputText"]',
  'producer_logo_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:14:j_idt1679:0:j_idt1681:4:inputText"]',
  'producer_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:15:fieldvaluelist:0:inputText"]',
  'producer_location'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:16:fieldvaluelist:0:inputText"]',
  'contributor_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_label"]',
  'contributor_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:1:inputText"]',
  'funding_info_agency'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:0:inputText"]',
  'funding_info_id'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:18:j_idt1679:0:j_idt1681:1:inputText"]',
  'distributor_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:0:inputText"]',
  'distributor_affiliation'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:1:inputText"]',
  'distributor_abbrev_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:2:inputText"]',
  'distributor_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:3:inputText"]',
  'distributor_logo_url'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:19:j_idt1679:0:j_idt1681:4:inputText"]',
  'distribution_date'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:20:fieldvaluelist:0:inputText"]',
  'time_period_start'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:0:inputText"]',
  'time_period_end'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:23:j_idt1679:0:j_idt1681:1:inputText"]',
  'date_of_collection_start'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:0:inputText"]',
  'date_of_collection_end'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:24:j_idt1679:0:j_idt1681:1:inputText"]',
  'data_type'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:25:fieldvaluelist:0:inputText"]',
  'series_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:0:inputText"]',
  'series_info'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:26:j_idt1679:0:j_idt1681:1:description"]',
  'software_name'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:0:inputText"]',
  'software_version'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:27:j_idt1679:0:j_idt1681:1:inputText"]',
  'related_material'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:28:fieldvaluelist:0:description"]',
  'related_dataset'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:29:fieldvaluelist:0:description"]',
  'other_reference'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:30:fieldvaluelist:0:inputText"]',
  'data_source'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:31:fieldvaluelist:0:description"]',
  'origin_hist_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:32:fieldvaluelist:0:description"]',
  'character_of_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:33:fieldvaluelist:0:description"]',
  'doc_to_sources'='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:34:fieldvaluelist:0:description"]'
)

# We have different functions for create / edit as the xpath changes between the two, and there is no other way to get the fields
set_dataset_metadata_create <- function(add_string='') {
  # We clear all the elements for when this code is called during edit and there are already contents
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:0:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['title'], sep='')))
  
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_affiliation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_label"]')$clickElement() #click author identifier type dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:2:cvv_2"]')$clickElement() #click "ISNI" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:5:j_idt630:0:j_idt632:3:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['author_id'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_affiliation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:6:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['contact_email'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['description'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:7:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(ds_props['date'], sep=''))
  #TODO: add a clear for the select thing?
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2"]')$clickElement() #click subject dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:8:unique2_panel"]/div[2]/ul/li[14]/div')$clickElement() #click "other" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['keyword_term'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:1:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['keyword_cv_name'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:9:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(ds_props['keyword_cv_url'], add_string, sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['related_pub_citation'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_label"]')$clickElement() #click related pub id type dropdown
  Sys.sleep(.1)
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:1:cvv_4"]')$clickElement() #click "doi" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:2:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['related_pub_id'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:11:j_idt630:0:j_idt632:3:inputText"]')$sendKeysToElement(list(paste(ds_props['related_pub_url'], add_string, sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:12:fieldvaluelist:0:description"]')$sendKeysToElement(list(paste(add_string, ds_props['notes'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:21:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(paste(add_string, ds_props['depositor'], sep='')))
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]')$clearElement()
  sesh$findElement(value='//*[@id="datasetForm:j_idt573:0:j_idt576:22:fieldvaluelist:0:inputText"]')$sendKeysToElement(list(ds_props['deposit_date'], sep=''))
  
  #TODO: Upload files here?
  sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #create dataset
}

set_dataset_metadata_edit <- function(add_string='') {
  
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv"]')$clickElement() #click author identifier type dropdown
  Sys.sleep(.3)
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:5:j_idt1679:0:j_idt1681:2:cvv_4"]')$clickElement() #click "VIAF" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]/ul/li/span[1]')$clickElement() #Delete existing field "Other"
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2"]')$clickElement() #click subject dropdown
  Sys.sleep(.3)
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:8:unique2_panel"]/div[2]/ul/li[10]/div')$clickElement() #click "mathematical science" inside dropdown
  #sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]/div[3]')$clickElement() #click related pub id type dropdown
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv"]')$clickElement() #click related pub id type dropdown
  Sys.sleep(.3)
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:11:j_idt1679:0:j_idt1681:1:cvv_4"]')$clickElement() #click "DOI" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2"]/div[3]')$clickElement() #click language dropdown
  Sys.sleep(.3)
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:13:unique2_panel"]/div[2]/ul/li[2]')$clickElement() #click "Afar" inside dropdown
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv"]')$clickElement() #click contributor type dropdown
  Sys.sleep(.3)
  sesh$findElement(value='//*[@id="datasetForm:tabView:j_idt1622:0:j_idt1625:17:j_idt1679:0:j_idt1681:0:cvv_3"]')$clickElement() #click "Data Manager" inside dropdown
  
  sesh$findElement(value=ds_edit_xpaths['title'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['title'])$sendKeysToElement(list(paste(add_string, ds_props['title'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['author_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['author_name'])$sendKeysToElement(list(paste(add_string, ds_props['author_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['author_affiliation'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['author_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['author_affiliation'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['author_id'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['author_id'])$sendKeysToElement(list(paste(add_string, ds_props['author_id'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['contact_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['contact_name'])$sendKeysToElement(list(paste(add_string, ds_props['contact_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['contact_affiliation'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['contact_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['contact_affiliation'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['contact_email'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['contact_email'])$sendKeysToElement(list(paste(add_string, ds_props['contact_email'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['description'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['description'])$sendKeysToElement(list(paste(add_string, ds_props['description'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['date'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['date'])$sendKeysToElement(list(ds_props['date'], sep=''))
  sesh$findElement(value=ds_edit_xpaths['keyword_term'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['keyword_term'])$sendKeysToElement(list(paste(add_string, ds_props['keyword_term'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['keyword_cv_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['keyword_cv_name'])$sendKeysToElement(list(paste(add_string, ds_props['keyword_cv_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['keyword_cv_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['keyword_cv_url'])$sendKeysToElement(list(paste(ds_props['keyword_cv_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['related_pub_citation'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['related_pub_citation'])$sendKeysToElement(list(paste(add_string, ds_props['related_pub_citation'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['related_pub_id'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['related_pub_id'])$sendKeysToElement(list(paste(add_string, ds_props['related_pub_id'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['related_pub_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['related_pub_url'])$sendKeysToElement(list(paste(ds_props['related_pub_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['notes'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['notes'])$sendKeysToElement(list(paste(add_string, ds_props['notes'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['depositor'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['depositor'])$sendKeysToElement(list(paste(add_string, ds_props['depositor'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['deposit_date'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['deposit_date'])$sendKeysToElement(list(ds_props['deposit_date'], sep=''))

  sesh$findElement(value=ds_edit_xpaths['subtitle'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['subtitle'])$sendKeysToElement(list(paste(add_string, ds_props['subtitle'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['alternative_title'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['alternative_title'])$sendKeysToElement(list(paste(add_string, ds_props['alternative_title'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['alternative_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['alternative_url'])$sendKeysToElement(list(paste(ds_props['alternative_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['other_id_agency'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['other_id_agency'])$sendKeysToElement(list(paste(add_string, ds_props['other_id_agency'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['other_id_id'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['other_id_id'])$sendKeysToElement(list(paste(add_string, ds_props['other_id_id'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['topic_class_term'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['topic_class_term'])$sendKeysToElement(list(paste(add_string, ds_props['topic_class_term'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['topic_class_cv_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['topic_class_cv_name'])$sendKeysToElement(list(paste(add_string, ds_props['topic_class_cv_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['topic_class_cv_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['topic_class_cv_url'])$sendKeysToElement(list(paste(ds_props['topic_class_cv_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_name'])$sendKeysToElement(list(paste(add_string, ds_props['producer_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_affiliation'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['producer_affiliation'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_abbrev_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_abbrev_name'])$sendKeysToElement(list(paste(add_string, ds_props['producer_abbrev_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_url'])$sendKeysToElement(list(paste(ds_props['producer_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_logo_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_logo_url'])$sendKeysToElement(list(paste(ds_props['producer_logo_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['producer_date'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_date'])$sendKeysToElement(list(toString(ds_props['producer_date'])))
  sesh$findElement(value=ds_edit_xpaths['producer_location'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['producer_location'])$sendKeysToElement(list(paste(add_string, ds_props['producer_location'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['contributor_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['contributor_name'])$sendKeysToElement(list(paste(add_string, ds_props['contributor_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['funding_info_agency'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['funding_info_agency'])$sendKeysToElement(list(paste(add_string, ds_props['funding_info_agency'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['funding_info_id'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['funding_info_id'])$sendKeysToElement(list(paste(add_string, ds_props['funding_info_id'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['distributor_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distributor_name'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['distributor_affiliation'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distributor_affiliation'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_affiliation'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['distributor_abbrev_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distributor_abbrev_name'])$sendKeysToElement(list(paste(add_string, ds_props['distributor_abbrev_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['distributor_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distributor_url'])$sendKeysToElement(list(paste(ds_props['distributor_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['distributor_logo_url'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distributor_logo_url'])$sendKeysToElement(list(paste(ds_props['distributor_logo_url'], add_string, sep='')))
  sesh$findElement(value=ds_edit_xpaths['distribution_date'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['distribution_date'])$sendKeysToElement(list(toString(ds_props['distribution_date'])))
  sesh$findElement(value=ds_edit_xpaths['time_period_start'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['time_period_start'])$sendKeysToElement(list(toString(ds_props['time_period_start'])))
  sesh$findElement(value=ds_edit_xpaths['time_period_end'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['time_period_end'])$sendKeysToElement(list(toString(ds_props['time_period_end'])))
  sesh$findElement(value=ds_edit_xpaths['date_of_collection_start'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['date_of_collection_start'])$sendKeysToElement(list(toString(ds_props['date_of_collection_start'])))
  sesh$findElement(value=ds_edit_xpaths['date_of_collection_end'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['date_of_collection_end'])$sendKeysToElement(list(toString(ds_props['date_of_collection_end'])))
  sesh$findElement(value=ds_edit_xpaths['data_type'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['data_type'])$sendKeysToElement(list(paste(add_string, ds_props['data_type'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['series_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['series_name'])$sendKeysToElement(list(paste(add_string, ds_props['series_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['series_info'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['series_info'])$sendKeysToElement(list(paste(add_string, ds_props['series_info'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['software_name'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['software_name'])$sendKeysToElement(list(paste(add_string, ds_props['software_name'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['software_version'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['software_version'])$sendKeysToElement(list(paste(add_string, ds_props['software_version'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['related_material'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['related_material'])$sendKeysToElement(list(paste(add_string, ds_props['related_material'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['related_dataset'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['related_dataset'])$sendKeysToElement(list(paste(add_string, ds_props['related_dataset'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['other_reference'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['other_reference'])$sendKeysToElement(list(paste(add_string, ds_props['other_reference'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['data_source'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['data_source'])$sendKeysToElement(list(paste(add_string, ds_props['data_source'], sep='')))
  sesh$findElement(value=ds_edit_xpaths['origin_hist_sources'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['origin_hist_sources'])$sendKeysToElement(list(paste(add_string, ds_props['origin_hist_sources'], sep='')))  
  sesh$findElement(value=ds_edit_xpaths['character_of_sources'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['character_of_sources'])$sendKeysToElement(list(paste(add_string, ds_props['character_of_sources'], sep='')))  
  sesh$findElement(value=ds_edit_xpaths['doc_to_sources'])$clearElement()
  sesh$findElement(value=ds_edit_xpaths['doc_to_sources'])$sendKeysToElement(list(paste(add_string, ds_props['doc_to_sources'], sep='')))  
  
  sesh$findElement(value='//*[@id="datasetForm:saveBottom"]')$clickElement() #create dataset
}

test_dataset_metadata <- function(add_string='', is_update=FALSE) {
  # if (is_update) {
  #   Sys.sleep(999999999)
  # }
  # add_string='edit'
  # is_update=TRUE
  
  #For some reason, dates are false when tested identical. I'm not sure if some character is being replaced on the backend or what. But this is fine
  #We don't currently test some dropdowns results because it is extremely convoluted to test the values of jquery dropdowns.
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['title'])$getElementAttribute("value")), paste(add_string, ds_props['title'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['author_name'])$getElementAttribute("value")), paste(add_string, ds_props['author_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['author_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['author_affiliation'], sep=''))
  #expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['author_id_type'])$getElementAttribute("value")), paste(add_string, ds_props['author_id_type'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['author_id'])$getElementAttribute("value")), paste(add_string, ds_props['author_id'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['contact_name'])$getElementAttribute("value")), paste(add_string, ds_props['contact_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['contact_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['contact_affiliation'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['contact_email'])$getElementAttribute("value")), paste(add_string, ds_props['contact_email'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['description'])$getElementAttribute("value")), paste(add_string, ds_props['description'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['date'])$getElementAttribute("value")), toString(ds_props['date']))
  #expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['subject'])$getElementAttribute("value")), paste(add_string, ds_props['subject'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['keyword_term'])$getElementAttribute("value")), paste(add_string, ds_props['keyword_term'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['keyword_cv_name'])$getElementAttribute("value")), paste(add_string, ds_props['keyword_cv_name'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['keyword_cv_url'])$getElementAttribute("value")), paste(ds_props['keyword_cv_url'], add_string, sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_pub_citation'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_citation'], sep=''))
  #expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_pub_id_type'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_id_type'], sep=''))
  #TODO: I think this doesn't work because it needs the above set... but weirdly I thought it worked before???? Well it doesn't work now
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_pub_id'])$getElementAttribute("value")), paste(add_string, ds_props['related_pub_id'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_pub_url'])$getElementAttribute("value")), paste(ds_props['related_pub_url'], add_string, sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['notes'])$getElementAttribute("value")), paste(add_string, ds_props['notes'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['depositor'])$getElementAttribute("value")), paste(add_string, ds_props['depositor'], sep=''))
  expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['deposit_date'])$getElementAttribute("value")), toString(ds_props['deposit_date']))

  if (is_update) {
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['subtitle'])$getElementAttribute("value")), paste(add_string, ds_props['subtitle'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['alternative_title'])$getElementAttribute("value")), paste(add_string, ds_props['alternative_title'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['alternative_url'])$getElementAttribute("value")), paste(ds_props['alternative_url'], add_string, sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['other_id_agency'])$getElementAttribute("value")), paste(add_string, ds_props['other_id_agency'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['other_id_id'])$getElementAttribute("value")), paste(add_string, ds_props['other_id_id'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['topic_class_term'])$getElementAttribute("value")), paste(add_string, ds_props['topic_class_term'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['topic_class_cv_name'])$getElementAttribute("value")), paste(add_string, ds_props['topic_class_cv_name'], sep=''))
    # expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['language'])$getElementAttribute("value")), paste(add_string, ds_props['language'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_name'])$getElementAttribute("value")), paste(add_string, ds_props['producer_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['producer_affiliation'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_abbrev_name'])$getElementAttribute("value")), paste(add_string, ds_props['producer_abbrev_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_url'])$getElementAttribute("value")), paste(ds_props['producer_url'], add_string,  sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_logo_url'])$getElementAttribute("value")), paste(ds_props['producer_logo_url'], add_string, sep=''))
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['producer_date'])$getElementAttribute("value")), ds_props['producer_date'])
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['producer_location'])$getElementAttribute("value")), paste(add_string, ds_props['producer_location'], sep=''))
    # expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['contributor_type'])$getElementAttribute("value")), paste(add_string, ds_props['contributor_type'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['contributor_name'])$getElementAttribute("value")), paste(add_string, ds_props['contributor_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['funding_info_agency'])$getElementAttribute("value")), paste(add_string, ds_props['funding_info_agency'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['funding_info_id'])$getElementAttribute("value")), paste(add_string, ds_props['funding_info_id'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['distributor_name'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['distributor_affiliation'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_affiliation'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['distributor_abbrev_name'])$getElementAttribute("value")), paste(add_string, ds_props['distributor_abbrev_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['distributor_url'])$getElementAttribute("value")), paste(ds_props['distributor_url'], add_string, sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['distributor_logo_url'])$getElementAttribute("value")), paste(ds_props['distributor_logo_url'], add_string, sep=''))
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['distribution_date'])$getElementAttribute("value")), ds_props['distribution_date'])
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['time_period_start'])$getElementAttribute("value")), ds_props['time_period_start'])
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['time_period_end'])$getElementAttribute("value")), ds_props['time_period_end'])
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['date_of_collection_start'])$getElementAttribute("value")), ds_props['date_of_collection_start'])
    expect_equivalent(toString(sesh$findElement(value=ds_edit_xpaths['date_of_collection_end'])$getElementAttribute("value")), ds_props['date_of_collection_end'])
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['data_type'])$getElementAttribute("value")), paste(add_string, ds_props['data_type'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['series_name'])$getElementAttribute("value")), paste(add_string, ds_props['series_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['series_info'])$getElementAttribute("value")), paste(add_string, ds_props['series_info'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['software_name'])$getElementAttribute("value")), paste(add_string, ds_props['software_name'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['software_version'])$getElementAttribute("value")), paste(add_string, ds_props['software_version'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_material'])$getElementAttribute("value")), paste(add_string, ds_props['related_material'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['related_dataset'])$getElementAttribute("value")), paste(add_string, ds_props['related_dataset'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['other_reference'])$getElementAttribute("value")), paste(add_string, ds_props['other_reference'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['data_source'])$getElementAttribute("value")), paste(add_string, ds_props['data_source'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['origin_hist_sources'])$getElementAttribute("value")), paste(add_string, ds_props['origin_hist_sources'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['character_of_sources'])$getElementAttribute("value")), paste(add_string, ds_props['character_of_sources'], sep=''))
    expect_identical(toString(sesh$findElement(value=ds_edit_xpaths['doc_to_sources'])$getElementAttribute("value")), paste(add_string, ds_props['doc_to_sources'], sep=''))
  }
}




































