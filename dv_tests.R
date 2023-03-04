library(RSelenium)
library(testthat)
library(askpass)
source('dv_api.R')

# How are we writing these tests so that they rely on each other?
# - Ideally each unit test should be independent
# - The plan could be to split up unit tests into pieces that can be run as parts
# - I don't know many distinct unit tests we'll have



# TODO Tomorrow:
# - Implement (bad) auth test step via builtin account
# - Begin implementing R03-R25
#   - How am I sharing information between the pieces? Global variables in dv_tests.R? (<<-)

r01alt_builtin_auth <- function() {
  username <- askpass("Username for builtin account")
  password <- askpass("Password for builtin account")
  #username <- ''
  #password <- ''
  
  sesh$navigate(paste(dv_server_url,'/loginpage.xhtml?redirectPage=%2Fdataverse.xhtml', sep=''))
  #Sys.sleep(1)
  sesh$findElement(using="xpath", value='//*[@id="loginForm:credentialsContainer:0:credValue"]')$sendKeysToElement(list(username))
  sesh$findElement(using="xpath", value='//*[@id="loginForm:credentialsContainer:1:sCredValue"]')$sendKeysToElement(list(password, key="enter"))
  #NOTE: For some reason this button click works with directly setting username/password, but NOT when using askpass.
  #      currently the code is just triggering an enter key after entering the password, but we may have the issue again
  #sesh$findElement(using="xpath", value='//*[@id="loginForm:login"]')$clickElement()

}

load_dataverse_admin_info_from_file <- function() {
  #Currently this is programmed to read from a secret_table file located at a fixed directory
  #TODO: This needs to be made dynamic once I understand how to do this better in rstudio
  dframe <- read.table(file='/Users/madunlap/Documents/GitHub/secret_table.txt',header=FALSE,
                       sep='=',col.names=c('key','value'))
  dtable <- data.table(dframe,key='key')
  
  dv_admin_api_token <<- dtable["DATAVERSE_API_TOKEN"]$value
  dv_server_url <<- dtable["DATAVERSE_SERVER_URL"]$value
}

begin_user_browser <- function() {
  sesh <<- remoteDriver(
    remoteServerAddr = "localhost",
    port = 4444L,
    browserName = "safari"
  )
  sesh$errorDetails()
  sesh$open()
  sesh$getStatus()
}

load_dataverse_admin_info_from_file()
begin_user_browser()
r01alt_builtin_auth()
#print(dv_server_url)






sesh$closeWindow()