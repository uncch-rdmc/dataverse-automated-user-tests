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
  
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:dataverseCategory"]/option[@selected]')$getElementText()), toString(dv_props['category']))
  expect_identical(toString(sesh$findElement(value='//*[@id="dataverseForm:j_idt271:0:contactEmail"]')$getElementAttribute("value")), paste(add_string, dv_props['email'], sep=''))
  
  sesh$findElement(value='//*[@id="dataverseForm:cancel"]')$clickElement()
  
}