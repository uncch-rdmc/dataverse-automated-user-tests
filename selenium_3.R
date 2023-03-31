library(RSelenium)

#' CLASS remoteDriver3

### Additional selenium 3 driver calls. RSelenium is only for 2.0 and certain functions are missing/broken ###

remoteDriver3 <- 
  setRefClass(
    contains=remoteDriver,
    methods = list (
      getActiveElement = function(){
        
      },
    )
  )


getActiveElement = function() {
  "Get the element on the page that currently has focus. The located
        element will be returned as a WebElement id."
  qpath <- sprintf(
    "%s/session/%s/element/active",
    serverURL, sessionInfo[["id"]]
  )
  queryRD(qpath)
  .self$value
},