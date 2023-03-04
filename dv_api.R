# holds api calls we need for our testing
require(data.table)
library(httr)
#library(jsonlite)
# known api needs:
# - delete dataverse

destroy_dataset <- function(pid, server, token) {
  
  #TODO: try connecting to a rest api
  #curl -H "X-Dataverse-key:$API_TOKEN" -X DELETE http://$SERVER/api/datasets/999/destroy
  call <- paste(server, "/api/datasets/:persistentId/destroy?persistentId=", pid, sep='')
  print(call)
  delete_dataset_response <- DELETE(url = call,
                            add_headers('X-Dataverse-key' = token),
                            verbose(info = TRUE))
  status_code(delete_dataset_response)
  content(delete_dataset_response)

}

#destroy_dataset("doi:10.5072/FK2/LSJD0F")