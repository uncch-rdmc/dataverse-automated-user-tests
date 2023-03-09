# holds api calls we need for our testing
require(data.table)
library(httr)
#library(jsonlite)

destroy_dataset <- function(id, server, token) {
  call <- paste(server, "/api/datasets/", id, "/destroy", sep='')
  print(call)
  destroy_dataset_response <- DELETE(url = call,
                            add_headers('X-Dataverse-key' = token),
                            verbose(info = TRUE))
  status_code(destroy_dataset_response)
  content(destroy_dataset_response)
  #TODO: return anything?
}

delete_dataverse <- function(alias, server, token) {
  call <- paste(server, "/api/dataverses/", alias, sep='')
  print(call)
  delete_dataverse_response <- DELETE(url = call,
                                    add_headers('X-Dataverse-key' = token),
                                    verbose(info = TRUE))
  status_code(delete_dataverse_response)
  content(delete_dataverse_response)
  #TODO: return anything?
}