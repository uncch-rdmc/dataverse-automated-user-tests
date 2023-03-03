# holds api calls we need for our testing
require(data.table)
library(httr)
#library(jsonlite)
# known api needs:
# - delete dataverse

destroy_dataset <- function(pid) {
  #Currently this is programmed to read from a secret_table file located at a fixed directory
  #TODO: This needs to be made dynamic once I understand how to do this better in rstudio
  dframe <- read.table(file='/Users/madunlap/Documents/GitHub/secret_table.txt',header=FALSE,
                       sep='=',col.names=c('key','value'))
  print(dframe)
  dtable <- data.table(dframe,key='key')
  print(dtable)
  print(dtable["DATAVERSE_API_TOKEN"]$value)
  print(dtable["DATAVERSE_SERVER_URL"]$value)
  
  #TODO: try connecting to a rest api
  #curl -H "X-Dataverse-key:$API_TOKEN" -X DELETE http://$SERVER/api/datasets/999/destroy
  call <- paste(dtable["DATAVERSE_SERVER_URL"]$value, "/api/datasets/:persistentId/destroy?persistentId=", pid, sep='')
  print(call)
  delete_dataset_response <- DELETE(url = call,
                            add_headers('X-Dataverse-key' = dtable["DATAVERSE_API_TOKEN"]$value),
                            verbose(info = TRUE))
  status_code(delete_dataset_response)
  content(delete_dataset_response)

}

destroy_dataset("doi:10.5072/FK2/LSJD0F")